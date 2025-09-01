#!/usr/bin/env python3
"""
Quick Start NLP System
A demonstration script to get you started with the NLP system quickly.
"""

import sys
import os
from pathlib import Path
import json
import time
from typing import Optional

from app.core.nlp_engine import NLPEngine

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n--- {title} ---")


def load_model(model_name: str = "gpt2", task: Optional[str] = None):
    """Load an NLP model using the system's NLPEngine.

    This helper exposes model loading for tests and scripts while keeping the
    quick start example self-contained.

    Args:
        model_name: Name of the model to load.
        task: Optional task the model should perform.

    Returns:
        An object implementing the generation interface.
    """

    engine = NLPEngine()
    return engine.load_model(model_name, task)

def main():
    """Main quick start demonstration"""
    print_header("NLP System Quick Start")
    
    print("This script will demonstrate the key features of the NLP system.")
    print("Make sure you have installed all dependencies first:")
    print("  pip install -r requirements.txt")
    
    input("\nPress Enter to continue...")
    
    try:
        # Import components
        print_section("Importing Components")
        print("Importing NLP Engine...")
        from app.core.nlp_engine import NLPEngine
        
        print("Importing Corpus Gatherer...")
        from app.services.corpus_gatherer import CorpusGatherer
        
        print("✅ All components imported successfully!")
        
        # Initialize NLP Engine
        print_section("Initializing NLP Engine")
        print("Initializing NLP Engine (this may take a moment for first run)...")
        start_time = time.time()
        nlp_engine = NLPEngine()
        init_time = time.time() - start_time
        print(f"✅ NLP Engine initialized in {init_time:.2f} seconds")
        print(f"   Device: {nlp_engine.device}")
        
        # Demo text analysis
        print_section("Text Analysis Demo")
        
        demo_text = """
        Natural Language Processing (NLP) is a fascinating field of artificial intelligence 
        that focuses on the interaction between computers and human language. It enables 
        machines to understand, interpret, and generate human language in meaningful ways.
        
        The applications of NLP are vast and include machine translation, sentiment analysis, 
        chatbots, information extraction, and much more. Modern NLP systems use advanced 
        deep learning techniques such as transformers and large language models to achieve 
        remarkable performance on various language tasks.
        
        Companies like Google, Microsoft, and OpenAI have made significant contributions 
        to the field, developing models like BERT, GPT, and T5 that have revolutionized 
        how we approach natural language understanding and generation.
        """
        
        print("Analyzing sample text...")
        print(f"Text length: {len(demo_text)} characters")
        
        # Sentiment Analysis
        print("\n1. Sentiment Analysis:")
        sentiment = nlp_engine.analyze_sentiment(demo_text)
        print(f"   Result: {sentiment}")
        
        # Entity Extraction
        print("\n2. Entity Extraction:")
        entities = nlp_engine.extract_entities(demo_text)
        print(f"   Found {len(entities)} entities:")
        for entity in entities[:5]:  # Show first 5
            print(f"   - {entity.get('text', 'N/A')} ({entity.get('label', 'N/A')})")
        
        # Keyword Extraction
        print("\n3. Keyword Extraction:")
        keywords = nlp_engine.extract_keywords(demo_text, top_k=8)
        print("   Top keywords:")
        for keyword, score in keywords:
            print(f"   - {keyword}: {score:.3f}")
        
        # Readability Analysis
        print("\n4. Readability Analysis:")
        readability = nlp_engine.analyze_readability(demo_text)
        print(f"   Flesch Reading Ease: {readability['flesch_reading_ease']:.1f}")
        print(f"   Grade Level: {readability['flesch_kincaid_grade']:.1f}")
        print(f"   Gunning Fog Index: {readability['gunning_fog']:.1f}")
        
        # Text Summarization
        print("\n5. Text Summarization:")
        summary = nlp_engine.generate_summary(demo_text, max_length=100)
        print(f"   Summary: {summary}")
        
        # Comprehensive Analysis
        print("\n6. Comprehensive Analysis:")
        print("   Running comprehensive analysis...")
        analysis = nlp_engine.comprehensive_analysis(demo_text)
        print(f"   Analysis completed with {len(analysis)} components")
        
        # Topic Modeling Demo
        print_section("Topic Modeling Demo")
        
        documents = [
            "Machine learning algorithms are transforming various industries.",
            "Deep learning neural networks achieve remarkable accuracy in image recognition.",
            "Natural language processing enables human-computer interaction through text.",
            "Computer vision systems can identify and classify objects in images.",
            "Data science techniques help extract valuable insights from large datasets.",
            "Artificial intelligence is revolutionizing healthcare and medical diagnosis.",
            "Robotics and automation are changing manufacturing processes worldwide.",
            "Big data analytics provide unprecedented understanding of user behavior."
        ]
        
        print(f"Analyzing {len(documents)} documents for topics...")
        topics = nlp_engine.extract_topics(documents, num_topics=3, method="lda")
        
        print("Extracted topics:")
        for i, topic in enumerate(topics['topics']):
            print(f"   Topic {i+1}: {', '.join(topic['words'][:5])}")
        
        # Text Clustering Demo
        print_section("Text Clustering Demo")
        
        print("Clustering documents by similarity...")
        clusters = nlp_engine.cluster_texts(documents, num_clusters=3, method="kmeans")
        
        print("Clustering results:")
        for cluster_id, texts in clusters['clusters'].items():
            print(f"   Cluster {cluster_id}: {len(texts)} documents")
            print(f"     Sample: {texts[0][:50]}...")
        
        # Corpus Collection Demo
        print_section("Corpus Collection Demo")
        
        print("Initializing corpus gatherer...")
        gatherer = CorpusGatherer(output_dir="demo_corpus")
        
        print("Available sources:")
        for source in gatherer.collectors.keys():
            print(f"   - {source}")
        
        # Create sample corpus data
        print("\nCreating sample corpus data...")
        sample_data = [
            {
                'title': 'Introduction to Machine Learning',
                'text': 'Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models.',
                'url': 'https://example.com/ml-intro',
                'published': '2024-01-01',
                'source': 'demo'
            },
            {
                'title': 'Deep Learning Fundamentals',
                'text': 'Deep learning uses neural networks with multiple layers to learn complex patterns in data.',
                'url': 'https://example.com/dl-fundamentals',
                'published': '2024-01-02',
                'source': 'demo'
            },
            {
                'title': 'Natural Language Processing Overview',
                'text': 'NLP combines computational linguistics with machine learning to process human language.',
                'url': 'https://example.com/nlp-overview',
                'published': '2024-01-03',
                'source': 'demo'
            }
        ]
        
        # Save sample data
        sample_file = gatherer.output_dir / "raw" / "demo_data.json"
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f)
        
        print(f"✅ Sample data saved to {sample_file}")
        
        # Process corpus
        print("\nProcessing corpus...")
        df = gatherer.process_corpus([sample_file.name])
        
        print(f"✅ Corpus processed: {len(df)} items")
        
        # Get corpus statistics
        stats = gatherer.get_corpus_stats(df)
        print(f"   Total words: {stats['total_words']}")
        print(f"   Average words per item: {stats['avg_words_per_item']:.1f}")
        
        # API Demo
        print_section("API Endpoints Demo")
        
        print("The NLP system provides REST API endpoints:")
        print("   POST /api/nlp/analyze - Comprehensive text analysis")
        print("   POST /api/nlp/sentiment - Sentiment analysis")
        print("   POST /api/nlp/entities - Entity extraction")
        print("   POST /api/nlp/keywords - Keyword extraction")
        print("   POST /api/nlp/summary - Text summarization")
        print("   POST /api/nlp/topics - Topic extraction")
        print("   POST /api/nlp/cluster - Text clustering")
        print("   POST /api/nlp/corpus/collect - Corpus collection")
        print("   GET /api/nlp/corpus/stats - Corpus statistics")
        print("   GET /api/nlp/health - Health check")
        
        # CLI Demo
        print_section("Command Line Interface Demo")
        
        print("The system also provides a comprehensive CLI:")
        print("   python scripts/nlp_cli.py analyze text 'Your text here'")
        print("   python scripts/nlp_cli.py corpus collect --sources news wikipedia")
        print("   python scripts/nlp_cli.py demo")
        print("   python scripts/nlp_cli.py info")
        
        # Performance Demo
        print_section("Performance Demo")
        
        print("Testing performance with larger text...")
        large_text = demo_text * 5  # 5x larger
        
        start_time = time.time()
        large_analysis = nlp_engine.comprehensive_analysis(large_text)
        end_time = time.time()
        
        print(f"✅ Analysis completed in {end_time - start_time:.2f} seconds")
        print(f"   Text size: {len(large_text)} characters")
        print(f"   Processing speed: {len(large_text)/(end_time - start_time):.0f} chars/second")
        
        # Next Steps
        print_section("Next Steps")
        
        print("To continue exploring the NLP system:")
        print("1. Run the CLI demo: python scripts/nlp_cli.py demo")
        print("2. Try the API: Start the server and visit /docs")
        print("3. Run tests: python tests/test_nlp_system.py")
        print("4. Read documentation: NLP_SYSTEM_README.md")
        print("5. Collect real data: python scripts/nlp_cli.py corpus collect")
        
        print_header("Quick Start Complete!")
        print("🎉 Congratulations! You've successfully explored the NLP system.")
        print("The system is ready for your text analysis and corpus collection needs.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Please check the error and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
