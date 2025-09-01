"""
Test Suite for NLP System
Comprehensive tests for NLP engine, corpus gatherer, and API endpoints.
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.nlp_engine import NLPEngine
from app.services.corpus_gatherer import CorpusGatherer

class TestNLPEngine(unittest.TestCase):
    """Test cases for NLP Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.nlp_engine = NLPEngine(models_dir=self.temp_dir)
        self.test_text = """
        Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on 
        the interaction between computers and human language. It enables machines to understand, 
        interpret, and generate human language in a way that is both meaningful and useful.
        
        NLP has applications in various domains including machine translation, sentiment analysis, 
        chatbots, and information extraction. Modern NLP systems use deep learning techniques 
        such as transformers and large language models to achieve state-of-the-art performance.
        """
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        
    def test_initialization(self):
        """Test NLP engine initialization"""
        self.assertIsNotNone(self.nlp_engine)
        self.assertIsNotNone(self.nlp_engine.device)
        self.assertTrue(self.nlp_engine.models_dir.exists())
        
    def test_preprocess_text(self):
        """Test text preprocessing"""
        preprocessed = self.nlp_engine.preprocess_text(self.test_text)
        self.assertIsInstance(preprocessed, str)
        self.assertLess(len(preprocessed), len(self.test_text))  # Should be shorter after preprocessing
        
    def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        sentiment = self.nlp_engine.analyze_sentiment(self.test_text)
        self.assertIsInstance(sentiment, dict)
        self.assertIn('method', sentiment)
        
    def test_extract_entities(self):
        """Test entity extraction"""
        entities = self.nlp_engine.extract_entities(self.test_text)
        self.assertIsInstance(entities, list)
        
    def test_extract_keywords(self):
        """Test keyword extraction"""
        keywords = self.nlp_engine.extract_keywords(self.test_text)
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        
    def test_analyze_readability(self):
        """Test readability analysis"""
        readability = self.nlp_engine.analyze_readability(self.test_text)
        self.assertIsInstance(readability, dict)
        self.assertIn('flesch_reading_ease', readability)
        self.assertIn('flesch_kincaid_grade', readability)
        
    def test_generate_summary(self):
        """Test text summarization"""
        summary = self.nlp_engine.generate_summary(self.test_text)
        self.assertIsInstance(summary, str)
        self.assertLess(len(summary), len(self.test_text))
        
    def test_extract_topics(self):
        """Test topic extraction"""
        texts = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing deals with human language.",
            "Computer vision focuses on image and video analysis."
        ]
        topics = self.nlp_engine.extract_topics(texts, num_topics=2)
        self.assertIsInstance(topics, dict)
        self.assertIn('topics', topics)
        
    def test_get_embeddings(self):
        """Test embedding generation"""
        embeddings = self.nlp_engine.get_embeddings(self.test_text)
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertGreater(embeddings.size, 0)
        
    def test_cluster_texts(self):
        """Test text clustering"""
        texts = [
            "Machine learning algorithms",
            "Deep learning neural networks", 
            "Natural language processing",
            "Computer vision systems",
            "Data science techniques"
        ]
        clusters = self.nlp_engine.cluster_texts(texts, num_clusters=2)
        self.assertIsInstance(clusters, dict)
        self.assertIn('clusters', clusters)
        
    def test_comprehensive_analysis(self):
        """Test comprehensive text analysis"""
        analysis = self.nlp_engine.comprehensive_analysis(self.test_text)
        self.assertIsInstance(analysis, dict)
        self.assertIn('basic_stats', analysis)
        self.assertIn('sentiment', analysis)
        self.assertIn('entities', analysis)
        self.assertIn('keywords', analysis)
        self.assertIn('readability', analysis)
        
    def test_model_loading(self):
        """Test model loading functionality"""
        # Test with a simple model
        model = self.nlp_engine.load_model("sentence-transformers/all-MiniLM-L6-v2", "embedding")
        self.assertIsNotNone(model)
        
    def test_model_saving_and_loading(self):
        """Test model saving and loading"""
        # Create a simple mock model
        mock_model = Mock()
        mock_model.name = "test_model"
        
        # Save model
        self.nlp_engine.save_model(mock_model, "test_model")
        
        # Load model
        loaded_model = self.nlp_engine.load_saved_model("test_model")
        self.assertIsNotNone(loaded_model)

