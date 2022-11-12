from typing import Union

from requests import Response
from requests_html import HTMLSession


class Parser:
    _BASE_URL = 'https://www.metacritic.com'

    def __init__(self, year):
        self.year = year
        self.session = HTMLSession()

    def get_pagination_count_pages(self) -> Union[tuple[Response, None], tuple[Response, int]]:
        url = self._BASE_URL + f'/browse/games/score/metascore/year/all/filtered?year_selected={self.year}&distribution=&sort=desc&view=detailed&page=0'
        request = self.session.get(url)

        if request.status_code != 200:
            print(f'get_pagination_count_pages error, status code {request.status_code}')
            return request, None

        last_page = request.html.find('.last_page', first=True)
        pagi_num = int(last_page.find('.page_num', first=True).text) if last_page else None

        return request, pagi_num
