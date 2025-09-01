"""
Compliance ingest service for Blackletter Systems.

This module provides functionality for ingesting compliance feeds:
- Fetch and parse RSS/Atom feeds
- Extract and summarize compliance information
- Store compliance items
"""

import os
import time
import hashlib
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import json

import httpx
import feedparser
from bs4 import BeautifulSoup

from app.core.llm_adapter import generate
from app.models.schemas import ComplianceItem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ingest_compliance_feed(
    url: str,
    source_type: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Ingest a compliance feed.
    
    Args:
        url: URL of the feed
        source_type: Type of source (e.g., ICO, FCA)
        metadata: Additional metadata
        
    Returns:
        Dict[str, Any]: Ingest results
    """
    try:
        # Fetch the feed
        logger.info(f"Fetching feed from {url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            feed_content = response.text
        
        # Parse the feed
        feed = feedparser.parse(feed_content)
        
        # Process entries
        items = []
        
        for entry in feed.entries[:10]:  # Limit to 10 entries for now
            # Extract basic information
            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", entry.get("updated", ""))
            
            # Try to parse the date
            try:
                date = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                try:
                    date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z")
                except ValueError:
                    date = datetime.now()
            
            # Extract content
            content = ""
            if "content" in entry:
                content = entry.content[0].value
            elif "summary" in entry:
                content = entry.summary
            elif "description" in entry:
                content = entry.description
            
            # Clean HTML
            soup = BeautifulSoup(content, "html.parser")
            text_content = soup.get_text(separator=" ", strip=True)
            
            # Generate summary with LLM
            summary = await summarize_compliance_item(title, text_content, source_type)
            
            # Extract tags
            tags = await extract_tags(title, text_content, source_type)
            
            # Create compliance item
            item = ComplianceItem(
                title=title,
                summary=summary,
                source=source_type,
                url=link,
                date=date,
                tags=tags,
                metadata=metadata
            )
            
            items.append(item)
        
        # Store items in database
        # This would typically store in a database, but for now we'll just return them
        
        return {
            "items": items
        }
    
    except Exception as e:
        logger.error(f"Error ingesting compliance feed: {str(e)}")
        raise

async def summarize_compliance_item(
    title: str,
    content: str,
    source_type: str
) -> str:
    """
    Summarize a compliance item using LLM.
    
    Args:
        title: Item title
        content: Item content
        source_type: Type of source
        
    Returns:
        str: Summarized content
    """
    try:
        # Prepare context for LLM
        max_chars = 3000  # Limit text to avoid token limits
        truncated_content = content[:max_chars] + ("..." if len(content) > max_chars else "")
        
        prompt = f"Title: {title}\n\nContent: {truncated_content}\n\nPlease provide a concise summary (3-5 sentences) of this compliance update from {source_type}. Focus on actionable requirements and key changes."
        
        system_prompt = "You are a legal compliance expert. Provide clear, concise summaries of regulatory updates, focusing on practical implications and actionable requirements."
        
        # Generate summary with LLM
        summary = await generate(prompt, system_prompt)
        return summary
    
    except Exception as e:
        logger.error(f"Error summarizing compliance item: {str(e)}")
        return "Failed to generate summary."

async def extract_tags(
    title: str,
    content: str,
    source_type: str
) -> List[str]:
    """
    Extract tags from compliance item using LLM.
    
    Args:
        title: Item title
        content: Item content
        source_type: Type of source
        
    Returns:
        List[str]: Extracted tags
    """
    try:
        # Prepare context for LLM
        max_chars = 2000  # Limit text to avoid token limits
        truncated_content = content[:max_chars] + ("..." if len(content) > max_chars else "")
        
        prompt = f"Title: {title}\n\nContent: {truncated_content}\n\nPlease extract 3-5 relevant tags for this compliance update from {source_type}. Return the tags as a JSON array of strings."
        
        system_prompt = "You are a legal compliance expert. Extract relevant tags for categorizing regulatory updates. Focus on industry sectors, regulatory domains, and compliance requirements."
        
        # Generate tags with LLM
        response = await generate(prompt, system_prompt)
        
        # Try to parse as JSON
        try:
            tags = json.loads(response)
            if isinstance(tags, list):
                return [str(tag).strip().lower() for tag in tags if tag]
        except json.JSONDecodeError:
            # If not valid JSON, extract tags using regex
            import re
            tag_matches = re.findall(r'["\'](#?\w+)["\']', response)
            if tag_matches:
                return [tag.strip().lower() for tag in tag_matches if tag]
            
            # Last resort: split by commas or newlines
            words = re.split(r'[,\n]', response)
            return [word.strip().lower() for word in words if word.strip()]
    
    except Exception as e:
        logger.error(f"Error extracting tags: {str(e)}")
    
    # Default tags based on source type
    default_tags = {
        "ico": ["data protection", "privacy"],
        "fca": ["financial regulation", "compliance"],
        "eu": ["eu regulation", "compliance"],
        "ukgov": ["uk regulation", "compliance"]
    }
    
    return default_tags.get(source_type.lower(), ["compliance"])

async def get_compliance_items(
    source_type: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[ComplianceItem]:
    """
    Get compliance items from database.
    
    Args:
        source_type: Optional filter by source type
        tag: Optional filter by tag
        limit: Maximum number of items to return
        offset: Offset for pagination
        
    Returns:
        List[ComplianceItem]: List of compliance items
    """
    # This would typically query a database
    # For now, return some sample items
    
    items = [
        ComplianceItem(
            title="Updated guidance on data protection impact assessments",
            summary="The ICO has published updated guidance on data protection impact assessments (DPIAs). The new guidance clarifies when DPIAs are mandatory and provides a streamlined template for organizations to use. Key changes include a simplified threshold assessment and clearer examples of high-risk processing activities.",
            source="ico",
            url="https://ico.org.uk/about-the-ico/news-and-events/news-and-blogs/2023/08/updated-guidance-on-data-protection-impact-assessments/",
            date=datetime(2023, 8, 10),
            tags=["data protection", "dpia", "gdpr", "risk assessment"]
        ),
        ComplianceItem(
            title="FCA fines bank for anti-money laundering failures",
            summary="The Financial Conduct Authority (FCA) has fined a major bank £50 million for failures in its anti-money laundering (AML) systems. The bank failed to properly monitor high-risk customers and transactions between 2018 and 2021. Organizations must ensure robust AML controls, particularly for high-risk clients, and maintain adequate transaction monitoring systems.",
            source="fca",
            url="https://www.fca.org.uk/news/press-releases/fca-fines-bank-anti-money-laundering-failures",
            date=datetime(2023, 7, 15),
            tags=["aml", "financial crime", "banking", "fines"]
        ),
        ComplianceItem(
            title="EU adopts new Digital Services Act",
            summary="The European Union has formally adopted the Digital Services Act (DSA), which will impose new obligations on online platforms to manage illegal content and protect users. Large platforms must implement risk management systems, provide transparency on algorithms, and undergo independent audits. The DSA will be fully applicable from January 2024, with earlier compliance required for very large platforms.",
            source="eu",
            url="https://commission.europa.eu/news/digital-services-act-adopted-2023-06-15_en",
            date=datetime(2023, 6, 15),
            tags=["digital services", "online platforms", "content moderation", "eu regulation"]
        )
    ]
    
    # Apply filters
    if source_type:
        items = [item for item in items if item.source.lower() == source_type.lower()]
    
    if tag:
        items = [item for item in items if tag.lower() in [t.lower() for t in item.tags]]
    
    # Apply pagination
    paginated_items = items[offset:offset + limit]
    
    return paginated_items
