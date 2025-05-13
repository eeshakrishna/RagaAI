# data_ingestion/scraping_agent.py

import requests
from bs4 import BeautifulSoup

class ScrapingAgent:
    def download_filings(self, cik: str, filing_type: str = "10-K", count: int = 2):
        base_url = "https://www.sec.gov"
        search_url = (
            f"{base_url}/cgi-bin/browse-edgar?action=getcompany"
            f"&CIK={cik}&type={filing_type}&count={count}&owner=exclude&output=atom"
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; FinanceAssistant/1.0; +https://yourdomain.com)"
        }

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            entries = soup.find_all("entry")
            if not entries:
                return ["No filings found for the given CIK."]

            filings = []
            for entry in entries[:count]:
                title = entry.find("title").text
                date = entry.find("updated").text
                link = entry.find("link")["href"]
                filings.append(f"📄 {filing_type} filed on {date}\n🔗 {link}")


            return filings

        except Exception as e:
            return [f"Error fetching filings: {e}"]
