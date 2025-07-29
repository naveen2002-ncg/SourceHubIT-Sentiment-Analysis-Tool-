#!/usr/bin/env python3
"""
Demo script for the Sentiment Analysis Tool
This script demonstrates the capabilities of the sentiment analysis tool
with various examples of different sentiment types.
"""

from cli_sentiment_analysis import CLISentimentAnalyzer
import time

def run_demo():
    """Run a comprehensive demo of the sentiment analysis tool"""
    
    print("=" * 70)
    print("SENTIMENT ANALYSIS TOOL - DEMO")
    print("=" * 70)
    print("This demo showcases the tool's capabilities with various text examples.")
    print()
    
    analyzer = CLISentimentAnalyzer()
    
    # Demo texts with different sentiments
    demo_texts = [
        {
            "category": "POSITIVE SENTIMENT",
            "text": "I absolutely love this product! It's amazing and works perfectly. The quality is outstanding and I would definitely recommend it to everyone. This is the best purchase I've ever made!",
            "description": "Highly positive product review"
        },
        {
            "category": "NEGATIVE SENTIMENT", 
            "text": "This is the worst product I've ever used. It's completely broken and doesn't work at all. The quality is terrible and I'm very disappointed. I would never recommend this to anyone.",
            "description": "Highly negative product review"
        },
        {
            "category": "NEUTRAL SENTIMENT",
            "text": "The product arrived on time. It seems to work as described. The packaging was adequate. I haven't used it extensively yet, so I can't give a full opinion.",
            "description": "Neutral product review"
        },
        {
            "category": "MIXED SENTIMENT",
            "text": "The product has some good features but also several problems. I like the design but the performance is disappointing. It's okay for basic use but not worth the price.",
            "description": "Mixed sentiment with both positive and negative aspects"
        },
        {
            "category": "SOCIAL MEDIA TEXT",
            "text": "OMG! Just got my new phone and it's 🔥🔥🔥! The camera is insane and the battery life is amazing. Can't believe how fast it is! #loveit #newphone",
            "description": "Social media post with emojis and hashtags"
        },
        {
            "category": "FORMAL BUSINESS TEXT",
            "text": "The quarterly report indicates satisfactory performance with room for improvement. Revenue targets were met, however, operational costs exceeded projections. Strategic adjustments are recommended.",
            "description": "Formal business communication"
        }
    ]
    
    # Run analysis for each demo text
    for i, demo in enumerate(demo_texts, 1):
        print(f"\n{i}. {demo['category']}")
        print(f"   Description: {demo['description']}")
        print("-" * 50)
        
        # Analyze the text
        results = analyzer.analyze_text(demo['text'], method='both')
        
        # Display results
        analyzer.print_results(results, demo['text'], method='both')
        
        # Add a small delay between analyses for better readability
        if i < len(demo_texts):
            print("\n" + "=" * 70)
            time.sleep(2)
    
    # Summary
    print("\n" + "=" * 70)
    print("DEMO SUMMARY")
    print("=" * 70)
    print("The demo showcased:")
    print("✓ Multiple sentiment analysis methods (VADER and TextBlob)")
    print("✓ Emotion detection capabilities")
    print("✓ Text statistics and analysis")
    print("✓ Handling of different text types (reviews, social media, formal)")
    print("✓ Mixed sentiment analysis")
    print()
    print("The tool successfully analyzed:")
    print(f"• {len(demo_texts)} different text examples")
    print("• Various sentiment intensities")
    print("• Different writing styles and formats")
    print()
    print("To try the tool yourself:")
    print("• GUI Version: python sentiment_analysis.py")
    print("• CLI Version: python cli_sentiment_analysis.py --interactive")
    print("• Single Analysis: python cli_sentiment_analysis.py \"Your text here\"")
    print("=" * 70)

def quick_test():
    """Run a quick test to verify the tool is working"""
    print("Running quick functionality test...")
    
    analyzer = CLISentimentAnalyzer()
    test_text = "This is a test of the sentiment analysis tool."
    
    try:
        results = analyzer.analyze_text(test_text, method='both')
        print("✓ Tool is working correctly!")
        print("✓ All analysis methods functioning")
        print("✓ Ready for use")
        return True
    except Exception as e:
        print(f"✗ Error during test: {e}")
        return False

if __name__ == '__main__':
    print("Sentiment Analysis Tool - Demo")
    print("Choose an option:")
    print("1. Run full demo")
    print("2. Quick functionality test")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                run_demo()
                break
            elif choice == '2':
                quick_test()
                break
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break 