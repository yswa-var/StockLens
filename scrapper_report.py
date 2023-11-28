import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def scrape_balanceSheet(company_code):
    url = f"https://www.screener.in/company/{company_code}/"
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    # Locate the Peer Comparison table
    # This selector might need to be adjusted based on actual HTML
    table = soup.find('table')

    if not table:
        return "Peer Comparison table not found"

    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        rows.append(cols)

    # Convert to DataFrame for easy manipulation
    peer_comparison_data = pd.DataFrame(rows, columns=headers)

    return peer_comparison_data

# Example usage
company_code = 'GAIL'  # Replace with any other company code
balance = scrape_balanceSheet(company_code)