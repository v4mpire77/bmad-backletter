"""
Corpus Gatherer - Data Collection Service
Collects and processes large amounts of text data from various sources for NLP training and testing.
"""

import logging
import os
import time
import json
import csv
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from tqdm import tqdm

# Data collection libraries
import feedparser
import arxiv
from scholarly import scholarly
import wikipedia
from newspaper import Article, Config
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import tweepy
import praw
from reddit_api import RedditAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorpusGatherer:
    """
    Comprehensive data corpus gathering service.
    Collects text data from multiple sources for NLP applications.
    """
    
    def __init__(self, output_dir: str = "corpus_data", max_workers: int = 10):
        """
        Initialize the corpus gatherer.
        
        Args:
            output_dir: Directory to save collected data
            max_workers: Maximum number of concurrent workers
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.max_workers = max_workers
        
        # Create subdirectories
        (self.output_dir / "raw").mkdir(exist_ok=True)
        (self.output_dir / "processed").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        
        # Configure requests session with retry strategy
        self.session = self._create_session()
        
        # Initialize data collectors
        self.collectors = {
            'news': self._collect_news,
            'academic': self._collect_academic,
            'wikipedia': self._collect_wikipedia,
            'youtube': self._collect_youtube,
            'reddit': self._collect_reddit,
            'twitter': self._collect_twitter,
            'web': self._collect_web_content
        }
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
        
    def collect_corpus(self, sources: List[str], 
                      query: str = None,
                      max_items: int = 1000,
                      date_from: str = None,
                      date_to: str = None) -> Dict[str, Any]:
        """
        Collect corpus data from multiple sources.
        
        Args:
            sources: List of sources to collect from
            query: Search query (optional)
            max_items: Maximum items per source
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            
        Returns:
            Collection results summary
        """
        results = {
            'total_items': 0,
            'sources': {},
            'metadata': {
                'collection_date': datetime.now().isoformat(),
                'query': query,
                'date_range': {'from': date_from, 'to': date_to}
            }
        }
        
        logger.info(f"Starting corpus collection from {len(sources)} sources")
        
        # Collect from each source
        for source in sources:
            if source in self.collectors:
                try:
                    logger.info(f"Collecting from {source}...")
                    source_results = self.collectors[source](
                        query=query,
                        max_items=max_items,
                        date_from=date_from,
                        date_to=date_to
                    )
                    results['sources'][source] = source_results
                    results['total_items'] += source_results.get('count', 0)
                    
                except Exception as e:
                    logger.error(f"Error collecting from {source}: {e}")
                    results['sources'][source] = {'error': str(e), 'count': 0}
            else:
                logger.warning(f"Unknown source: {source}")
                
        # Save metadata
        self._save_metadata(results)
        
        logger.info(f"Corpus collection completed. Total items: {results['total_items']}")
        return results
        
    def _collect_news(self, query: str = None, max_items: int = 100, 
                     date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect news articles."""
        news_sources = [
            'https://feeds.bbci.co.uk/news/rss.xml',
            'https://rss.cnn.com/rss/edition.rss',
            'https://feeds.reuters.com/reuters/topNews',
            'https://feeds.npr.org/1001/rss.xml',
            'https://www.theguardian.com/world/rss'
        ]
        
        articles = []
        
        for feed_url in news_sources:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:max_items // len(news_sources)]:
                    if query and query.lower() not in entry.title.lower():
                        continue
                        
                    try:
                        # Download and parse article
                        config = Config()
                        config.browser_user_agent = 'Mozilla/5.0'
                        article = Article(entry.link, config=config)
                        article.download()
                        article.parse()
                        
                        if article.text:
                            articles.append({
                                'title': entry.title,
                                'text': article.text,
                                'url': entry.link,
                                'published': entry.get('published', ''),
                                'source': 'news',
                                'feed_url': feed_url
                            })
                            
                    except Exception as e:
                        logger.debug(f"Error processing article {entry.link}: {e}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error processing feed {feed_url}: {e}")
                continue
                
        # Save to file
        self._save_data(articles, 'news_articles.json')
        
        return {
            'count': len(articles),
            'sources': len(news_sources),
            'file': 'news_articles.json'
        }
        
    def _collect_academic(self, query: str = None, max_items: int = 100,
                         date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect academic papers."""
        papers = []
        
        # Collect from arXiv
        if query:
            search = arxiv.Search(
                query=query,
                max_results=max_items,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for result in search.results():
                try:
                    papers.append({
                        'title': result.title,
                        'text': result.summary,
                        'url': result.entry_id,
                        'published': result.published.isoformat(),
                        'source': 'arxiv',
                        'authors': [author.name for author in result.authors],
                        'categories': result.categories
                    })
                except Exception as e:
                    logger.debug(f"Error processing arXiv paper: {e}")
                    continue
                    
        # Collect from Google Scholar
        try:
            if query:
                search_query = scholarly.search_pubs(query)
                for i, pub in enumerate(search_query):
                    if i >= max_items // 2:
                        break
                        
                    try:
                        papers.append({
                            'title': pub.get('bib', {}).get('title', ''),
                            'text': pub.get('bib', {}).get('abstract', ''),
                            'url': pub.get('pub_url', ''),
                            'published': pub.get('bib', {}).get('pub_year', ''),
                            'source': 'scholar',
                            'authors': pub.get('bib', {}).get('author', []),
                            'citations': pub.get('num_citations', 0)
                        })
                    except Exception as e:
                        logger.debug(f"Error processing Scholar paper: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error collecting from Google Scholar: {e}")
            
        # Save to file
        self._save_data(papers, 'academic_papers.json')
        
        return {
            'count': len(papers),
            'sources': ['arxiv', 'scholar'],
            'file': 'academic_papers.json'
        }
        
    def _collect_wikipedia(self, query: str = None, max_items: int = 100,
                          date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect Wikipedia articles."""
        articles = []
        
        if query:
            # Search for articles
            search_results = wikipedia.search(query, results=max_items)
            
            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    articles.append({
                        'title': page.title,
                        'text': page.content,
                        'url': page.url,
                        'published': '',  # Wikipedia doesn't have publication dates
                        'source': 'wikipedia',
                        'categories': page.categories,
                        'links': page.links[:10]  # First 10 links
                    })
                except Exception as e:
                    logger.debug(f"Error processing Wikipedia article {title}: {e}")
                    continue
        else:
            # Get random articles
            try:
                random_pages = wikipedia.random(pages=max_items)
                for title in random_pages:
                    try:
                        page = wikipedia.page(title)
                        articles.append({
                            'title': page.title,
                            'text': page.content,
                            'url': page.url,
                            'published': '',
                            'source': 'wikipedia',
                            'categories': page.categories,
                            'links': page.links[:10]
                        })
                    except Exception as e:
                        logger.debug(f"Error processing Wikipedia article {title}: {e}")
                        continue
            except Exception as e:
                logger.error(f"Error getting random Wikipedia articles: {e}")
                
        # Save to file
        self._save_data(articles, 'wikipedia_articles.json')
        
        return {
            'count': len(articles),
            'sources': ['wikipedia'],
            'file': 'wikipedia_articles.json'
        }
        
    def _collect_youtube(self, query: str = None, max_items: int = 100,
                        date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect YouTube video transcripts."""
        # Note: This requires YouTube Data API key
        videos = []
        
        # For demonstration, we'll use a list of popular video IDs
        # In practice, you'd use the YouTube Data API to search for videos
        sample_video_ids = [
            'dQw4w9WgXcQ',  # Rick Roll
            'kJQP7kiw5Fk',  # Despacito
            '9bZkp7q19f0',  # Gangnam Style
        ]
        
        for video_id in sample_video_ids[:max_items]:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = ' '.join([entry['text'] for entry in transcript_list])
                
                videos.append({
                    'title': f'Video {video_id}',
                    'text': transcript_text,
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'published': '',
                    'source': 'youtube',
                    'video_id': video_id
                })
            except Exception as e:
                logger.debug(f"Error processing YouTube video {video_id}: {e}")
                continue
                
        # Save to file
        self._save_data(videos, 'youtube_transcripts.json')
        
        return {
            'count': len(videos),
            'sources': ['youtube'],
            'file': 'youtube_transcripts.json'
        }
        
    def _collect_reddit(self, query: str = None, max_items: int = 100,
                       date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect Reddit posts and comments."""
        # Note: This requires Reddit API credentials
        posts = []
        
        # For demonstration, we'll create sample data
        # In practice, you'd use PRAW to access Reddit API
        sample_subreddits = ['python', 'machinelearning', 'datascience']
        
        for subreddit in sample_subreddits:
            try:
                # Simulate Reddit data collection
                for i in range(max_items // len(sample_subreddits)):
                    posts.append({
                        'title': f'Sample post {i} from r/{subreddit}',
                        'text': f'This is a sample post content about {subreddit}. ' * 10,
                        'url': f'https://reddit.com/r/{subreddit}',
                        'published': datetime.now().isoformat(),
                        'source': 'reddit',
                        'subreddit': subreddit,
                        'score': 100 + i
                    })
            except Exception as e:
                logger.error(f"Error collecting from r/{subreddit}: {e}")
                continue
                
        # Save to file
        self._save_data(posts, 'reddit_posts.json')
        
        return {
            'count': len(posts),
            'sources': sample_subreddits,
            'file': 'reddit_posts.json'
        }
        
    def _collect_twitter(self, query: str = None, max_items: int = 100,
                        date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect Twitter tweets."""
        # Note: This requires Twitter API credentials
        tweets = []
        
        # For demonstration, we'll create sample data
        # In practice, you'd use tweepy to access Twitter API
        sample_queries = ['python', 'AI', 'machine learning'] if not query else [query]
        
        for search_query in sample_queries:
            try:
                for i in range(max_items // len(sample_queries)):
                    tweets.append({
                        'title': f'Tweet about {search_query}',
                        'text': f'This is a sample tweet about {search_query}. ' * 3,
                        'url': f'https://twitter.com/user/status/{i}',
                        'published': datetime.now().isoformat(),
                        'source': 'twitter',
                        'query': search_query,
                        'likes': 10 + i,
                        'retweets': 5 + i
                    })
            except Exception as e:
                logger.error(f"Error collecting tweets for {search_query}: {e}")
                continue
                
        # Save to file
        self._save_data(tweets, 'twitter_tweets.json')
        
        return {
            'count': len(tweets),
            'sources': sample_queries,
            'file': 'twitter_tweets.json'
        }
        
    def _collect_web_content(self, query: str = None, max_items: int = 100,
                           date_from: str = None, date_to: str = None) -> Dict[str, Any]:
        """Collect web content from various sources."""
        web_pages = []
        
        # Sample websites to scrape
        sample_urls = [
            'https://en.wikipedia.org/wiki/Artificial_intelligence',
            'https://en.wikipedia.org/wiki/Machine_learning',
            'https://en.wikipedia.org/wiki/Deep_learning'
        ]
        
        for url in sample_urls[:max_items]:
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract text content
                text_content = ' '.join([p.get_text() for p in soup.find_all('p')])
                
                if text_content:
                    web_pages.append({
                        'title': soup.title.string if soup.title else url,
                        'text': text_content,
                        'url': url,
                        'published': '',
                        'source': 'web',
                        'domain': url.split('/')[2]
                    })
                    
            except Exception as e:
                logger.debug(f"Error processing web page {url}: {e}")
                continue
                
        # Save to file
        self._save_data(web_pages, 'web_content.json')
        
        return {
            'count': len(web_pages),
            'sources': ['web'],
            'file': 'web_content.json'
        }
        
    def _save_data(self, data: List[Dict], filename: str):
        """Save collected data to file."""
        filepath = self.output_dir / "raw" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Saved {len(data)} items to {filepath}")
        
    def _save_metadata(self, metadata: Dict[str, Any]):
        """Save collection metadata."""
        filepath = self.output_dir / "metadata" / f"collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
            
    def process_corpus(self, input_files: List[str] = None) -> pd.DataFrame:
        """
        Process collected corpus data into a unified format.
        
        Args:
            input_files: List of input files to process (if None, process all)
            
        Returns:
            Processed corpus as DataFrame
        """
        if input_files is None:
            # Process all files in raw directory
            input_files = list((self.output_dir / "raw").glob("*.json"))
        else:
            input_files = [self.output_dir / "raw" / f for f in input_files]
            
        all_data = []
        
        for filepath in input_files:
            if not filepath.exists():
                logger.warning(f"File not found: {filepath}")
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for item in data:
                    processed_item = {
                        'title': item.get('title', ''),
                        'text': item.get('text', ''),
                        'url': item.get('url', ''),
                        'published': item.get('published', ''),
                        'source': item.get('source', ''),
                        'file': filepath.name,
                        'text_length': len(item.get('text', '')),
                        'word_count': len(item.get('text', '').split())
                    }
                    
                    # Add additional metadata
                    for key, value in item.items():
                        if key not in processed_item:
                            processed_item[f'meta_{key}'] = value
                            
                    all_data.append(processed_item)
                    
            except Exception as e:
                logger.error(f"Error processing file {filepath}: {e}")
                continue
                
        # Create DataFrame
        df = pd.DataFrame(all_data)
        
        # Save processed data
        processed_file = self.output_dir / "processed" / "corpus_processed.csv"
        df.to_csv(processed_file, index=False, encoding='utf-8')
        
        # Save as JSON for easier loading
        json_file = self.output_dir / "processed" / "corpus_processed.json"
        df.to_json(json_file, orient='records', indent=2, force_ascii=False)
        
        logger.info(f"Processed corpus saved: {len(df)} items")
        logger.info(f"CSV: {processed_file}")
        logger.info(f"JSON: {json_file}")
        
        return df
        
    def get_corpus_stats(self, df: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Get statistics about the corpus.
        
        Args:
            df: Corpus DataFrame (if None, load from processed file)
            
        Returns:
            Corpus statistics
        """
        if df is None:
            processed_file = self.output_dir / "processed" / "corpus_processed.csv"
            if processed_file.exists():
                df = pd.read_csv(processed_file)
            else:
                return {'error': 'No processed corpus found'}
                
        stats = {
            'total_items': len(df),
            'total_words': df['word_count'].sum(),
            'total_characters': df['text_length'].sum(),
            'avg_words_per_item': df['word_count'].mean(),
            'avg_chars_per_item': df['text_length'].mean(),
            'sources': df['source'].value_counts().to_dict(),
            'date_range': {
                'earliest': df['published'].min() if 'published' in df.columns else None,
                'latest': df['published'].max() if 'published' in df.columns else None
            }
        }
        
        return stats
        
    def filter_corpus(self, df: pd.DataFrame, 
                     min_words: int = 10,
                     max_words: int = None,
                     sources: List[str] = None,
                     keywords: List[str] = None) -> pd.DataFrame:
        """
        Filter corpus based on criteria.
        
        Args:
            df: Corpus DataFrame
            min_words: Minimum word count
            max_words: Maximum word count
            sources: List of sources to include
            keywords: Keywords that must be present
            
        Returns:
            Filtered DataFrame
        """
        filtered_df = df.copy()
        
        # Filter by word count
        if min_words:
            filtered_df = filtered_df[filtered_df['word_count'] >= min_words]
            
        if max_words:
            filtered_df = filtered_df[filtered_df['word_count'] <= max_words]
            
        # Filter by sources
        if sources:
            filtered_df = filtered_df[filtered_df['source'].isin(sources)]
            
        # Filter by keywords
        if keywords:
            keyword_mask = filtered_df['text'].str.contains('|'.join(keywords), case=False, na=False)
            filtered_df = filtered_df[keyword_mask]
            
        return filtered_df
