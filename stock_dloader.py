import streamlit as st
import base64
from datetime import datetime
import io
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings
import plotly.express as px
import time
import numpy as np
today_date = datetime.today().strftime('%d-%m-%Y')
np.seterr(divide='ignore', invalid='ignore')

# Open the image using Pillow (PIL)
image = "https://raw.githubusercontent.com/bbmusa/StockLens/main/app/image.jpg"

# Display the image in Streamlit
st.image(image, width=600)
def format_nse_codes(codes):
    """
    This function takes a list of NSE codes and returns a string formatted with today's date
    and the codes prefixed with 'NSE:'.
    """
    # Get today's date in the format '9 Nov 2023'
    today_date = datetime.now().strftime("%d %b %Y").lstrip("0")

    # Convert the list of NSE codes to the desired format
    formatted_codes = ", ".join([f"NSE:{code}" for code in codes])

    # Combine the date and formatted NSE codes
    formatted_string = f"### {today_date}, {formatted_codes}"
    
    return formatted_string

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
    # Define a dictionary to map the starting strings to the new names
    rename_dict = {
        'Pro': 'Promoter',
        'FII': 'FII',
        'DII': 'DII',
        'Gov': 'Government',
        'Oth': 'Others',
        'Pub': 'Public'
    }

    # Function to apply the renaming logic
    def rename_columns(col_name):
        for key, value in rename_dict.items():
            if col_name.startswith(key):
                return value
        return col_name  # Return the original name if no match is found

    # Rename the columns using the function
    df.columns = [rename_columns(col) for col in df.columns]
    df['Promoter'] = df['Promoter'].str.replace('%', '').astype(float)
    df['FII'] = df['FII'].str.replace('%', '').astype(float)
    df['DII'] = df['DII'].str.replace('%', '').astype(float)
    df['Public'] = df['Public'].str.replace('%', '').astype(float)

    df['Public % Change'] = df['Public'].pct_change() * 100
    df['FII % Change'] = df['FII'].pct_change() * 100
    df['DII % Change'] = df['DII'].pct_change() * 100
    df['Promoter % Change'] = df['Promoter'].pct_change() * 100

    # The first row will have NaN values because there is no previous row to compare with
    # You may want to fill NaN values with 0 or leave them as is, depending on your requirement
    df.fillna(0, inplace=True)

    df["Score"] = (df['Promoter % Change']+df['DII % Change']+df['FII % Change'])-df['Public % Change'] 
    st.link_button(value, url)
    fig = px.bar(df, x=df.index, y='Score', title='Score Bar Graph')
    st.plotly_chart(fig)

    financial_data = {}

    # Find the 'company-ratios' div and extract each financial data point
    company_ratios = soup.find('div', class_='company-ratios')
    if company_ratios:
        for li in company_ratios.find_all('li', {'data-source': 'default'}):
            name = li.find('span', class_='name').get_text(strip=True)
            value = li.find('span', class_='value').get_text(strip=True)
            financial_data[name] = value
    else:
        print("Company Ratios section not found in the HTML content.")
    
    st.title("Basic Data")
    st.write(financial_data)
    #-----------------
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
    balanceSheet = pd.DataFrame(rows, columns=headers)
    st.title("Balance Sheet")
    st.dataframe(balanceSheet)
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
 
# Define a function to refresh the data
def refresh_data():
    st.write("Refreshing data...")
    df = get_stocks()
    return df

# Initial data retrieval
df = get_stocks()

# Button to trigger data refresh
if st.button('Refresh Data'):
    df = refresh_data()


c1, c2 = st.columns([1, 2])

c1.write(df)
tradingview = format_nse_codes(df['nsecode'])
c2.code(tradingview)

# Rest of your code...
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
        st.title("ShareHolding")
        st.write(result)


#------------------------------

# def scrape_financial_data(url):
#     """
#     Scrape financial data from HTML content of a Screener.in company page.

#     :param html_content: HTML content of the page
#     :return: Dictionary containing the financial data
#     """
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     financial_data = {}

#     # Find the 'company-ratios' div and extract each financial data point
#     company_ratios = soup.find('div', class_='company-ratios')
#     if company_ratios:
#         for li in company_ratios.find_all('li', {'data-source': 'default'}):
#             name = li.find('span', class_='name').get_text(strip=True)
#             value = li.find('span', class_='value').get_text(strip=True)
#             financial_data[name] = value
#     else:
#         print("Company Ratios section not found in the HTML content.")

#     return financial_data

# url = "https://www.screener.in/company/GAIL/"
# data = scrape_financial_data(url)
# st.write(data)
