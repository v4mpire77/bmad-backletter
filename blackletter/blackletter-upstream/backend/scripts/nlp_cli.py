#!/usr/bin/env python3
"""
NLP CLI - Command Line Interface for NLP Operations
Provides easy-to-use commands for text analysis, corpus collection, and model management.
"""

import click
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.core.nlp_engine import NLPEngine
from app.services.corpus_gatherer import CorpusGatherer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """NLP Command Line Interface - Text Analysis and Corpus Management"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

@cli.group()
def analyze():
    """Text analysis commands"""
    pass

@analyze.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Input text file')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
@click.option('--types', '-t', multiple=True, 
              default=['sentiment', 'entities', 'keywords', 'readability'],
              help='Types of analysis to perform')
def text(text, file, output, types):
    """Analyze text with comprehensive NLP techniques"""
    console.print(Panel.fit("🔍 Text Analysis", style="bold blue"))
    
    # Get input text
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            input_text = f.read()
    elif text:
        input_text = text
    else:
        input_text = click.edit()
        if not input_text:
            console.print("❌ No text provided", style="red")
            return
    
    # Initialize NLP engine
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Initializing NLP engine...", total=None)
        nlp_engine = NLPEngine()
        progress.update(task, description="Analyzing text...")
        
        # Perform analysis
        results = {}
        for analysis_type in types:
            try:
                if analysis_type == 'sentiment':
                    results['sentiment'] = nlp_engine.analyze_sentiment(input_text)
                elif analysis_type == 'entities':
                    results['entities'] = nlp_engine.extract_entities(input_text)
                elif analysis_type == 'keywords':
                    results['keywords'] = nlp_engine.extract_keywords(input_text)
                elif analysis_type == 'readability':
                    results['readability'] = nlp_engine.analyze_readability(input_text)
                elif analysis_type == 'summary':
                    results['summary'] = nlp_engine.generate_summary(input_text)
                elif analysis_type == 'comprehensive':
                    results = nlp_engine.comprehensive_analysis(input_text)
                    break
            except Exception as e:
                console.print(f"❌ Error in {analysis_type} analysis: {e}", style="red")
    
    # Display results
    display_analysis_results(results, input_text)
    
    # Save results if output specified
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        console.print(f"💾 Results saved to {output}", style="green")

def display_analysis_results(results, text):
    """Display analysis results in a formatted table"""
    console.print(f"\n📊 Analysis Results for {len(text)} characters")
    
    # Basic stats
    stats_table = Table(title="Text Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    
    stats_table.add_row("Characters", str(len(text)))
    stats_table.add_row("Words", str(len(text.split())))
    stats_table.add_row("Sentences", str(len(text.split('.'))))
    
    console.print(stats_table)
    
    # Sentiment
    if 'sentiment' in results:
        sentiment = results['sentiment']
        console.print(f"\n😊 Sentiment: {sentiment.get('label', 'N/A')} "
                     f"(confidence: {sentiment.get('score', 0):.3f})")
    
    # Keywords
    if 'keywords' in results:
        keywords_table = Table(title="Top Keywords")
        keywords_table.add_column("Keyword", style="cyan")
        keywords_table.add_column("Score", style="magenta")
        
        for keyword, score in results['keywords'][:10]:
            keywords_table.add_row(keyword, f"{score:.3f}")
        
        console.print(keywords_table)
    
    # Entities
    if 'entities' in results:
        entities_table = Table(title="Named Entities")
        entities_table.add_column("Entity", style="cyan")
        entities_table.add_column("Type", style="magenta")
        entities_table.add_column("Confidence", style="green")
        
        for entity in results['entities'][:10]:
            entities_table.add_row(
                entity.get('text', ''),
                entity.get('label', ''),
                f"{entity.get('score', 0):.3f}"
            )
        
        console.print(entities_table)
    
    # Readability
    if 'readability' in results:
        readability = results['readability']
        console.print(f"\n📖 Readability Score: {readability.get('flesch_reading_ease', 0):.1f}")
        console.print(f"📚 Grade Level: {readability.get('flesch_kincaid_grade', 0):.1f}")

@cli.group()
def corpus():
    """Corpus management commands"""
    pass

@corpus.command()
@click.option('--sources', '-s', multiple=True, 
              default=['news', 'wikipedia', 'academic'],
              help='Sources to collect from')
@click.option('--query', '-q', help='Search query')
@click.option('--max-items', '-m', default=100, help='Maximum items per source')
@click.option('--output-dir', '-o', default='corpus_data', help='Output directory')
@click.option('--date-from', help='Start date (YYYY-MM-DD)')
@click.option('--date-to', help='End date (YYYY-MM-DD)')
def collect(sources, query, max_items, output_dir, date_from, date_to):
    """Collect corpus data from various sources"""
    console.print(Panel.fit("📚 Corpus Collection", style="bold green"))
    
    console.print(f"🎯 Sources: {', '.join(sources)}")
    if query:
        console.print(f"🔍 Query: {query}")
    console.print(f"📊 Max items per source: {max_items}")
    
    # Initialize corpus gatherer
    gatherer = CorpusGatherer(output_dir=output_dir)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Collecting corpus data...", total=None)
        
        try:
            results = gatherer.collect_corpus(
                sources=list(sources),
                query=query,
                max_items=max_items,
                date_from=date_from,
                date_to=date_to
            )
            
            progress.update(task, description="Collection completed!")
            
        except Exception as e:
            console.print(f"❌ Error during collection: {e}", style="red")
            return
    
    # Display results
    display_collection_results(results)

def display_collection_results(results):
    """Display corpus collection results"""
    console.print(f"\n✅ Collection completed!")
    console.print(f"📊 Total items: {results['total_items']}")
    
    results_table = Table(title="Collection Results by Source")
    results_table.add_column("Source", style="cyan")
    results_table.add_column("Items", style="magenta")
    results_table.add_column("Status", style="green")
    
    for source, result in results['sources'].items():
        if 'error' in result:
            status = f"❌ {result['error']}"
            items = 0
        else:
            status = "✅ Success"
            items = result.get('count', 0)
        
        results_table.add_row(source, str(items), status)
    
    console.print(results_table)

@corpus.command()
@click.option('--input-files', '-i', multiple=True, help='Input files to process')
@click.option('--output-dir', '-o', default='corpus_data', help='Output directory')
def process(input_files, output_dir):
    """Process collected corpus data"""
    console.print(Panel.fit("⚙️ Corpus Processing", style="bold yellow"))
    
    gatherer = CorpusGatherer(output_dir=output_dir)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Processing corpus data...", total=None)
        
        try:
            df = gatherer.process_corpus(input_files if input_files else None)
            progress.update(task, description="Processing completed!")
            
        except Exception as e:
            console.print(f"❌ Error during processing: {e}", style="red")
            return
    
    # Display stats
    stats = gatherer.get_corpus_stats(df)
    display_corpus_stats(stats)

def display_corpus_stats(stats):
    """Display corpus statistics"""
    if 'error' in stats:
        console.print(f"❌ {stats['error']}", style="red")
        return
    
    console.print(f"\n📊 Corpus Statistics")
    
    stats_table = Table(title="Corpus Overview")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    
    stats_table.add_row("Total Items", str(stats['total_items']))
    stats_table.add_row("Total Words", f"{stats['total_words']:,}")
    stats_table.add_row("Total Characters", f"{stats['total_characters']:,}")
    stats_table.add_row("Avg Words/Item", f"{stats['avg_words_per_item']:.1f}")
    stats_table.add_row("Avg Chars/Item", f"{stats['avg_chars_per_item']:.1f}")
    
    console.print(stats_table)
    
    # Source distribution
    if 'sources' in stats:
        sources_table = Table(title="Items by Source")
        sources_table.add_column("Source", style="cyan")
        sources_table.add_column("Count", style="magenta")
        sources_table.add_column("Percentage", style="green")
        
        total = stats['total_items']
        for source, count in stats['sources'].items():
            percentage = (count / total * 100) if total > 0 else 0
            sources_table.add_row(source, str(count), f"{percentage:.1f}%")
        
        console.print(sources_table)

@corpus.command()
@click.option('--min-words', default=10, help='Minimum word count')
@click.option('--max-words', help='Maximum word count')
@click.option('--sources', multiple=True, help='Sources to include')
@click.option('--keywords', multiple=True, help='Keywords that must be present')
@click.option('--output', '-o', help='Output file for filtered data')
def filter(min_words, max_words, sources, keywords, output):
    """Filter corpus based on criteria"""
    console.print(Panel.fit("🔍 Corpus Filtering", style="bold purple"))
    
    gatherer = CorpusGatherer()
    
    # Load processed corpus
    processed_file = gatherer.output_dir / "processed" / "corpus_processed.csv"
    if not processed_file.exists():
        console.print("❌ No processed corpus found. Run 'corpus process' first.", style="red")
        return
    
    df = pd.read_csv(processed_file)
    console.print(f"📊 Original corpus: {len(df)} items")
    
    # Apply filters
    filtered_df = gatherer.filter_corpus(
        df, min_words, max_words, 
        list(sources) if sources else None,
        list(keywords) if keywords else None
    )
    
    console.print(f"✅ Filtered corpus: {len(filtered_df)} items")
    
    # Display filter criteria
    criteria_table = Table(title="Filter Criteria")
    criteria_table.add_column("Criterion", style="cyan")
    criteria_table.add_column("Value", style="magenta")
    
    criteria_table.add_row("Min Words", str(min_words))
    if max_words:
        criteria_table.add_row("Max Words", str(max_words))
    if sources:
        criteria_table.add_row("Sources", ", ".join(sources))
    if keywords:
        criteria_table.add_row("Keywords", ", ".join(keywords))
    
    console.print(criteria_table)
    
    # Save filtered data
    if output:
        filtered_df.to_csv(output, index=False)
        console.print(f"💾 Filtered data saved to {output}", style="green")

@cli.group()
def models():
    """Model management commands"""
    pass

@models.command()
def list():
    """List available models"""
    console.print(Panel.fit("🤖 Available Models", style="bold blue"))
    
    nlp_engine = NLPEngine()
    
    models_table = Table(title="Default Models")
    models_table.add_column("Task", style="cyan")
    models_table.add_column("Model", style="magenta")
    
    for task, model in nlp_engine.default_models.items():
        models_table.add_row(task, model)
    
    console.print(models_table)
    
    if nlp_engine.model_cache:
        cached_table = Table(title="Cached Models")
        cached_table.add_column("Model", style="cyan")
        
        for model_name in nlp_engine.model_cache.keys():
            cached_table.add_row(model_name)
        
        console.print(cached_table)

@models.command()
@click.argument('model_name')
@click.argument('task')
def load(model_name, task):
    """Load a specific model"""
    console.print(Panel.fit("📥 Model Loading", style="bold green"))
    
    nlp_engine = NLPEngine()
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task_progress = progress.add_task(f"Loading {model_name}...", total=None)
        
        try:
            model = nlp_engine.load_model(model_name, task)
            progress.update(task_progress, description="Model loaded successfully!")
            
            if model:
                console.print(f"✅ Model {model_name} loaded for task: {task}", style="green")
            else:
                console.print(f"❌ Failed to load model {model_name}", style="red")
                
        except Exception as e:
            console.print(f"❌ Error loading model: {e}", style="red")

@cli.command()
def info():
    """Show NLP system information"""
    console.print(Panel.fit("ℹ️ NLP System Information", style="bold cyan"))
    
    nlp_engine = NLPEngine()
    gatherer = CorpusGatherer()
    
    info_table = Table(title="System Overview")
    info_table.add_column("Component", style="cyan")
    info_table.add_column("Value", style="magenta")
    
    info_table.add_row("NLP Engine Version", "1.0.0")
    info_table.add_row("Corpus Gatherer Version", "1.0.0")
    info_table.add_row("Device", nlp_engine.device)
    info_table.add_row("Models Directory", str(nlp_engine.models_dir))
    info_table.add_row("Corpus Directory", str(gatherer.output_dir))
    
    console.print(info_table)
    
    # Available sources
    sources_table = Table(title="Available Data Sources")
    sources_table.add_column("Source", style="cyan")
    
    for source in gatherer.collectors.keys():
        sources_table.add_row(source)
    
    console.print(sources_table)
    
    # Available analysis types
    analysis_table = Table(title="Available Analysis Types")
    analysis_table.add_column("Type", style="cyan")
    
    analysis_types = [
        "sentiment", "entities", "keywords", "readability",
        "summary", "topics", "clustering", "embeddings"
    ]
    
    for analysis_type in analysis_types:
        analysis_table.add_row(analysis_type)
    
    console.print(analysis_table)

@cli.command()
def demo():
    """Run a demonstration of NLP capabilities"""
    console.print(Panel.fit("🎯 NLP Demo", style="bold magenta"))
    
    demo_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on 
    the interaction between computers and human language. It enables machines to understand, 
    interpret, and generate human language in a way that is both meaningful and useful.
    
    NLP has applications in various domains including machine translation, sentiment analysis, 
    chatbots, and information extraction. Modern NLP systems use deep learning techniques 
    such as transformers and large language models to achieve state-of-the-art performance.
    """
    
    console.print(f"📝 Demo Text: {demo_text.strip()}")
    
    nlp_engine = NLPEngine()
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Running NLP analysis...", total=None)
        
        # Run comprehensive analysis
        results = nlp_engine.comprehensive_analysis(demo_text)
        progress.update(task, description="Analysis completed!")
    
    # Display results
    display_analysis_results(results, demo_text)

if __name__ == '__main__':
    cli()
