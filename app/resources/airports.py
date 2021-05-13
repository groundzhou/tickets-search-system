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
        with db.cursor() as cur:
            cur.execute('''SELECT a.id, a.name, a.code, a.city_code, c.name city_name
                           FROM ground.airport a, ground.city c 
                           WHERE a.city_code = c.code''')
            result = cur.fetchall()
        return jsonify(result)

    if request.method == 'POST':
        return 'ok'