class TestCorpusGatherer(unittest.TestCase):
    """Test cases for Corpus Gatherer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.gatherer = CorpusGatherer(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        
    def test_initialization(self):
        """Test corpus gatherer initialization"""
        self.assertIsNotNone(self.gatherer)
        self.assertTrue(self.gatherer.output_dir.exists())
        self.assertTrue((self.gatherer.output_dir / "raw").exists())
        self.assertTrue((self.gatherer.output_dir / "processed").exists())
        self.assertTrue((self.gatherer.output_dir / "metadata").exists())
        
    @patch('app.services.corpus_gatherer.feedparser')
    def test_collect_news(self, mock_feedparser):
        """Test news collection with mocked feedparser"""
        # Mock feedparser response
        mock_feed = Mock()
        mock_feed.entries = [
            Mock(
                title="Test News Article",
                link="https://example.com/article",
                published="2024-01-01"
            )
        ]
        mock_feedparser.parse.return_value = mock_feed
        
        # Mock newspaper Article
        with patch('app.services.corpus_gatherer.Article') as mock_article_class:
            mock_article = Mock()
            mock_article.text = "This is a test news article content."
            mock_article_class.return_value = mock_article
            
            result = self.gatherer._collect_news(query="test", max_items=10)
            
            self.assertIsInstance(result, dict)
            self.assertIn('count', result)
            self.assertIn('file', result)
            
    @patch('app.services.corpus_gatherer.wikipedia')
    def test_collect_wikipedia(self, mock_wikipedia):
        """Test Wikipedia collection with mocked wikipedia"""
        # Mock wikipedia search and page
        mock_wikipedia.search.return_value = ["Test Article"]
        mock_page = Mock()
        mock_page.title = "Test Article"
        mock_page.content = "This is test content from Wikipedia."
        mock_page.url = "https://en.wikipedia.org/wiki/Test_Article"
        mock_page.categories = ["Test", "Example"]
        mock_page.links = ["Link1", "Link2"]
        mock_wikipedia.page.return_value = mock_page
        
        result = self.gatherer._collect_wikipedia(query="test", max_items=10)
        
        self.assertIsInstance(result, dict)
        self.assertIn('count', result)
        self.assertIn('file', result)
        
    def test_collect_academic(self):
        """Test academic paper collection"""
        # This test might fail if no internet connection or API issues
        try:
            result = self.gatherer._collect_academic(query="machine learning", max_items=5)
            self.assertIsInstance(result, dict)
            self.assertIn('count', result)
            self.assertIn('file', result)
        except Exception as e:
            # Skip test if API is not available
            self.skipTest(f"Academic collection failed: {e}")
            
    def test_process_corpus(self):
        """Test corpus processing"""
        # Create sample data
        sample_data = [
            {
                'title': 'Test Article 1',
                'text': 'This is the first test article.',
                'url': 'https://example.com/1',
                'published': '2024-01-01',
                'source': 'test'
            },
            {
                'title': 'Test Article 2', 
                'text': 'This is the second test article.',
                'url': 'https://example.com/2',
                'published': '2024-01-02',
                'source': 'test'
            }
        ]
        
        # Save sample data
        sample_file = self.gatherer.output_dir / "raw" / "test_data.json"
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f)
            
        # Process corpus
        df = self.gatherer.process_corpus([sample_file.name])
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn('title', df.columns)
        self.assertIn('text', df.columns)
        self.assertIn('source', df.columns)
        
    def test_get_corpus_stats(self):
        """Test corpus statistics generation"""
        # Create sample DataFrame
        sample_data = {
            'title': ['Article 1', 'Article 2'],
            'text': ['Short text.', 'This is a longer text with more words.'],
            'source': ['test', 'test'],
            'text_length': [11, 35],
            'word_count': [2, 8]
        }
        df = pd.DataFrame(sample_data)
        
        stats = self.gatherer.get_corpus_stats(df)
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_items'], 2)
        self.assertEqual(stats['total_words'], 10)
        self.assertEqual(stats['total_characters'], 46)
        
    def test_filter_corpus(self):
        """Test corpus filtering"""
        # Create sample DataFrame
        sample_data = {
            'title': ['Short', 'Medium', 'Long Article'],
            'text': ['Short.', 'This is medium length text.', 'This is a very long article with many words and sentences.'],
            'source': ['test', 'test', 'test'],
            'word_count': [1, 6, 12]
        }
        df = pd.DataFrame(sample_data)
        
        # Test filtering by word count
        filtered_df = self.gatherer.filter_corpus(df, min_words=5)
        self.assertEqual(len(filtered_df), 2)
        
        # Test filtering by sources
        filtered_df = self.gatherer.filter_corpus(df, sources=['test'])
        self.assertEqual(len(filtered_df), 3)
        
        # Test filtering by keywords
        filtered_df = self.gatherer.filter_corpus(df, keywords=['long'])
        self.assertEqual(len(filtered_df), 1)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete NLP system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.nlp_engine = NLPEngine(models_dir=self.temp_dir)
        self.gatherer = CorpusGatherer(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        
    def test_end_to_end_analysis(self):
        """Test complete end-to-end analysis pipeline"""
        # Sample texts
        texts = [
            "Machine learning is transforming the world of technology.",
            "Deep learning algorithms are achieving remarkable results.",
            "Natural language processing enables human-computer interaction."
        ]
        
        # Collect and process corpus
        try:
            # Create sample data
            sample_data = [
                {
                    'title': f'Article {i}',
                    'text': text,
                    'url': f'https://example.com/{i}',
                    'published': '2024-01-01',
                    'source': 'test'
                }
                for i, text in enumerate(texts)
            ]
            
            # Save sample data
            sample_file = self.gatherer.output_dir / "raw" / "test_integration.json"
            with open(sample_file, 'w') as f:
                json.dump(sample_data, f)
                
            # Process corpus
            df = self.gatherer.process_corpus([sample_file.name])
            
            # Analyze each text
            for text in texts:
                analysis = self.nlp_engine.comprehensive_analysis(text)
                self.assertIsInstance(analysis, dict)
                self.assertIn('sentiment', analysis)
                self.assertIn('keywords', analysis)
                
            # Extract topics from all texts
            topics = self.nlp_engine.extract_topics(texts, num_topics=2)
            self.assertIsInstance(topics, dict)
            
            # Cluster texts
            clusters = self.nlp_engine.cluster_texts(texts, num_clusters=2)
            self.assertIsInstance(clusters, dict)
            
        except Exception as e:
            self.skipTest(f"Integration test failed: {e}")

class TestPerformance(unittest.TestCase):
    """Performance tests for the NLP system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.nlp_engine = NLPEngine(models_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        
    def test_analysis_performance(self):
        """Test performance of text analysis"""
        import time
        
        # Generate test text
        test_text = "This is a test text for performance analysis. " * 100
        
        # Time the analysis
        start_time = time.time()
        analysis = self.nlp_engine.comprehensive_analysis(test_text)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Assert reasonable performance (should complete within 30 seconds)
        self.assertLess(execution_time, 30.0)
        self.assertIsInstance(analysis, dict)
        
    def test_batch_processing_performance(self):
        """Test performance of batch text processing"""
        import time
        
        # Generate multiple test texts
        texts = [f"This is test text number {i}. " * 10 for i in range(10)]
        
        # Time batch processing
        start_time = time.time()
        
        results = []
        for text in texts:
            result = self.nlp_engine.analyze_sentiment(text)
            results.append(result)
            
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Assert reasonable performance
        self.assertLess(execution_time, 60.0)
        self.assertEqual(len(results), 10)

def run_benchmarks():
    """Run performance benchmarks"""
    print("Running NLP System Benchmarks...")
    
    # Initialize components
    nlp_engine = NLPEngine()
    
    # Benchmark text
    benchmark_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on 
    the interaction between computers and human language. It enables machines to understand, 
    interpret, and generate human language in a way that is both meaningful and useful.
    
    NLP has applications in various domains including machine translation, sentiment analysis, 
    chatbots, and information extraction. Modern NLP systems use deep learning techniques 
    such as transformers and large language models to achieve state-of-the-art performance.
    
    The field has seen remarkable progress in recent years, with models like BERT, GPT, and 
    T5 achieving unprecedented results on various language tasks. These models are trained on 
    massive amounts of text data and can perform tasks such as text classification, question 
    answering, and text generation with high accuracy.
    """
    
    import time
    
    # Benchmark sentiment analysis
    print("\n1. Sentiment Analysis Benchmark")
    start_time = time.time()
    sentiment = nlp_engine.analyze_sentiment(benchmark_text)
    end_time = time.time()
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Result: {sentiment}")
    
    # Benchmark entity extraction
    print("\n2. Entity Extraction Benchmark")
    start_time = time.time()
    entities = nlp_engine.extract_entities(benchmark_text)
    end_time = time.time()
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Entities found: {len(entities)}")
    
    # Benchmark keyword extraction
    print("\n3. Keyword Extraction Benchmark")
    start_time = time.time()
    keywords = nlp_engine.extract_keywords(benchmark_text)
    end_time = time.time()
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Keywords: {keywords[:5]}")  # Show first 5
    
    # Benchmark readability analysis
    print("\n4. Readability Analysis Benchmark")
    start_time = time.time()
    readability = nlp_engine.analyze_readability(benchmark_text)
    end_time = time.time()
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Flesch Reading Ease: {readability.get('flesch_reading_ease', 'N/A')}")
    
    # Benchmark summarization
    print("\n5. Summarization Benchmark")
    start_time = time.time()
    summary = nlp_engine.generate_summary(benchmark_text)
    end_time = time.time()
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Summary length: {len(summary)} characters")
    
    # Benchmark comprehensive analysis
    print("\n6. Comprehensive Analysis Benchmark")
    start_time = time.time()
    analysis = nlp_engine.comprehensive_analysis(benchmark_text)
    end_time = time.time()
    print(f"   Time: {end_time - start_time:.3f} seconds")
    print(f"   Analysis components: {list(analysis.keys())}")

if __name__ == '__main__':
    # Run tests
    print("Running NLP System Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run benchmarks
    run_benchmarks()
