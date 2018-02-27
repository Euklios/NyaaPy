import requests
from bs4 import BeautifulSoup
from NyaaPy import utils


class Nyaa:
    URI = "http://nyaa.si"

    def search(self, keyword, **kwargs):
        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        request_url = "{}/?f={}&c={}_{}&q={}".format(Nyaa.URI, filters, category, subcategory, keyword)
        if page > 0:
            request_url += "&p={}".format(page)
        r = requests.get(request_url)

        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('table tr')

        return utils.parse_nyaa(rows, limit=None)

    def get(self, id):
        r = requests.get("{}/view/{}".format(Nyaa.URI, id))
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.findAll("div", {"class": "panel", "id": None})
        
        return utils.parse_single(content)

    def get_user(self, username):
        r = requests.get("{}/user/{}".format(Nyaa.URI, username))
        soup = BeautifulSoup(r.text, 'html.parser')

        return utils.parse_nyaa(soup.select('table tr'), limit=None)

    def news(self, number_of_results):
        r = requests.get(Nyaa.URI)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select('table tr')

        return utils.parse_nyaa(rows, limit=number_of_results + 1)
