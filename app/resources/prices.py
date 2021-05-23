from flask import Blueprint, request, jsonify
from app.database import get_db
from datetime import date

bp = Blueprint('prices', __name__, url_prefix='/api/prices')


@bp.route('', methods=['GET', 'POST'])
def lowest_prices():
    """
    供应商资源集合
    """
    if request.method == 'GET':
        dcity_code = request.args.get('dcity', 'BJS')
        acity_code = request.args.get('acity', 'KMG')

        db = get_db()
        with db.cursor() as cur:
            cur.execute(
                '''SELECT *
                FROM ground.low_price
                WHERE dcity_code = %s AND acity_code = %s AND cdate = %s
                ORDER BY ddate
                LIMIT 60''',
                (dcity_code, acity_code, date.today())
            )
            prices = cur.fetchall()
        labels = []
        prices2 = []
        result = {}
        for t in prices:
            labels.append(str(t['ddate'])[5:])
            prices2.append(t['price'])
            t['ddate'] = str(t['ddate'])
            t['cdate'] = str(t['cdate'])
        result['labels'] = labels
        result['prices'] = prices2
        return jsonify(result)

    if request.method == 'POST':
        return 'ok'
