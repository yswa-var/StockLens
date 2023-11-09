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
np.seterr(divide='ignore', invalid='ignore')

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


def chartink_eng(cond=None):
    url="https://chartink.com/screener/process"

    if cond is None:
        return

    conditions = {"scan_clause": cond}

    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        meta = soup.find_all("meta", {"name": "csrf-token"})[0]["content"]
        header = {"x-csrf-token": meta}
        data = s.post(url, headers=header, data=conditions).json()
        scan = pd.DataFrame(data["data"])
        return scan

def get_stocks():
    #short term
    cond = "( {cash} ( latest ema ( latest close , 21 ) >= latest ema ( latest close , 50 ) and latest ema ( close,10 ) / latest ema ( close,21 ) <= 1.03 and latest ema ( close,10 ) / latest ema ( close,21 ) > 1 and latest ema ( close,21 ) / latest ema ( close,30 ) <= 1.03 and latest ema ( close,21 ) / latest ema ( close,30 ) > 1 and latest ema ( close,30 ) / latest ema ( close,50 ) <= 1.03 and latest ema ( close,30 ) / latest ema ( close,50 ) > 1 and latest close >= weekly max ( 52 , weekly high ) * 0.75 and latest close >= weekly max ( 52 , weekly low ) * 1 and latest close > 30 and latest sma ( latest volume , 50 ) > 10000 and latest close > 30 and market cap >= 300 and latest ema ( latest close , 10 ) > latest ema ( latest close , 21 ) and latest ema ( latest close , 21 ) > latest ema ( latest close , 50 ) and latest ema ( latest close , 50 ) > latest ema ( latest close , 100 ) and latest close > latest ema ( latest close , 50 ) and quarterly indian public percentage <= 1 quarter ago indian public percentage and 1 quarter ago indian public percentage <= 2 quarter ago indian public percentage and 2 quarter ago indian public percentage <= 3 quarter ago indian public percentage and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) and ( {cash} ( quarterly indian promoter and group percentage > 1 quarter ago indian promoter and group percentage or 1 quarter ago indian promoter and group percentage > 2 quarter ago indian promoter and group percentage or 2 quarter ago indian promoter and group percentage > 3 quarter ago indian promoter and group percentage or 3 quarter ago indian promoter and group percentage > 4 quarters ago indian promoter and group percentage or 4 quarters ago indian promoter and group percentage > 5 quarters ago indian promoter and group percentage ) ) ) ) "
    df1 = pd.DataFrame(chartink_eng(cond=cond))['nsecode']

    #mid
    cond = "( {cash} ( weekly ema ( weekly close , 21 ) >= weekly ema ( weekly close , 50 ) and weekly ema ( close,10 ) / weekly ema ( close,21 ) <= 1.03 and weekly ema ( close,10 ) / weekly ema ( close,21 ) > 1 and weekly ema ( close,21 ) / weekly ema ( close,30 ) <= 1.03 and weekly ema ( close,21 ) / weekly ema ( close,30 ) > 1 and weekly ema ( close,30 ) / weekly ema ( close,50 ) <= 1.03 and weekly ema ( close,30 ) / weekly ema ( close,50 ) > 1 and latest close > 30 and latest sma ( latest volume , 50 ) > 3000 and market cap >= 300 and latest close > 30 and weekly ema ( weekly close , 10 ) > weekly ema ( weekly close , 21 ) and weekly ema ( weekly close , 21 ) > weekly ema ( weekly close , 50 ) and weekly ema ( weekly close , 50 ) > weekly ema ( weekly close , 100 ) and weekly close > weekly ema ( weekly close , 50 ) and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) and latest volume > latest sma ( latest volume , 20 ) and quarterly indian public percentage <= 1 quarter ago indian public percentage and 1 quarter ago indian public percentage <= 2 quarter ago indian public percentage and ( {cash} ( quarterly indian promoter and group percentage > 1 quarter ago indian promoter and group percentage or 1 quarter ago indian promoter and group percentage > 2 quarter ago indian promoter and group percentage or 2 quarter ago indian promoter and group percentage > 3 quarter ago indian promoter and group percentage or 3 quarter ago indian promoter and group percentage > 4 quarters ago indian promoter and group percentage or 4 quarters ago indian promoter and group percentage > 5 quarters ago indian promoter and group percentage ) ) ) ) "
    df2 = pd.DataFrame(chartink_eng(cond=cond))['nsecode']

    #weekly
    cond = "( {cash} ( latest ema ( latest close , 20 ) >= latest ema ( latest close , 50 ) and latest ema ( latest close , 50 ) >= latest ema ( latest close , 75 ) and latest ema ( latest close , 75 ) >= latest ema ( latest close , 100 ) and latest ema ( latest close , 100 ) >= latest ema ( latest close , 200 ) and latest ema ( close,20 ) / latest ema ( close,50 ) < 1.03 and latest ema ( close,20 ) / latest ema ( close,50 ) > 1 and latest ema ( close,50 ) / latest ema ( close,75 ) < 1.03 and latest ema ( close,50 ) / latest ema ( close,75 ) > 1 and latest ema ( close,75 ) / latest ema ( close,100 ) < 1.03 and latest ema ( close,75 ) / latest ema ( close,100 ) > 1 and ( {cash} ( quarterly indian promoter and group percentage > 1 quarter ago indian promoter and group percentage or 1 quarter ago indian promoter and group percentage > 2 quarter ago indian promoter and group percentage or 2 quarter ago indian promoter and group percentage > 3 quarter ago indian promoter and group percentage or 3 quarter ago indian promoter and group percentage > 4 quarters ago indian promoter and group percentage or 4 quarters ago indian promoter and group percentage > 5 quarters ago indian promoter and group percentage ) ) and ( {cash} ( latest close >= weekly max ( 52 , weekly high ) * 0.75 and latest close >= weekly max ( 52 , weekly low ) * 1 ) ) and ( {cash} ( latest close > 30 and latest sma ( latest volume , 50 ) > 10000 and market cap >= 300 and latest close > 30 ) ) and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) ) ) "
    df3 = pd.DataFrame(chartink_eng(cond=cond))['nsecode']
    # Convert Series to DataFrame
    df1 = df1.to_frame()
    df2 = df2.to_frame()
    df3 = df3.to_frame()

    # Reset index to make the current index a column and create a proper index
    df1.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    df3.reset_index(drop=True, inplace=True)

    # Add 'Cat' column
    df1['Cat'] = "S"
    df2['Cat'] = "M"
    df3['Cat'] = "L"

    # Concatenate DataFrames vertically
    df = pd.concat([df1, df2, df3], axis=0)

    return df

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
    time.sleep(4)
    return df


