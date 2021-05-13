from flask import Blueprint, request, jsonify
from app.database import get_db

bp = Blueprint('providers', __name__, url_prefix='/api/providers')


@bp.route('', methods=['GET', 'POST'])
def providers():
    """
    供应商资源集合
    """
    if request.method == 'GET':
        db = get_db()
        with db.cursor() as cur:
            cur.execute('''SELECT id, name, site, icon_path
                           FROM ground.provider''')
            result = cur.fetchall()
        return jsonify(result)

    if request.method == 'POST':
        return 'ok'
