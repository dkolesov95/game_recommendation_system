import psycopg2


class Database:
    def __init__(self, dbname, table_name, user, password, host, port):
        self.dbname = dbname
        self.table_name = table_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connect = None
        self.cursor = None

    def connect_to_db(self):
        self.connect = psycopg2.connect(dbname=self.dbname, user=self.user,
                                        password=self.password, host=self.host,
                                        port=self.port)
        self.cursor = self.connect.cursor()

    def create_table(self):
        expression = f'CREATE TABLE IF NOT EXISTS {self.table_name} (' \
                     'id SERIAL PRIMARY KEY, ' \
                     'name varchar(200) NOT NULL, ' \
                     'platform varchar(20) NOT NULL, ' \
                     'date varchar(20) NOT NULL, ' \
                     'summary varchar(5000) NOT NULL, ' \
                     'metascore varchar(4) NOT NULL, ' \
                     'userscore varchar(5) NOT NULL, ' \
                     'href varchar(200) NOT NULL)'
        self.cursor.execute(expression)
        self.connect.commit()

    def insert_data(self, data):
        for d in data:
            self.cursor.execute(f'INSERT INTO {self.table_name} (name, platform, date, '
                                'summary, metascore, userscore, href) VALUES %s' % (d,))
        self.connect.commit()

    def close(self):
        self.cursor.close()
        self.connect.close()
