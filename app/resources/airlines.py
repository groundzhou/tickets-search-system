from flask import Blueprint, request, jsonify
from app.database import get_db

bp = Blueprint('airlines', __name__, url_prefix='/api/airlines')


@bp.route('', methods=['GET', 'POST'])
def airlines():
    """
    机场资源集合
    """
    if request.method == 'GET':
        db = get_db()
        airline_dict = {}
        with db.cursor() as cur:
            cur.execute('''SELECT name, code
                           FROM ground.airline''')
            airline_list = cur.fetchall()
            for i in airline_list:
                airline_dict[i['code']] = i['name']
        return jsonify(dict=airline_dict, list=airline_list)

    if request.method == 'POST':
        return 'ok'
