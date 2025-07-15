# VERSION 1: WORKING WITH OLLAMA

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import requests
import json

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Alpha Vantage API Key
os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHA_VANTAGE_API_KEY")

class StockRequest(BaseModel):
    stock_symbol: str

def get_stock_data(symbol: str):
    try:
        ts = TimeSeries()  # Uses ALPHAVANTAGE_API_KEY from env
        data, _ = ts.get_daily(symbol=symbol, outputsize='full')
        df = pd.DataFrame(data).T
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching stock data: {str(e)}")

@app.post("/analyze_stock")
async def analyze_stock(request: StockRequest):
    try:
        stock_data = get_stock_data(request.stock_symbol)
        input_text = f"""
Analyze the following stock data for {request.stock_symbol}:
{stock_data.head().to_string()}

Provide a comprehensive analysis including:
1. Price trends
2. Volatility analysis
3. Key support and resistance levels
4. Trading volume analysis
5. Investment recommendations
"""

        # Send prompt to Ollama's LLaMA3 API
        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json={
                "model": "llama3.2:latest",  # Make sure you pulled this model via `ollama pull llama3`
                "prompt": input_text,
                "stream": False
            }
        )

        if response.status_code != 200:
            raise Exception(f"Ollama Error: {response.text}")

        data = response.json()
        return {"analysis": data.get("response", "No response from LLaMA.")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





# # VERSION 2: Gemini + Alpha Vantage

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# import pandas as pd
# from alpha_vantage.timeseries import TimeSeries
# import requests

# # Load environment variables
# load_dotenv()

# # Initialize FastAPI app
# app = FastAPI()

# # API keys from .env
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# ALPHA_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
# os.environ["ALPHAVANTAGE_API_KEY"] = ALPHA_API_KEY

# # ✅ Use supported Gemini model from your account
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"


# # Request schema
# class StockRequest(BaseModel):
#     stock_symbol: str

# # Function to get stock data
# def get_stock_data(symbol: str):
#     try:
#         ts = TimeSeries()
#         data, _ = ts.get_daily(symbol=symbol, outputsize='full')
#         df = pd.DataFrame(data).T
#         df.index = pd.to_datetime(df.index)
#         return df
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error fetching stock data: {str(e)}")

# # API route to analyze stock
# @app.post("/analyze_stock")
# async def analyze_stock(request: StockRequest):
#     try:
#         stock_data = get_stock_data(request.stock_symbol)

#         prompt = f"""
# Analyze the following stock data for {request.stock_symbol}:
# {stock_data.head().to_string()}

# Provide a comprehensive analysis including:
# 1. Price trends
# 2. Volatility analysis
# 3. Key support and resistance levels
# 4. Trading volume analysis
# 5. Investment recommendations
# """

#         # Call Gemini API
#         response = requests.post(
#             GEMINI_URL,
#             headers={"Content-Type": "application/json"},
#             json={
#                 "contents": [
#                     {
#                         "parts": [{"text": prompt}]
#                     }
#                 ]
#             }
#         )

#         if response.status_code != 200:
#             raise Exception(f"Gemini API error: {response.text}")

#         result = response.json()
#         analysis = result["candidates"][0]["content"]["parts"][0]["text"]
#         return {"analysis": analysis}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Run the app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)





# # VERSION 3: Gemini + YFinance

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# import pandas as pd
# import yfinance as yf
# import requests

# # Load environment variables
# load_dotenv()

# # FastAPI app
# app = FastAPI()

# # Gemini API key from .env
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# # ✅ Using Flash (free tier, high quota)
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# # Request body schema
# class StockRequest(BaseModel):
#     stock_symbol: str

# # Fetch stock data using yFinance (no API key needed)
# def get_stock_data(symbol: str):
#     try:
#         stock = yf.Ticker(symbol)
#         hist = stock.history(period="1mo")
#         if hist.empty:
#             raise Exception("No data returned from yFinance.")
#         return hist
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error fetching stock data: {str(e)}")

# # Route: POST /analyze_stock
# @app.post("/analyze_stock")
# async def analyze_stock(request: StockRequest):
#     try:
#         stock_data = get_stock_data(request.stock_symbol)

#         prompt = f"""
# Analyze the following stock data for {request.stock_symbol}:
# {stock_data.head().to_string()}

# Provide a comprehensive analysis including:
# 1. Price trends
# 2. Volatility analysis
# 3. Key support and resistance levels
# 4. Trading volume analysis
# 5. Investment recommendations
# """

#         # Gemini API request
#         response = requests.post(
#             GEMINI_URL,
#             headers={"Content-Type": "application/json"},
#             json={
#                 "contents": [
#                     {
#                         "parts": [{"text": prompt}]
#                     }
#                 ]
#             }
#         )

#         if response.status_code != 200:
#             raise Exception(f"Gemini API error: {response.text}")

#         result = response.json()
#         analysis = result["candidates"][0]["content"]["parts"][0]["text"]
#         return {"analysis": analysis}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Run app (development server)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

