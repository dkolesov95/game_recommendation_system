import time

from metacritic import Parser


def main() -> None:
    # db = connect to db
    for year in range(2015, 2016):
        parser = Parser(year)

        pagination_num = 0
        last_page = 1
        while pagination_num < last_page:
            request, data = parser.get_data_from_page(pagination_num)
            pagination_num += 1
            if request is None:
                continue

            if pagination_num == 1:
                last_page = parser.get_pagination_count_pages(request)

            # db.send_data_to_db(data)
            time.sleep(5)


if __name__ == '__main__':
    main()
