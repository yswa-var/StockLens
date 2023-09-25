import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://www.screener.in/company/OFSS/"
response = requests.get(url)

soup = bs(response.content, "html.parser")


# Find the section with id "quarterly-shp"
quarterly_shp_section = soup.find('div', {'id': 'quarterly-shp'})

# Find the shareholding pattern table within the section
shareholding_table = quarterly_shp_section.find('table', {'class': 'data-table'})

# Extract table data into a list of lists
shareholding_data = []
for row in shareholding_table.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    shareholding_data.append(cols)

# # Print the shareholding data
# for row in shareholding_data:
#     print(row)

df = pd.DataFrame(shareholding_data)
print(df)