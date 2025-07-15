import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Stock Analysis with CrewAI",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Stock Analysis with CrewAI")
st.markdown("""
This application uses CrewAI with Google Gemini Pro to analyze stocks.
Enter a stock symbol to get a comprehensive analysis.
""")

# Input for stock symbol
stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL, MSFT):", "").upper()

if st.button("Analyze Stock"):
    if stock_symbol:
        with st.spinner("Analyzing stock data..."):
            try:
                # Make request to FastAPI endpoint
                response = requests.post(
                    "http://localhost:8000/analyze_stock",
                    json={"stock_symbol": stock_symbol}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display the analysis
                    st.markdown("## Analysis Results")
                    st.markdown(result["analysis"])
                else:
                    st.error(f"Error: {response.json()['detail']}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a stock symbol")

# Add some helpful information
st.markdown("""
---
### How to use:
1. Enter a valid stock symbol (e.g., AAPL for Apple Inc.)
2. Click the "Analyze Stock" button
3. Wait for the analysis to complete
4. Review the comprehensive analysis provided by the AI

### Note:
- Make sure the FastAPI backend is running
- Stock symbols should be in uppercase
- The analysis may take a few moments to complete
""") 