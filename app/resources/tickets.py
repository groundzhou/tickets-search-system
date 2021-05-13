from flask import Blueprint, request, jsonify
from app.database import get_db

bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')


@bp.route('', methods=['GET', 'POST'])
def tickets():
    """
    供应商资源集合
    """
    if request.method == 'GET':
        db = get_db()
        with db.cursor() as cur:
            cur.execute('''SELECT dairport_code, ddate, dtime, aairport_code, adate, atime,
                airline_code, aircraft, aircraft_type, price, discount, class, cdate
                FROM ground.ticket limit 20''')
            result = cur.fetchall()

        for t in result:
            t['dtime'] = str(t['dtime'])
            t['atime'] = str(t['atime'])
            t['ddate'] = str(t['ddate'])
            t['adate'] = str(t['adate'])
            t['cdate'] = str(t['cdate'])
        return jsonify(result)

    if request.method == 'POST':
        return 'ok'