def HoldingScore(ticker):
    try:
        df = get_shareholding(ticker)
        if len(df[0].to_numpy()) == 6:
            df[0] = ["x","Promoter", "FII", "DII", "Retail","Share Holders"]
        if len(df[0].to_numpy()) == 7:
            df[0] = ["x","Promoter", "FII", "DII","Gov", "Retail","Share Holders"]
        if len(df[0].to_numpy()) == 8:
            df[0] = ["x","Promoter", "FII", "DII","Gov", "Retail","other","Share Holders"]
        if len(df[0].to_numpy()) > 8:
            df[0] = ["x","Promoter", "FII", "DII","Gov", "Retail","other","Share Holders",'xx']
        
        df = df.transpose()

        df = df.drop(columns=[0])
        df.columns = df.iloc[0]
        df = df.iloc[1:]

        df.drop([1, 2, 3, 4, 5, 6, 7, 8], inplace=True)
        # Convert percentage strings to float
        df['Promoter'] = df['Promoter'].str.rstrip('%').astype(float)
        df['FII'] = df['FII'].str.rstrip('%').astype(float)
        df['DII'] = df['DII'].str.rstrip('%').astype(float)
        df['Retail'] = df['Retail'].str.rstrip('%').astype(float)
        try:
            df['Gov'] = df['Gov'].str.rstrip('%').astype(float)
        except:
            pass
        # Remove commas and convert 'share holders' to int
        df['Share Holders'] = df['Share Holders'].str.replace(',', '').astype(int)
        score = round((np.diff(df['FII'].to_numpy()) / df['FII'].to_numpy()[:-1]).sum() + (np.diff(df['DII'].to_numpy()) / df['DII'].to_numpy()[:-1]).sum() + (np.diff(df['Promoter'].to_numpy()) / df['Promoter'].to_numpy()[:-1]).sum() - (np.diff(df['Retail'].to_numpy()) / df['Retail'].to_numpy()[:-1]).sum(),5)
        holding = round(-(np.diff(df['Share Holders'].to_numpy()) / df['Share Holders'].to_numpy()[:-1]).sum(),3)
        return score, holding
    except Exception as e:
        print('error '+ticker)
        print(e)
        return 0, 0
        
def csv_caller(df):
    df["Holding score"] = 0
    df['Holding no'] = 0
    k = 0 
    progress_bar = st.progress(0)
    for i in df['nsecode']:
        Score, holding = HoldingScore(i)
        # Convert the 'Holding score' and 'Holding no' columns to float data type
        df['Holding score'] = df['Holding score'].astype(float)
        df['Holding no'] = df['Holding no'].astype(float)

        # Now you can assign the floating-point values without warnings
        df.loc[k, 'Holding score'] = Score  # Assuming Score is a float
        df.loc[k, 'Holding no'] = holding   # Assuming holding is a float

        k+=1
        progress_bar.progress(k)
    df.fillna(0.0, inplace=True)
    return df

df = get_stocks()
st.title('HotChick Stocks')
df = csv_caller(df)
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