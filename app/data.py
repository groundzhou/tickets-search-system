import json
import psycopg2


def get_db():
    """
    获取数据库连接
    """
    db = psycopg2.connect(
        dbname='ground',
        user='ground',
        password='ground',
        host='localhost',
        port=5432
    )

    return db


def insert_data():
    city_file_path = '/home/ground/projects/tickets-search-system/data/mainCities.json'

    db = get_db()
    with open(city_file_path) as f:
        cities = json.load(f)['mainCity']
    with db.cursor() as cur:
        for city in cities:
            cur.execute('INSERT INTO ground.city (name, code) VALUES (%s, %s)', (city['name'], city['code']))

    db.commit()
    db.close()


if __name__ == '__main__':
    insert_data()
