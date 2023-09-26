import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_shareholding(x):
    url = "https://www.screener.in/company/" + x +"/"
    response = requests.get(url)

    soup = bs(response.content, "html.parser")

    quarterly_shp_section = soup.find('div', {'id': 'quarterly-shp'})

    shareholding_table = quarterly_shp_section.find('table', {'class': 'data-table'})
    shareholding_data = []
    for row in shareholding_table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        shareholding_data.append(cols)

    df = pd.DataFrame(shareholding_data)
    return df
