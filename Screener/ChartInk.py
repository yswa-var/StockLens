import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings
import time
import numpy as np

warnings.simplefilter('ignore')

class ChartInk:
    """A class for interacting with the ChartInk screener."""

    def get_stocks(cond=None):
        url="https://chartink.com/screener/process"
        """Retrieves stocks that match the given conditions.

        Args:
            cond: A string containing the scan clause.

        Returns:
            A Pandas DataFrame containing the stocks that match the conditions.
        """

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
    df = pd.DataFrame(ChartInk.get_stocks(cond=cond))['nsecode']
    df.to_csv("short_term.csv")

    #mid
    cond = "( {cash} ( weekly ema ( weekly close , 21 ) >= weekly ema ( weekly close , 50 ) and weekly ema ( close,10 ) / weekly ema ( close,21 ) <= 1.03 and weekly ema ( close,10 ) / weekly ema ( close,21 ) > 1 and weekly ema ( close,21 ) / weekly ema ( close,30 ) <= 1.03 and weekly ema ( close,21 ) / weekly ema ( close,30 ) > 1 and weekly ema ( close,30 ) / weekly ema ( close,50 ) <= 1.03 and weekly ema ( close,30 ) / weekly ema ( close,50 ) > 1 and latest close > 30 and latest sma ( latest volume , 50 ) > 3000 and market cap >= 300 and latest close > 30 and weekly ema ( weekly close , 10 ) > weekly ema ( weekly close , 21 ) and weekly ema ( weekly close , 21 ) > weekly ema ( weekly close , 50 ) and weekly ema ( weekly close , 50 ) > weekly ema ( weekly close , 100 ) and weekly close > weekly ema ( weekly close , 50 ) and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) and latest volume > latest sma ( latest volume , 20 ) and quarterly indian public percentage <= 1 quarter ago indian public percentage and 1 quarter ago indian public percentage <= 2 quarter ago indian public percentage and ( {cash} ( quarterly indian promoter and group percentage > 1 quarter ago indian promoter and group percentage or 1 quarter ago indian promoter and group percentage > 2 quarter ago indian promoter and group percentage or 2 quarter ago indian promoter and group percentage > 3 quarter ago indian promoter and group percentage or 3 quarter ago indian promoter and group percentage > 4 quarters ago indian promoter and group percentage or 4 quarters ago indian promoter and group percentage > 5 quarters ago indian promoter and group percentage ) ) ) ) "
    df = pd.DataFrame(ChartInk.get_stocks(cond=cond))['nsecode']
    df.to_csv("mid_term.csv")

    #weekly
    cond = "( {cash} ( latest ema ( latest close , 20 ) >= latest ema ( latest close , 50 ) and latest ema ( latest close , 50 ) >= latest ema ( latest close , 75 ) and latest ema ( latest close , 75 ) >= latest ema ( latest close , 100 ) and latest ema ( latest close , 100 ) >= latest ema ( latest close , 200 ) and latest ema ( close,20 ) / latest ema ( close,50 ) < 1.03 and latest ema ( close,20 ) / latest ema ( close,50 ) > 1 and latest ema ( close,50 ) / latest ema ( close,75 ) < 1.03 and latest ema ( close,50 ) / latest ema ( close,75 ) > 1 and latest ema ( close,75 ) / latest ema ( close,100 ) < 1.03 and latest ema ( close,75 ) / latest ema ( close,100 ) > 1 and ( {cash} ( quarterly indian promoter and group percentage > 1 quarter ago indian promoter and group percentage or 1 quarter ago indian promoter and group percentage > 2 quarter ago indian promoter and group percentage or 2 quarter ago indian promoter and group percentage > 3 quarter ago indian promoter and group percentage or 3 quarter ago indian promoter and group percentage > 4 quarters ago indian promoter and group percentage or 4 quarters ago indian promoter and group percentage > 5 quarters ago indian promoter and group percentage ) ) and ( {cash} ( latest close >= weekly max ( 52 , weekly high ) * 0.75 and latest close >= weekly max ( 52 , weekly low ) * 1 ) ) and ( {cash} ( latest close > 30 and latest sma ( latest volume , 50 ) > 10000 and market cap >= 300 and latest close > 30 ) ) and weekly ema ( weekly close , 50 ) >= weekly ema ( weekly close , 100 ) ) ) "
    df = pd.DataFrame(ChartInk.get_stocks(cond=cond))['nsecode']
    df.to_csv("long_term.csv")

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
    time.sleep(4);
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
        
def csv_caller(x):
    of = pd.read_csv(x)
    of = of.drop(columns=['Unnamed: 0'])
    of["Holding score"] = 0
    of['Holding no'] = 0
    k = 0
    for i in of['nsecode']:
        Score, holding = HoldingScore(i)
        of['Holding score'][k] = Score
        of['Holding no'][k] = holding
        k+=1
    of.fillna(0.0, inplace=True)
    return of

get_stocks()
mid_ga = csv_caller("long_term.csv")
short_ga = csv_caller("short_term.csv")
long_ga = csv_caller("mid_term.csv")
mid_ga['cat'] = "M"
short_ga['cat'] = "S"
long_ga['cat'] = "L"
merged_df = pd.concat([mid_ga, short_ga, long_ga], axis=0)

