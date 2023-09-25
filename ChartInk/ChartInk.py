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
