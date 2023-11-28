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

# Open the image using Pillow (PIL)
image = "https://raw.githubusercontent.com/bbmusa/StockLens/main/app/image.jpg"

# Display the image in Streamlit
st.sidebar.image(image, width=400)

def process_button_click(value):
    url = "https://www.screener.in/company/" + value +"/"
    st.link_button(value,url=url)

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

    #fire
    cond = "( {cash} ( latest ema ( latest close , 20 ) >= latest ema ( latest close , 50 ) and latest ema ( latest close , 50 ) >= latest ema ( latest close , 75 ) and latest ema ( latest close , 75 ) >= latest ema ( latest close , 100 ) and latest ema ( latest close , 100 ) >= latest ema ( latest close , 200 ) and latest ema ( close,20 ) / latest ema ( close,50 ) < 1.03 and latest ema ( close,20 ) / latest ema ( close,50 ) > 1 and latest ema ( close,50 ) / latest ema ( close,75 ) < 1.03 and latest ema ( close,50 ) / latest ema ( close,75 ) > 1 and latest ema ( close,75 ) / latest ema ( close,100 ) < 1.03 and latest ema ( close,75 ) / latest ema ( close,100 ) > 1 and ( {cash} ( quarterly indian promoter and group percentage > 1 quarter ago indian promoter and group percentage or 1 quarter ago indian promoter and group percentage > 2 quarter ago indian promoter and group percentage or 2 quarter ago indian promoter and group percentage > 3 quarter ago indian promoter and group percentage or 3 quarter ago indian promoter and group percentage > 4 quarters ago indian promoter and group percentage or 4 quarters ago indian promoter and group percentage > 5 quarters ago indian promoter and group percentage ) ) and ( {cash} ( latest close >= weekly max ( 52 , weekly high ) * 0.75 and latest close >= weekly max ( 52 , weekly low ) * 1 ) ) and ( {cash} ( latest close > 30 and latest sma ( latest volume , 50 ) > 10000 and market cap >= 300 and latest close > 30 ) ) and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) ) ) "
    df4 = pd.DataFrame(chartink_eng(cond=cond))['nsecode']

    # Convert Series to DataFrame
    df1 = df1.to_frame()
    df2 = df2.to_frame()
    df3 = df3.to_frame()
    df4 = df4.to_frame()

    # Reset index to make the current index a column and create a proper index
    df1.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    df3.reset_index(drop=True, inplace=True)
    df4.reset_index(drop=True, inplace=True)

    # Add 'Cat' column
    df4['Cat'] = "🔥"
    df1['Cat'] = "S"
    df2['Cat'] = "M"
    df3['Cat'] = "L"
    

    # Concatenate DataFrames vertically
    df = pd.concat([df4, df1, df2, df3], axis=0)

    return df


# try:
#     gf = gf()
#     st.write(gf)
#     string = f"### {today_date},"
#     for i in gf['nsecode']:
#         string = string + "NSE:" + i + " , "
#     st.code(string)
# except:
#     st.text("X🔥")

df = get_stocks()

# Buttons for downloading CSV and Excel
st.write(df)
string2 = f"### {today_date}, "
for i in df['nsecode']:
    string2 = string2 + "NSE:" + i + " ,"
st.code(string2)
# df = csv_caller(df)
# st.header('"Things you own end up owning you!"')


unique_values = df['nsecode'].unique()


# Display buttons for each unique value
screen = st.sidebar.text_input("Screener","GAIL")
st.sidebar.link_button("Search on Screener", f"https://www.screener.in/company/{screen}/")
st.sidebar.write('Know Me')
st.sidebar.link_button("Linkedin", url="https://www.linkedin.com/in/yashaswa-varshney")
st.sidebar.link_button("Github", "https://github.com/bbmusa")