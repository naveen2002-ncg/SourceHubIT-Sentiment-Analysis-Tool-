(.venv) PS C:\Users\naveen\SENTIMENT ANALYSIS TOOL> python sentiment_analysis.py             
  File "C:\Users\naveen\SENTIMENT ANALYSIS TOOL\sentiment_analysis.py", line 230             
    blob = TextBlob(text)                                                                    
IndentationError: expected an indented block after 'if' statement on line 229                
(.venv) PS C:\Users\naveen\SENTIMENT ANALYSIS TOOL>        # Sentiment Analysis Tool

A comprehensive sentiment analysis tool that analyzes the sentiment (positive, negative, or neutral) of user input or text data such as tweets, reviews, or comments. The tool provides both a graphical user interface (GUI) and a command-line interface (CLI).

## Features

### Core Features
- **Multiple Analysis Methods**: Uses both VADER and TextBlob for sentiment analysis
- **Emotion Analysis**: Basic emotion detection (joy, sadness, anger, fear, surprise)
- **Text Statistics**: Word count, sentence count, average word length
- **Visualization**: Charts and graphs for sentiment scores
- **Export Results**: Save analysis results to files

### GUI Features
- **Modern Interface**: Clean, user-friendly GUI built with Tkinter
- **Real-time Analysis**: Instant sentiment analysis with progress indicators
- **Sample Texts**: Pre-loaded sample texts for testing
- **Interactive Charts**: Matplotlib-based visualizations
- **Analysis History**: Track previous analyses

### CLI Features
- **Interactive Mode**: Command-line interface for continuous analysis
- **Batch Processing**: Analyze single texts or run in interactive mode
- **JSON Output**: Export results in JSON format
- **Multiple Methods**: Choose between VADER, TextBlob, or both
- **File Output**: Save results to files

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Options

#### Option 1: Virtual Environment (Recommended)
```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Global Installation
```bash
# Install dependencies globally
pip install -r requirements.txt
```

### Verify Installation
```bash
# Test CLI version
python cli_sentiment_analysis.py "Hello world!"

# Test GUI version (if tkinter is available)
python sentiment_analysis.py
```

## Usage

### GUI Version

Run the graphical interface:
```bash
# Make sure virtual environment is activated
python sentiment_analysis.py
```

**Features:**
- Enter text in the input box
- Choose analysis method (VADER, TextBlob, or Both)
- Click "Analyze Sentiment" to get results
- Use sample text buttons for quick testing
- View visualizations of sentiment scores
- Export results to files

### CLI Version

#### Basic Usage
```bash
python cli_sentiment_analysis.py "Your text here"
```

#### Interactive Mode
```bash
python cli_sentiment_analysis.py --interactive
```

#### Command Line Options
```bash
# Analyze with specific method
python cli_sentiment_analysis.py --method vader "This is great!"

# Output results in JSON format
python cli_sentiment_analysis.py --json "Some text"

# Save results to file
python cli_sentiment_analysis.py --json --output results.json "Text to analyze"
```

#### Available Commands in Interactive Mode
- `exit` - Quit the program
- `help` - Show available commands
- `sample positive` - Load a positive sample text
- `sample negative` - Load a negative sample text
- `sample neutral` - Load a neutral sample text

### Demo Script
```bash
# Run comprehensive demo
python demo.py
```

## Analysis Methods

### VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Purpose**: Optimized for social media text
- **Output**: Compound score (-1 to 1), positive/neutral/negative scores
- **Strengths**: Handles emojis, slang, and informal language well

### TextBlob
- **Purpose**: General-purpose sentiment analysis
- **Output**: Polarity (-1 to 1) and subjectivity (0 to 1)
- **Strengths**: Good for formal text and longer documents

### Emotion Analysis
- **Method**: Keyword-based emotion detection
- **Emotions**: Joy, Sadness, Anger, Fear, Surprise
- **Output**: Emotion scores based on keyword frequency

## Output Examples

### GUI Output
The GUI displays:
- Sentiment classification (Positive/Negative/Neutral)
- Detailed scores from each method
- Emotion analysis results
- Text statistics
- Visual charts

### CLI Output
```
============================================================
SENTIMENT ANALYSIS RESULTS
============================================================
Text: I absolutely love this product! It's amazing and works perfectly...
Analysis Time: 2024-01-15 14:30:25
------------------------------------------------------------

VADER ANALYSIS:
  Sentiment: Positive
  Compound Score: 0.636
  Positive: 0.556
  Neutral: 0.444
  Negative: 0.000

TEXTBLOB ANALYSIS:
  Sentiment: Positive
  Polarity: 0.600
  Subjectivity: 0.800

EMOTION ANALYSIS:
  Joy: 3

TEXT STATISTICS:
  Total Words: 15
  Filtered Words: 12
  Sentences: 1
  Average Word Length: 5.2

============================================================
```

## File Structure

```
SENTIMENT ANALYSIS TOOL/
├── sentiment_analysis.py      # GUI version
├── cli_sentiment_analysis.py  # Command-line version
├── demo.py                    # Demo script
├── requirements.txt           # Python dependencies
├── sample_texts.txt          # Long text examples
├── README.md                 # This file
├── run_gui.bat              # Windows GUI launcher
├── run_cli.bat              # Windows CLI launcher
└── PROJECT_SUMMARY.md       # Project overview
```

## Dependencies

- **textblob**: Text processing and sentiment analysis
- **vaderSentiment**: VADER sentiment analysis
- **nltk**: Natural language processing
- **tkinter**: GUI framework (usually included with Python)
- **matplotlib**: Data visualization
- **pandas**: Data manipulation
- **numpy**: Numerical computing

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'matplotlib'**
   ```bash
   # Solution: Install in virtual environment
   pip install matplotlib
   
   # Or reinstall all dependencies
   pip install -r requirements.txt
   ```

2. **NLTK Data Not Found**
   - The tool automatically downloads required NLTK data
   - If issues persist, manually download:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)
   - Use virtual environment to avoid conflicts

4. **GUI Not Working**
   - Ensure tkinter is available (usually included with Python)
   - On some Linux systems: `sudo apt-get install python3-tk`
   - Try CLI version if GUI fails: `python cli_sentiment_analysis.py --interactive`

5. **Virtual Environment Issues**
   ```bash
   # Create new virtual environment
   python -m venv .venv
   
   # Activate (Windows)
   .venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### Performance Tips

- For large texts, the GUI version processes analysis in a separate thread
- CLI version is faster for batch processing
- VADER is generally faster than TextBlob for short texts
- Use virtual environment to avoid dependency conflicts

## Testing Long Texts

The tool includes sample long texts for testing:

```bash
# Test with long text samples
python cli_sentiment_analysis.py --interactive

# Then use commands like:
# sample positive
# sample negative
# sample neutral
```

Or copy text from `sample_texts.txt` for comprehensive testing.

## Customization

### Adding New Emotions
Edit the emotion keywords in both files:
```python
emotions = {
    "joy": ["happy", "joy", "excited", ...],
    "sadness": ["sad", "depressed", ...],
    # Add new emotions here
}
```

### Modifying Sentiment Thresholds
Adjust sentiment classification thresholds:
```python
# VADER thresholds
if compound >= 0.05:  # Adjust this value
    sentiment = "Positive"
```

## Contributing

Feel free to enhance the tool by:
- Adding more analysis methods
- Improving emotion detection
- Enhancing the GUI design
- Adding support for more languages
- Implementing batch file processing

## License

This project is open source and available under the MIT License.

## Acknowledgments

- VADER: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text.
- TextBlob: Steven Loria and contributors
- NLTK: Natural Language Toolkit community 