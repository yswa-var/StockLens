import pandas as pd
import streamlit as st
import base64
from datetime import datetime
import io
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings
import time
import numpy as np
today_date = datetime.today().strftime('%d-%m-%Y')


def download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Base64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">{text}</a>'
    return href




# Display DataFrame in the sidebar
def download_csv():
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

# Function to download as Excel
def download_excel():
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    excel_data = excel_buffer.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data.xlsx">Download Excel file</a>'
    st.markdown(href, unsafe_allow_html=True)

def process_button_click(value):
    url = "https://www.screener.in/company/" + value +"/"
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
    df = df.transpose()
    df = df.drop(columns=[0])
    df.columns = df.iloc[0]
    df = df.iloc[1:]

    return df


df = pd.read_csv(today_date+".csv")
df = df.drop(columns=['Unnamed: 0'])
st.title('HotChick Stocks')

# Buttons for downloading CSV and Excel
st.write(df)
st.sidebar.header('Download as:')
if st.sidebar.button('CSV'):
    download_csv()
if st.sidebar.button('Excel'):
    download_excel()

st.sidebar.write('Know More: ')
unique_values = df['nsecode'].unique()

# Display buttons for each unique value
for value in unique_values:
    button_label = f'{value}'
    if st.sidebar.button(button_label):
        result = process_button_click(value)
        st.write(result)