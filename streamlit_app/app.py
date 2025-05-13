import streamlit as st
import requests

st.title("📊 Finance Assistant")

# -------- Market Data --------
st.header("📈 Market Data")
ticker = st.text_input("Enter stock ticker (e.g., AAPL)")

if ticker:
    response = requests.get(f"http://localhost:8000/get_market_data/{ticker}")
    if response.status_code == 200:
        st.write("Market Data:")
        st.write(response.json())
    else:
        st.error("Failed to fetch market data.")

# -------- SEC Filings --------
st.header("📄 SEC Filings")
cik = st.text_input("Enter CIK (e.g., 0000320193 for Apple Inc.)")

if cik:
    response = requests.get(f"http://localhost:8000/get_filings/{cik}")
    if response.status_code == 200:
        filings = response.json().get("filings", [])
        st.write("SEC Filings Summary:")
        for i, filing in enumerate(filings):
            st.markdown(f"**Filing {i+1}:**")
            st.code(filing)
    else:
        st.error("Failed to fetch filings.")

# # --- Retriever Agent: Build Index ---
# st.header("🧠 Retriever Agent: Build Index")
# texts = st.text_area("Paste text chunks (one per line)", "Apple Inc. is a technology company.\nIt develops iPhones and other devices.")
# if st.button("Build Index"):
#     text_list = texts.split("\n")
#     response = requests.post(f"http://localhost:8000/build_index/", json=text_list)
#     if response.status_code == 200:
#         st.success(response.json()["message"])
#     else:
#         st.error(f"Error: {response.status_code}")

# # --- Retriever Agent: Query Index ---
# st.header("🔍 Retriever Agent: Retrieve Relevant Info")
# query = st.text_input("Enter query", "What does Apple develop?")
# if st.button("Retrieve"):
#     response = requests.get(f"http://localhost:8000/retrieve/", params={"query": query, "k": 3})
#     if response.status_code == 200:
#         st.success("Top results:")
#         st.json(response.json())
#     else:
#         st.error(f"Error: {response.status_code}")

# # ------------ Language Agent: Ask Question ------------
# st.header("🗣️ Ask the Language Agent")
# language_query = st.text_input("Enter query for Language Agent", "")
# if st.button("Ask Agent"):
#     if language_query:
#         response = requests.post("http://localhost:8000/ask_agent/", json={"query": language_query})
#         if response.status_code == 200:
#             st.write("Language Agent Response:")
#             st.write(response.json()["response"])
#         else:
#             st.error("Failed to get response from Language Agent.")
#     else:
#         st.error("Please enter a query.")

# # ------------ Combined Ingest and Index ------------
# st.header("🧵 Ingest & Index Combined Data")
# ticker_input = st.text_input("Ticker for Market Data (Optional)", "")
# cik_input = st.text_input("CIK for 10-K Filings (Optional)", "")

# if st.button("Ingest and Index from Agents"):
#     try:
#         payload = {}
#         if ticker_input:
#             payload["ticker"] = ticker_input
#         if cik_input:
#             payload["cik"] = cik_input

#         response = requests.post(f"http://localhost:8000/ingest_and_index/", params=payload)
#         st.success(response.json()["message"])
#     except Exception as e:
#         st.error(f"Failed to ingest and index: {e}")



st.header("🎙️ Voice Query")

if st.button("Speak Now"):
    with st.spinner("Listening..."):
        response = requests.get("http://localhost:8000/transcribe/")
        if response.status_code == 200:
            transcription = response.json()["transcription"]
            st.success(f"Transcribed: {transcription}")

            # Send to Language Agent
            agent_response = requests.post(
                "http://localhost:8000/ask_agent/", json={"query": transcription}
            )
            if agent_response.status_code == 200:
                st.write("🧠 Language Agent Response:")
                st.write(agent_response.json()["response"])
            else:
                st.error("Language Agent failed to respond.")
        else:
            st.error(response.json().get("error", "Voice transcription failed."))
