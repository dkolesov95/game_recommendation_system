from typing import Union, Tuple

from requests import Response
from requests_html import HTMLSession


class Parser:
    def __init__(self, year):
        self.year = year
        self.session = HTMLSession()

    def get_data_from_page(self, pagination_num) -> Union[Tuple[Response, list[tuple]], Tuple[None, None]]:
        url = f'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected={self.year}&distribution=&sort=desc&view=detailed&page={pagination_num}'
        request = self.session.get(url)

        if request.status_code != 200:
            print(f'get_pagination_count_pages error, status code {request.status_code}')
            return None, None

        games_data = []
        list_wrapper = request.html.find('.browse_list_wrapper')
        for lw in list_wrapper:
            trs = lw.find('tr')
            for tr in trs:
                if not tr.text:
                    continue
                games_data.append(self.collect_game_data(tr))
        return request, games_data

    @staticmethod
    def collect_game_data(game_card: Response) -> tuple:
        title = game_card.find('h3', first=True).text
        platform = game_card.find('.platform', first=True).find('.data', first=True).text
        date = game_card.find('.clamp-details', first=True).find('span')[-1].text
        summary = game_card.find('.summary', first=True).text
        metascore = game_card.find('.clamp-metascore', first=True).find('.metascore_w', first=True).text
        userscore = game_card.find('.clamp-userscore', first=True).find('.metascore_w', first=True).text
        href = game_card.find('a', first=True).attrs['href']
        return title, platform, date, summary, metascore, userscore, href

    # @staticmethod
    # def get_pagination_count_pages(request: Response) -> Union[int, None]:
    #     last_page = request.html.find('.last_page', first=True)
    #     return int(last_page.find('.page_num', first=True).text) if last_page else None
