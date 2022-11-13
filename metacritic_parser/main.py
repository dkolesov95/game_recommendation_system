import time

from metacritic import Parser
from database import Database


def main() -> None:
    db = Database(dbname='YOUR_DATABASE', table_name='YOUR_TABLE_NAME',
                  user='YOUR_USERNAME', password='YOUR_PASSWORD',
                  host='YOUR_HOST', port='YOUR_PORT')
    db.connect_to_db()
    db.create_table()

    for year in range(1996, 2023):
        parser = Parser(year)

        pagination_num = 0
        last_page = 1
        while pagination_num < last_page:
            print(f'year {year}, pagination_num {pagination_num}, last_page {last_page}')

            request, data = parser.get_data_from_page(pagination_num)
            pagination_num += 1
            if request is None:
                print(f'request ERROR year {year}, pagination_num {pagination_num}, last_page {last_page}')
                continue

            if pagination_num == 1:
                last_page = parser.get_pagination_count_pages(request)

            db.insert_data(data)
            time.sleep(10)
    db.close()


if __name__ == '__main__':
    main()
