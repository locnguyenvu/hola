import bs4
import requests
from datetime import datetime
from flask import current_app

import app.util as util

class ajax(object):

    BASE_URL = current_app.config.get("investment.dcvfm.crawler.base_url_ajax")

    def __init__(self):
        pass

    def get_nav_price_history(self, fund_name:str):
        request_payload = {
            "action": "filter_old_nav_by_date",
            "selected_fund": fund_name,
            "pageNum": 1
        }
        res = requests.post(self.BASE_URL, data=request_payload)
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
                "nav_price": util.strings.vntodecimal(columns[2].text),
                "net_change": util.strings.todecimal(columns[3].text),
                "probation_change": columns[4].text,
            })
        return price_histories
