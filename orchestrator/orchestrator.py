from fastapi import FastAPI
from pydantic import BaseModel
from data_ingestion.api_agent import APIAgent
from data_ingestion.scraping_agent import ScrapingAgent
from agents.retriever_agent import RetrieverAgent
from agents.language_agent import LanguageAgent  # <- Language Agent
from typing import List
from pydantic import BaseModel
import speech_recognition as sr
from fastapi.responses import JSONResponse


app = FastAPI()

# --- Data Ingestion Agents ---
@app.get("/get_market_data/{ticker}")
async def get_market_data(ticker: str):
    api_agent = APIAgent(ticker)
    data = api_agent.get_data()
    return {"data": data.to_dict()}

@app.get("/get_filings/{cik}")
async def get_filings(cik: str):
    scraping_agent = ScrapingAgent()
    filings_summary = scraping_agent.download_filings(cik, filing_type="10-K", count=2)
    return {"filings": filings_summary}

# --- Retriever Agent ---
retriever = RetrieverAgent()

@app.post("/build_index/")
async def build_index(texts: List[str]):
    retriever.build_index(texts)
    return {"message": "Index built successfully"}

@app.get("/retrieve/")
async def retrieve(query: str, k: int = 3):
    results = retriever.retrieve(query, k)
    return {"results": results}

@app.post("/ingest_and_index/")
async def ingest_and_index(ticker: str = None, cik: str = None):
    texts = []
    if ticker:
        api_agent = APIAgent(ticker)
        market_data = api_agent.get_data().to_string()
        texts.append(market_data)
    if cik:
        scraping_agent = ScrapingAgent()
        filings_summary = scraping_agent.download_filings(cik, filing_type="10-K", count=2)
        texts.extend(filings_summary)
    if not texts:
        return {"error": "No data provided to index."}
    retriever.build_index(texts)
    return {"message": "Ingested and indexed data from sources."}

class QueryInput(BaseModel):
    query: str

language_agent = LanguageAgent()  # Initialize it once

@app.post("/ask_agent/")
async def ask_agent(input_data: QueryInput):
    response = language_agent.generate_response(input_data.query)
    return {"response": response}



@app.get("/transcribe/")
async def transcribe_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=7)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Transcribed: {text}")
        return {"transcription": text}
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return JSONResponse(status_code=400, content={"error": "Speech unintelligible."})
    except sr.RequestError as e:
        print(f"Google API error: {e}")
        return JSONResponse(status_code=500, content={"error": "API unavailable or network error."})

