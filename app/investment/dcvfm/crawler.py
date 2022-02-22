import bs4
import requests
import aiohttp
import urllib.parse
from datetime import datetime
from flask import current_app


import app.util as util

class ajax(object):

    BASE_URL = current_app.config.get("investment.dcvfm.crawler.base_url_ajax")

    def __init__(self, session=None):
        """
        Default session is requests.Session
        """
        if session == None:
            session = requests.Session()
        self.session = session
        pass


    def fetch_nav_price_history(self, fund_name:str):
        request_payload = {
            "action": "filter_old_nav_by_date",
            "selected_fund": fund_name,
            "pageNum": 1
        }
        res = self.session.post(self.BASE_URL, data=request_payload)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        price_histories = []
        price_histories_html = soup.find_all("tr")
        for elm in price_histories_html:
            columns = elm.find_all("td")
            if len(columns) == 0:
                continue
            price_histories.append({
                "update_date": datetime.strptime(columns[0].text, "%d/%m/%Y"),
                "dealing_date": datetime.strptime(columns[1].text, "%d/%m/%Y"),
                "nav_price": util.strings.todecimal_dotts(columns[2].text),
                "net_change": util.strings.todecimal(columns[3].text),
                "probation_change": float(columns[4].text.replace("%", "")),
            })
        return price_histories

    async def afetch_nav_price_history(self, fund_name:str) -> list:
        request_payload = {
            "action": "filter_old_nav_by_date",
            "selected_fund": fund_name,
            "pageNum": 1
        }
        resp = await self.session.request(method="POST", url=self.BASE_URL, data=request_payload)
        resp.raise_for_status()
        html = await resp.text()
        soup = bs4.BeautifulSoup(html, 'html.parser')

        price_histories = []
        price_histories_html = soup.find_all("tr")
        for elm in price_histories_html:
            columns = elm.find_all("td")
            if len(columns) == 0:
                continue
            price_histories.append({
                "update_date": datetime.strptime(columns[0].text, "%d/%m/%Y"),
                "dealing_date": datetime.strptime(columns[1].text, "%d/%m/%Y"),
                "nav_price": util.strings.todecimal_dotts(columns[2].text),
                "net_change": util.strings.todecimal(columns[3].text),
                "probation_change": float(columns[4].text.replace("%", "")),
            })
        return price_histories

