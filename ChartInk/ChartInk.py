import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

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

get_stocks()