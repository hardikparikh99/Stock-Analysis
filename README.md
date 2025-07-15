# Stock Analysis with CrewAI and Google Gemini Pro

This project uses CrewAI with Google Gemini Pro to analyze stocks. It provides a FastAPI backend and a Streamlit frontend for an interactive user experience.

## Features

- Stock analysis using CrewAI and Google Gemini Pro
- Real-time stock data from Alpha Vantage API
- Interactive Streamlit interface
- FastAPI backend for processing requests

## Prerequisites

- Python 3.10 or higher
- Google Gemini API key
- Alpha Vantage API key

## Running Different Versions

This project supports three main backend configurations. By default, it runs with yfinance and Google Gemini API (Version 3). You can switch to other versions by commenting/uncommenting the relevant code sections in `main.py` as described below.

### Version 1: Ollama + Alpha Vantage API
- **Use when you want to run LLM inference locally with Ollama and fetch stock data from Alpha Vantage.**
- **Requirements:**
  - Ollama installed and running locally ([Ollama setup guide](https://ollama.com/))
  - Alpha Vantage API key
- **Setup:**
  1. In `main.py`, uncomment the code block labeled `# VERSION 1: WORKING WITH OLLAMA` (lines 1–101 approx) and comment out the other versions.
  2. Ensure you have the following in your `.env` file:
     ```
     ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
     ```
  3. Pull the required LLaMA model with:
     ```bash
     ollama pull llama3
     ollama run llama3
     ```
  4. Start the FastAPI backend:
     ```bash
     python main.py
     ```
  5. Start the Streamlit frontend as usual.

### Version 2: Google Gemini API + Alpha Vantage API
- **Use when you want to use Google Gemini for LLM and Alpha Vantage for stock data.**
- **Requirements:**
  - Google Gemini API key
  - Alpha Vantage API key
- **Setup:**
  1. In `main.py`, uncomment the code block labeled `# VERSION 2: Gemini + Alpha Vantage` (lines 102–188 approx) and comment out the other versions.
  2. Ensure you have the following in your `.env` file:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
     ```
  3. Start the FastAPI backend:
     ```bash
     python main.py
     ```
  4. Start the Streamlit frontend as usual.

### Version 3 (Default): yfinance + Google Gemini API
- **Use when you want to use Google Gemini for LLM and yfinance for stock data (no Alpha Vantage API key needed).**
- **Requirements:**
  - Google Gemini API key
- **Setup:**
  1. By default, this version is active in `main.py` (from line 189 onward).
  2. Ensure you have the following in your `.env` file:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```
  3. Start the FastAPI backend:
     ```bash
     python main.py
     ```
  4. Start the Streamlit frontend as usual.

**To switch versions:** Edit `main.py` to comment/uncomment the corresponding code blocks as described above. Only one version should be active at a time.

---

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
   ```

## Project Structure

```
Stock-Analysis/
│
├── app.py              # Streamlit frontend application
├── main.py             # FastAPI backend server
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
├── .gitignore         # Git ignore file
└── venv/              # Python virtual environment
```

## Running the Application

1. Start the FastAPI backend:
   ```bash
   uvicorn main:app --reload
   ```

2. In a new terminal, start the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## Usage

1. Enter a stock symbol (e.g., AAPL, GOOGL, MSFT)
2. Click "Analyze Stock"
3. Wait for the analysis to complete
4. Review the comprehensive analysis provided by the AI

## Note

- Make sure both the FastAPI backend and Streamlit frontend are running
- Stock symbols should be entered in uppercase
- The analysis may take a few moments to complete 