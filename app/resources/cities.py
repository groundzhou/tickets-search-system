from flask import Blueprint, request, jsonify
from app.database import get_db

bp = Blueprint('cities', __name__, url_prefix='/api/cities')


@bp.route('', methods=['GET', 'POST'])
def cities():
    """
    城市资源集合
    :return:
        GET：json格式城市列表
        POST：新城市URL
    """
    if request.method == 'GET':
        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                '''SELECT distinct c.id, c.name, c.code
                FROM ground.city c, ground.airport a
                WHERE c.code = a.city_code
                ORDER BY c.id'''
            )
            result = cur.fetchall()
            # for city in result:
            #     cur.execute('select name, code from ground.airport where city_code = %s', (city['code'],))
            #     city['airports'] = cur.fetchall()
        return jsonify(result)

    if request.method == 'POST':
        return 'ok'


@bp.route('/<string:city_code>', methods=['GET'])
def city(city_code):
    """
    城市资源文档
    :return:
        GET: 获取城市三字 city_code 的资源
    """
    if request.method == 'GET':
        db = get_db()
        with db.cursor() as cur:
            cur.execute('SELECT id, name, code FROM ground.city WHERE code=%s', (city_code,))
            result = cur.fetchall()

        return jsonify(result)
