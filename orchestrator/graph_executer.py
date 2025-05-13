from agents.retriever_agent import RetrieverAgent
from data_ingestion.api_agent import APIAgent
from data_ingestion.scraping_agent import ScrapingAgent
from agents.language_agent import LanguageAgent

class FinancialVoiceAgent:
    def __init__(self):
        # Initializing the components of the financial voice assistant
        self.retriever = RetrieverAgent()
        self.api_agent = APIAgent()
        self.scraping_agent = ScrapingAgent()
        self.llm_agent = LanguageAgent()

    def execute(self, query: str):
        """
        Main function to simulate a financial voice agent.
        It retrieves documents, fetches financial data, and generates a response.
        """
        # Step 1: Retrieve relevant documents based on the user's query
        relevant_docs = self.retriever.retrieve(query)

        # Step 2: Fetch data from financial APIs (e.g., stock data)
        ticker = query.split(" ")[-1]  # Assuming the query ends with a stock ticker
        api_data = self.api_agent.get_data(ticker)  # Get stock data for the ticker
        
        # Step 3: Scrape relevant filings or data (mocking SEC 10-K filings)
        scraping_data = self.scraping_agent.download_filings("0000320193", filing_type="10-K", count=2)  # Mock Apple CIK
        
        # Step 4: Combine the data from retrieval, API, and scraping
        context = relevant_docs + api_data.to_string() + scraping_data
        
        # Step 5: Pass the combined context to the LLM agent to generate a narrative or voice response
        response = self.llm_agent.generate_narrative(context)
        
        # Returning the generated response (which could be read aloud by a TTS system)
        return response


# Example usage (mocking a query from the user)
if __name__ == "__main__":
    financial_agent = FinancialVoiceAgent()
    query = "What is the stock price of Apple?"  # Sample query about a stock ticker
    response = financial_agent.execute(query)
    print("Financial Voice Agent Response:", response)
