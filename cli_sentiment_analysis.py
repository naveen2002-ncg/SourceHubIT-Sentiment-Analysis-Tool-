#!/usr/bin/env python3
"""
Command Line Sentiment Analysis Tool
A simple command-line interface for sentiment analysis using multiple methods.
"""

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import argparse
import sys
import json
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class CLISentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def analyze_text(self, text, method='both'):
        """Analyze sentiment of given text using specified method(s)"""
        results = {}
        
        if method in ['vader', 'both']:
            results['vader'] = self._analyze_vader(text)
            
        if method in ['textblob', 'both']:
            results['textblob'] = self._analyze_textblob(text)
            
        results['emotions'] = self._analyze_emotions(text)
        results['statistics'] = self._get_text_statistics(text)
        
        return results
    
    def _analyze_vader(self, text):
        """Analyze sentiment using VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Determine sentiment based on compound score
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        return {
            'sentiment': sentiment,
            'compound': compound,
            'positive': scores['pos'],
            'neutral': scores['neu'],
            'negative': scores['neg']
        }
    
    def _analyze_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment based on polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity
        }
    
    def _analyze_emotions(self, text):
        """Simple emotion analysis based on keyword matching"""
        emotions = {
            "joy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", "love", "like"],
            "sadness": ["sad", "depressed", "unhappy", "terrible", "awful", "horrible", "disappointed", "hate"],
            "anger": ["angry", "mad", "furious", "rage", "hate", "terrible", "awful", "horrible"],
            "fear": ["afraid", "scared", "fear", "terrified", "worried", "anxious", "nervous"],
            "surprise": ["surprised", "amazed", "shocked", "wow", "incredible", "unbelievable"]
        }
        
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in emotions.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
                
        return emotion_scores
    
    def _get_text_statistics(self, text):
        """Get basic text statistics"""
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        
        # Filter out stop words and punctuation
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
        
        return {
            "total_words": len(words),
            "filtered_words": len(filtered_words),
            "sentences": len(text.split('.')),
            "avg_word_length": sum(len(word) for word in filtered_words) / len(filtered_words) if filtered_words else 0
        }
    
    def print_results(self, results, text, method='both'):
        """Print analysis results in a formatted way"""
        print("\n" + "="*60)
        print("SENTIMENT ANALYSIS RESULTS")
        print("="*60)
        print(f"Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*60)
        
        if method in ['vader', 'both'] and 'vader' in results:
            vader = results['vader']
            print("VADER ANALYSIS:")
            print(f"  Sentiment: {vader['sentiment']}")
            print(f"  Compound Score: {vader['compound']:.3f}")
            print(f"  Positive: {vader['positive']:.3f}")
            print(f"  Neutral: {vader['neutral']:.3f}")
            print(f"  Negative: {vader['negative']:.3f}")
            print()
        
        if method in ['textblob', 'both'] and 'textblob' in results:
            textblob = results['textblob']
            print("TEXTBLOB ANALYSIS:")
            print(f"  Sentiment: {textblob['sentiment']}")
            print(f"  Polarity: {textblob['polarity']:.3f}")
            print(f"  Subjectivity: {textblob['subjectivity']:.3f}")
            print()
        
        if 'emotions' in results and results['emotions']:
            print("EMOTION ANALYSIS:")
            for emotion, score in results['emotions'].items():
                print(f"  {emotion.capitalize()}: {score}")
            print()
        
        if 'statistics' in results:
            stats = results['statistics']
            print("TEXT STATISTICS:")
            print(f"  Total Words: {stats['total_words']}")
            print(f"  Filtered Words: {stats['filtered_words']}")
            print(f"  Sentences: {stats['sentences']}")
            print(f"  Average Word Length: {stats['avg_word_length']:.1f}")
            print()
        
        print("="*60)

def interactive_mode():
    """Run the tool in interactive mode"""
    analyzer = CLISentimentAnalyzer()
    
    print("Sentiment Analysis Tool - Interactive Mode")
    print("Type 'exit' to quit, 'help' for options")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            text = input("\nEnter text to analyze: ").strip()
            
            if text.lower() == 'exit':
                print("Goodbye!")
                break
            elif text.lower() == 'help':
                print("\nAvailable commands:")
                print("  exit - Quit the program")
                print("  help - Show this help message")
                print("  sample positive - Load a positive sample text")
                print("  sample negative - Load a negative sample text")
                print("  sample neutral - Load a neutral sample text")
                continue
            elif text.lower() == 'sample positive':
                text = "I absolutely love this product! It's amazing and works perfectly. The quality is outstanding and I would definitely recommend it to everyone."
            elif text.lower() == 'sample negative':
                text = "This is the worst product I've ever used. It's completely broken and doesn't work at all. The quality is terrible and I'm very disappointed."
            elif text.lower() == 'sample neutral':
                text = "The product arrived on time. It seems to work as described. The packaging was adequate. I haven't used it extensively yet."
            
            if not text:
                print("Please enter some text to analyze.")
                continue
            
            # Analyze the text
            results = analyzer.analyze_text(text, method='both')
            analyzer.print_results(results, text, method='both')
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Sentiment Analysis Tool - Analyze text sentiment using VADER and TextBlob",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_sentiment_analysis.py "I love this product!"
  python cli_sentiment_analysis.py --method vader "This is terrible"
  python cli_sentiment_analysis.py --interactive
  python cli_sentiment_analysis.py --json "Some text here"
        """
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Text to analyze (if not provided, runs in interactive mode)'
    )
    
    parser.add_argument(
        '--method',
        choices=['vader', 'textblob', 'both'],
        default='both',
        help='Analysis method to use (default: both)'
    )
    
    parser.add_argument(
        '--interactive',
        '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file for results (works with --json)'
    )
    
    args = parser.parse_args()
    
    analyzer = CLISentimentAnalyzer()
    
    # If no text provided and not interactive, run interactive mode
    if not args.text and not args.interactive:
        interactive_mode()
        return
    
    # If interactive mode requested
    if args.interactive:
        interactive_mode()
        return
    
    # Analyze the provided text
    try:
        results = analyzer.analyze_text(args.text, method=args.method)
        
        if args.json:
            output_data = {
                'text': args.text,
                'timestamp': datetime.now().isoformat(),
                'method': args.method,
                'results': results
            }
            
            json_output = json.dumps(output_data, indent=2)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                print(f"Results saved to {args.output}")
            else:
                print(json_output)
        else:
            analyzer.print_results(results, args.text, method=args.method)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 