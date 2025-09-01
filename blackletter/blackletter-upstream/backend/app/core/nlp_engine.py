"""
NLP Engine - Core Natural Language Processing Module
Provides comprehensive text analysis, processing, and model management capabilities.
"""

import logging
import os
from typing import Dict, List, Optional, Tuple, Any, Union
from pathlib import Path
import json
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
from transformers import (
    AutoTokenizer, AutoModel, pipeline, 
    TextClassificationPipeline, TokenClassificationPipeline,
    QuestionAnsweringPipeline, SummarizationPipeline
)
import torch
from sentence_transformers import SentenceTransformer
import spacy
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.cluster import KMeans
import gensim
from gensim import corpora, models
from keybert import KeyBERT
import textstat
from readability import Readability
import textacy
from textacy import extract
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from rake_nltk import Rake

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPEngine:
    """
    Comprehensive NLP Engine providing text analysis, processing, and model management.
    """
    
    def __init__(self, models_dir: str = "models", device: str = "auto"):
        """
        Initialize the NLP Engine.
        
        Args:
            models_dir: Directory to store/load models
            device: Device to use for models ('cpu', 'cuda', or 'auto')
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Set device
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Using device: {self.device}")
        
        # Initialize components
        self._initialize_nltk()
        self._initialize_spacy()
        self._initialize_models()
        
        # Cache for loaded models
        self.model_cache = {}
        
    def _initialize_nltk(self):
        """Initialize NLTK components."""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            self.stemmer = PorterStemmer()
            
        except Exception as e:
            logger.warning(f"Failed to initialize NLTK: {e}")
            
    def _initialize_spacy(self):
        """Initialize spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.info("Downloading spaCy model...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            
    def _initialize_models(self):
        """Initialize default models."""
        self.default_models = {
            'sentiment': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
            'emotion': 'j-hartmann/emotion-english-distilroberta-base',
            'ner': 'dslim/bert-base-NER',
            'summarization': 'facebook/bart-large-cnn',
            'question_answering': 'deepset/roberta-base-squad2',
            'zero_shot': 'facebook/bart-large-mnli',
            'embedding': 'sentence-transformers/all-MiniLM-L6-v2'
        }
        
    def load_model(self, model_name: str, task: str = None) -> Any:
        """
        Load a model from cache or download.
        
        Args:
            model_name: Name of the model to load
            task: Specific task for the model
            
        Returns:
            Loaded model
        """
        cache_key = f"{model_name}_{task}" if task else model_name
        
        if cache_key in self.model_cache:
            return self.model_cache[cache_key]
            
        try:
            if task == "sentiment":
                model = pipeline("sentiment-analysis", model=model_name, device=self.device)
            elif task == "ner":
                model = pipeline("ner", model=model_name, device=self.device)
            elif task == "summarization":
                model = pipeline("summarization", model=model_name, device=self.device)
            elif task == "question-answering":
                model = pipeline("question-answering", model=model_name, device=self.device)
            elif task == "zero-shot":
                model = pipeline("zero-shot-classification", model=model_name, device=self.device)
            elif task == "embedding":
                model = SentenceTransformer(model_name, device=self.device)
            else:
                model = pipeline(task, model=model_name, device=self.device)
                
            self.model_cache[cache_key] = model
            return model
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return None
            
    def preprocess_text(self, text: str, 
                       remove_stopwords: bool = True,
                       lemmatize: bool = True,
                       stem: bool = False,
                       remove_punctuation: bool = True) -> str:
        """
        Preprocess text for analysis.
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stop words
            lemmatize: Whether to lemmatize words
            stem: Whether to stem words
            remove_punctuation: Whether to remove punctuation
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
            
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove punctuation
        if remove_punctuation:
            tokens = [token for token in tokens if token.isalnum()]
            
        # Remove stop words
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
            
        # Lemmatize
        if lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
            
        # Stem
        if stem:
            tokens = [self.stemmer.stem(token) for token in tokens]
            
        return " ".join(tokens)
        
    def analyze_sentiment(self, text: str, model_name: str = None) -> Dict[str, Any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Input text
            model_name: Model to use for sentiment analysis
            
        Returns:
            Sentiment analysis results
        """
        if not model_name:
            model_name = self.default_models['sentiment']
            
        model = self.load_model(model_name, "sentiment")
        
        if not model:
            # Fallback to TextBlob
            blob = TextBlob(text)
            return {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity,
                'method': 'textblob'
            }
            
        result = model(text)
        return {
            'label': result[0]['label'],
            'score': result[0]['score'],
            'method': 'transformer'
        }
        
    def extract_entities(self, text: str, model_name: str = None) -> List[Dict[str, Any]]:
        """
        Extract named entities from text.
        
        Args:
            text: Input text
            model_name: Model to use for NER
            
        Returns:
            List of extracted entities
        """
        if not model_name:
            model_name = self.default_models['ner']
            
        model = self.load_model(model_name, "ner")
        
        if not model:
            # Fallback to spaCy
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            return entities
            
        result = model(text)
        return result
        
    def generate_summary(self, text: str, max_length: int = 150, 
                        model_name: str = None) -> str:
        """
        Generate summary of text.
        
        Args:
            text: Input text
            max_length: Maximum length of summary
            model_name: Model to use for summarization
            
        Returns:
            Generated summary
        """
        if not model_name:
            model_name = self.default_models['summarization']
            
        model = self.load_model(model_name, "summarization")
        
        if not model:
            # Fallback to extractive summarization
            return self._extractive_summary(text, max_length)
            
        result = model(text, max_length=max_length, min_length=30, do_sample=False)
        return result[0]['summary_text']
        
    def _extractive_summary(self, text: str, max_length: int) -> str:
        """Generate extractive summary using sumy."""
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LexRankSummarizer()
            summary = summarizer(parser.document, 3)  # 3 sentences
            return " ".join([str(sentence) for sentence in summary])
        except:
            # Fallback to simple sentence selection
            sentences = sent_tokenize(text)
            return " ".join(sentences[:3])
            
    def extract_keywords(self, text: str, method: str = "keybert", 
                        top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords from text.
        
        Args:
            text: Input text
            method: Method to use ('keybert', 'rake', 'tfidf')
            top_k: Number of keywords to extract
            
        Returns:
            List of (keyword, score) tuples
        """
        if method == "keybert":
            model = KeyBERT()
            keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 2), 
                                           stop_words='english', top_k=top_k)
            return keywords
            
        elif method == "rake":
            rake = Rake()
            rake.extract_keywords_from_text(text)
            keywords = rake.get_ranked_phrases_with_scores()
            return [(phrase, score) for score, phrase in keywords[:top_k]]
            
        elif method == "tfidf":
            vectorizer = TfidfVectorizer(max_features=top_k, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            keywords = [(feature_names[i], scores[i]) for i in scores.argsort()[-top_k:][::-1]]
            return keywords
            
        return []
        
    def analyze_readability(self, text: str) -> Dict[str, Any]:
        """
        Analyze text readability metrics.
        
        Args:
            text: Input text
            
        Returns:
            Readability metrics
        """
        return {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'gunning_fog': textstat.gunning_fog(text),
            'smog_index': textstat.smog_index(text),
            'automated_readability_index': textstat.automated_readability_index(text),
            'coleman_liau_index': textstat.coleman_liau_index(text),
            'linsear_write_formula': textstat.linsear_write_formula(text),
            'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
            'difficult_words': textstat.difficult_words(text),
            'syllable_count': textstat.syllable_count(text),
            'lexicon_count': textstat.lexicon_count(text),
            'sentence_count': textstat.sentence_count(text)
        }
        
    def extract_topics(self, texts: List[str], num_topics: int = 5, 
                      method: str = "lda") -> Dict[str, Any]:
        """
        Extract topics from a collection of texts.
        
        Args:
            texts: List of input texts
            num_topics: Number of topics to extract
            method: Method to use ('lda', 'nmf', 'gensim')
            
        Returns:
            Topic extraction results
        """
        if method == "lda":
            vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            doc_term_matrix = vectorizer.fit_transform(texts)
            
            lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
            lda.fit(doc_term_matrix)
            
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            for topic_idx, topic in enumerate(lda.components_):
                top_words = [feature_names[i] for i in topic.argsort()[-10:][::-1]]
                topics.append({
                    'topic_id': topic_idx,
                    'words': top_words,
                    'weights': topic[topic.argsort()[-10:][::-1]].tolist()
                })
                
            return {
                'method': 'lda',
                'topics': topics,
                'model': lda
            }
            
        elif method == "gensim":
            # Preprocess texts
            processed_texts = [[word for word in text.lower().split() if word not in self.stop_words] 
                             for text in texts]
            
            # Create dictionary
            dictionary = corpora.Dictionary(processed_texts)
            corpus = [dictionary.doc2bow(text) for text in processed_texts]
            
            # Train LDA model
            lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, 
                                      passes=15, random_state=42)
            
            topics = []
            for topic_id in range(num_topics):
                topic_words = lda_model.show_topic(topic_id, 10)
                topics.append({
                    'topic_id': topic_id,
                    'words': [word for word, _ in topic_words],
                    'weights': [weight for _, weight in topic_words]
                })
                
            return {
                'method': 'gensim',
                'topics': topics,
                'model': lda_model
            }
            
        return {'method': method, 'topics': [], 'model': None}
        
    def get_embeddings(self, texts: Union[str, List[str]], 
                      model_name: str = None) -> np.ndarray:
        """
        Get embeddings for text(s).
        
        Args:
            texts: Input text or list of texts
            model_name: Model to use for embeddings
            
        Returns:
            Embeddings array
        """
        if not model_name:
            model_name = self.default_models['embedding']
            
        model = self.load_model(model_name, "embedding")
        
        if not model:
            # Fallback to TF-IDF
            vectorizer = TfidfVectorizer()
            if isinstance(texts, str):
                texts = [texts]
            return vectorizer.fit_transform(texts).toarray()
            
        if isinstance(texts, str):
            texts = [texts]
            
        embeddings = model.encode(texts)
        return embeddings
        
    def cluster_texts(self, texts: List[str], num_clusters: int = 5, 
                     method: str = "kmeans") -> Dict[str, Any]:
        """
        Cluster texts based on similarity.
        
        Args:
            texts: List of input texts
            num_clusters: Number of clusters
            method: Clustering method
            
        Returns:
            Clustering results
        """
        # Get embeddings
        embeddings = self.get_embeddings(texts)
        
        if method == "kmeans":
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(embeddings)
            
            # Group texts by cluster
            clusters = {}
            for i, label in enumerate(cluster_labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(texts[i])
                
            return {
                'method': 'kmeans',
                'clusters': clusters,
                'labels': cluster_labels.tolist(),
                'centroids': kmeans.cluster_centers_.tolist()
            }
            
        return {'method': method, 'clusters': {}, 'labels': [], 'centroids': []}
        
    def comprehensive_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive text analysis.
        
        Args:
            text: Input text
            
        Returns:
            Comprehensive analysis results
        """
        return {
            'basic_stats': {
                'char_count': len(text),
                'word_count': len(text.split()),
                'sentence_count': len(sent_tokenize(text)),
                'avg_word_length': np.mean([len(word) for word in text.split()])
            },
            'sentiment': self.analyze_sentiment(text),
            'entities': self.extract_entities(text),
            'keywords': self.extract_keywords(text),
            'readability': self.analyze_readability(text),
            'summary': self.generate_summary(text),
            'preprocessed': self.preprocess_text(text)
        }
        
    def save_model(self, model: Any, name: str):
        """Save a model to disk."""
        model_path = self.models_dir / f"{name}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {model_path}")
        
    def load_saved_model(self, name: str) -> Any:
        """Load a saved model from disk."""
        model_path = self.models_dir / f"{name}.pkl"
        if model_path.exists():
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded from {model_path}")
            return model
        return None
