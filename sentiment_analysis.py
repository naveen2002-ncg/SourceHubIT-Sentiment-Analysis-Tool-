import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import threading
import time

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SentimentAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize analyzers
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Create GUI components
        self.create_widgets()
        
        # Store analysis history
        self.analysis_history = []
        
    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="Sentiment Analysis Tool", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for input and controls
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Input section
        input_frame = ttk.LabelFrame(left_panel, text="Input Text", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(
            input_frame, 
            height=10, 
            width=50,
            font=("Arial", 11),
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # Sample text buttons
        sample_frame = ttk.Frame(input_frame)
        sample_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            sample_frame, 
            text="Sample Positive", 
            command=lambda: self.load_sample_text("positive")
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            sample_frame, 
            text="Sample Negative", 
            command=lambda: self.load_sample_text("negative")
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            sample_frame, 
            text="Sample Neutral", 
            command=lambda: self.load_sample_text("neutral")
        ).pack(side=tk.LEFT)
        
        # Analysis options
        options_frame = ttk.LabelFrame(left_panel, text="Analysis Options", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Analysis method selection
        ttk.Label(options_frame, text="Analysis Method:").pack(anchor=tk.W)
        self.method_var = tk.StringVar(value="vader")
        method_frame = ttk.Frame(options_frame)
        method_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Radiobutton(
            method_frame, 
            text="VADER", 
            variable=self.method_var, 
            value="vader"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            method_frame, 
            text="TextBlob", 
            variable=self.method_var, 
            value="textblob"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            method_frame, 
            text="Both", 
            variable=self.method_var, 
            value="both"
        ).pack(side=tk.LEFT)
        
        # Analyze button
        analyze_frame = ttk.Frame(left_panel)
        analyze_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.analyze_button = ttk.Button(
            analyze_frame,
            text="Analyze Sentiment",
            command=self.analyze_sentiment,
            style="Accent.TButton"
        )
        self.analyze_button.pack(fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            analyze_frame, 
            mode='indeterminate'
        )
        
        # Right panel for results
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(right_panel, text="Analysis Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            width=40,
            font=("Arial", 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Visualization frame
        viz_frame = ttk.LabelFrame(right_panel, text="Visualization", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure for charts
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Clear button
        clear_frame = ttk.Frame(right_panel)
        clear_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            clear_frame,
            text="Clear Results",
            command=self.clear_results
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            clear_frame,
            text="Export Results",
            command=self.export_results
        ).pack(side=tk.LEFT)
        
    def load_sample_text(self, sentiment_type):
        samples = {
            "positive": "I absolutely love this product! It's amazing and works perfectly. The quality is outstanding and I would definitely recommend it to everyone. This is the best purchase I've ever made!",
            "negative": "This is the worst product I've ever used. It's completely broken and doesn't work at all. The quality is terrible and I'm very disappointed. I would never recommend this to anyone.",
            "neutral": "The product arrived on time. It seems to work as described. The packaging was adequate. I haven't used it extensively yet, so I can't give a full opinion."
        }
        
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, samples.get(sentiment_type, ""))
        
    def analyze_sentiment(self):
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze.")
            return
            
        # Show progress
        self.analyze_button.config(state=tk.DISABLED)
        self.progress.pack(fill=tk.X, pady=(10, 0))
        self.progress.start()
        
        # Run analysis in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._perform_analysis, args=(text,))
        thread.daemon = True
        thread.start()
        
    def _perform_analysis(self, text):
        try:
            method = self.method_var.get()
            results = {}
            
            if method in ["vader", "both"]:
                vader_scores = self.vader_analyzer.polarity_scores(text)
                results["VADER"] = {
                    "sentiment": self._get_vader_sentiment(vader_scores),
                    "scores": vader_scores,
                    "compound": vader_scores['compound']
                }
                
            if method in ["textblob", "both"]:
                blob = TextBlob(text)
                textblob_polarity = blob.sentiment.polarity
                textblob_subjectivity = blob.sentiment.subjectivity
                results["TextBlob"] = {
                    "sentiment": self._get_textblob_sentiment(textblob_polarity),
                    "polarity": textblob_polarity,
                    "subjectivity": textblob_subjectivity
                }
            
            # Get emotion analysis
            emotions = self._analyze_emotions(text)
            results["Emotions"] = emotions
            
            # Get text statistics
            stats = self._get_text_statistics(text)
            results["Statistics"] = stats
            
            # Update GUI in main thread
            self.root.after(0, lambda: self._display_results(results, text))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
        finally:
            self.root.after(0, self._stop_progress)
            
    def _get_vader_sentiment(self, scores):
        compound = scores['compound']
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"
            
    def _get_textblob_sentiment(self, polarity):
        if polarity > 0:
            return "Positive"
        elif polarity < 0:
            return "Negative"
        else:
            return "Neutral"
            
    def _analyze_emotions(self, text):
        # Simple emotion analysis based on keyword matching
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
            emotion_scores[emotion] = score
            
        return emotion_scores
        
    def _get_text_statistics(self, text):
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        
        # Filter out stop words and punctuation
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
        
        return {
            "total_words": len(words),
            "filtered_words": len(filtered_words),
            "sentences": len(text.split('.')),
            "avg_word_length": np.mean([len(word) for word in filtered_words]) if filtered_words else 0
        }
        
    def _display_results(self, results, text):
        # Update results text
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        output = f"TEXT ANALYZED:\n{'-' * 40}\n{text[:100]}{'...' if len(text) > 100 else ''}\n\n"
        
        # Display sentiment analysis results
        for method, data in results.items():
            if method == "VADER":
                output += f"VADER ANALYSIS:\n{'-' * 20}\n"
                output += f"Sentiment: {data['sentiment']}\n"
                output += f"Compound Score: {data['compound']:.3f}\n"
                output += f"Positive: {data['scores']['pos']:.3f}\n"
                output += f"Neutral: {data['scores']['neu']:.3f}\n"
                output += f"Negative: {data['scores']['neg']:.3f}\n\n"
                
            elif method == "TextBlob":
                output += f"TEXTBLOB ANALYSIS:\n{'-' * 20}\n"
                output += f"Sentiment: {data['sentiment']}\n"
                output += f"Polarity: {data['polarity']:.3f}\n"
                output += f"Subjectivity: {data['subjectivity']:.3f}\n\n"
                
            elif method == "Emotions":
                output += f"EMOTION ANALYSIS:\n{'-' * 20}\n"
                for emotion, score in data.items():
                    if score > 0:
                        output += f"{emotion.capitalize()}: {score}\n"
                output += "\n"
                
            elif method == "Statistics":
                output += f"TEXT STATISTICS:\n{'-' * 20}\n"
                output += f"Total Words: {data['total_words']}\n"
                output += f"Filtered Words: {data['filtered_words']}\n"
                output += f"Sentences: {data['sentences']}\n"
                output += f"Avg Word Length: {data['avg_word_length']:.1f}\n\n"
        
        self.results_text.insert(1.0, output)
        self.results_text.config(state=tk.DISABLED)
        
        # Create visualization
        self._create_visualization(results)
        
        # Store in history
        self.analysis_history.append({
            "text": text[:100] + "..." if len(text) > 100 else text,
            "results": results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    def _create_visualization(self, results):
        self.ax.clear()
        
        # Create subplots for different visualizations
        if "VADER" in results:
            # VADER scores bar chart
            vader_data = results["VADER"]["scores"]
            categories = list(vader_data.keys())
            values = list(vader_data.values())
            
            bars = self.ax.bar(categories, values, color=['green', 'gray', 'red'])
            self.ax.set_title('VADER Sentiment Scores')
            self.ax.set_ylabel('Score')
            self.ax.set_ylim(0, 1)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.3f}', ha='center', va='bottom')
        
        elif "TextBlob" in results:
            # TextBlob polarity and subjectivity
            polarity = results["TextBlob"]["polarity"]
            subjectivity = results["TextBlob"]["subjectivity"]
            
            self.ax.scatter([polarity], [subjectivity], s=200, c='blue', alpha=0.7)
            self.ax.set_xlabel('Polarity (-1 to 1)')
            self.ax.set_ylabel('Subjectivity (0 to 1)')
            self.ax.set_title('TextBlob Analysis')
            self.ax.grid(True, alpha=0.3)
            self.ax.set_xlim(-1, 1)
            self.ax.set_ylim(0, 1)
            
            # Add reference lines
            self.ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
            self.ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        
        # Add emotion chart if available
        if "Emotions" in results:
            emotions = results["Emotions"]
            if any(score > 0 for score in emotions.values()):
                # Create emotion chart in a separate figure
                fig2, ax2 = plt.subplots(figsize=(4, 3))
                emotion_names = list(emotions.keys())
                emotion_scores = list(emotions.values())
                
                bars = ax2.bar(emotion_names, emotion_scores, color='orange')
                ax2.set_title('Emotion Analysis')
                ax2.set_ylabel('Score')
                
                # Rotate x-axis labels for better readability
                plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
                
                # Add the emotion chart to the main window
                canvas2 = FigureCanvasTkAgg(fig2, self.root)
                canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)
        
        self.canvas.draw()
        
    def _stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.analyze_button.config(state=tk.NORMAL)
        
    def clear_results(self):
        self.text_input.delete(1.0, tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.ax.clear()
        self.canvas.draw()
        
    def export_results(self):
        if not self.analysis_history:
            messagebox.showinfo("Info", "No analysis results to export.")
            return
            
        try:
            # Create a simple export of the last analysis
            filename = f"sentiment_analysis_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("SENTIMENT ANALYSIS RESULTS\n")
                f.write("=" * 50 + "\n\n")
                
                for entry in self.analysis_history[-3:]:  # Export last 3 analyses
                    f.write(f"Timestamp: {entry['timestamp']}\n")
                    f.write(f"Text: {entry['text']}\n")
                    f.write("-" * 30 + "\n")
                    
                    results = entry['results']
                    for method, data in results.items():
                        f.write(f"{method}:\n")
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if isinstance(value, float):
                                    f.write(f"  {key}: {value:.3f}\n")
                                else:
                                    f.write(f"  {key}: {value}\n")
                        f.write("\n")
                    
            messagebox.showinfo("Success", f"Results exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")

def main():
    root = tk.Tk()
    app = SentimentAnalysisTool(root)
    root.mainloop()

if __name__ == '__main__':
    main() 