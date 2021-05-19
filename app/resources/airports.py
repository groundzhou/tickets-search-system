from flask import Blueprint, request, jsonify
from app.database import get_db

bp = Blueprint('airports', __name__, url_prefix='/api/airports')


@bp.route('', methods=['GET', 'POST'])
def airports():
    """
    机场资源集合
    """
    if request.method == 'GET':
        db = get_db()
        airport_dict = {}
        with db.cursor() as cur:
            cur.execute('''SELECT name, code
                           FROM ground.airport''')
            airport_list = cur.fetchall()
            for i in airport_list:
                airport_dict[i['code']] = i['name']
        return jsonify(dict=airport_dict, list=airport_list)

    if request.method == 'POST':
        return 'ok'
