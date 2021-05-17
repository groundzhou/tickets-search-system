from flask import Blueprint, request, jsonify
from app.database import get_db
from app.pridict import Predictor
import time

bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')
predictor = Predictor('bjs_kmg')


@bp.route('', methods=['GET', 'POST'])
def tickets():
    """
    供应商资源集合
    """
    if request.method == 'GET':
        dcity_code = request.args.get('dcity', 'BJS')
        acity_code = request.args.get('acity', 'KMG')
        ddate = request.args.get('ddate', '2021-05-20')

        db = get_db()
        with db.cursor() as cur:
            cur.execute('''SELECT id, flight_num, dcity_code, dairport_code, ddate, dtime, acity_code, aairport_code, adate, atime,
                airline_code, aircraft, aircraft_type, price, discount, class, cdate
                FROM ground.ticket
                WHERE dcity_code = %s AND acity_code = %s AND ddate = %s
                ORDER BY price
                LIMIT 5''', (dcity_code, acity_code, ddate))
            result = cur.fetchall()

        for t in result:
            t['dtime'] = t['dtime'].strftime('%H:%M')
            t['atime'] = t['atime'].strftime('%H:%M')
            t['ddate'] = str(t['ddate'])
            t['adate'] = str(t['adate'])
            t['cdate'] = str(t['cdate'])
            t['discount'] = str(round(t['discount'] * 10, 1))
        time.sleep(0.5)
        return jsonify(result)

    if request.method == 'POST':
        return 'ok'


@bp.route('/<int:tid>', methods=['GET', 'POST'])
def ticket(tid):
    """
    获取机票预测价格
    """
    if request.method == 'GET':
        db = get_db()
        with db.cursor() as cur:
            cur.execute('''
                SELECT id, flight_num, dcity_code, dairport_code, ddate, dtime, acity_code, aairport_code, adate, atime,
                    airline_code, aircraft, aircraft_type, price, discount, class, cdate
                FROM ground.ticket
                WHERE id = %s''', (tid,))
            result = cur.fetchone()

        if result['dcity_code'] == 'BJS' and result['acity_code'] == 'KMG':
            keys = ['airline', 'dmonth', 'dday', 'dweek', 'dhour', 'ahour', 'ahead']
            features = [dict(zip(keys, [result['airline_code'],
                                        int(result['ddate'].month),
                                        int(result['ddate'].day),
                                        result['ddate'].isoweekday(),
                                        int(result['dtime'].hour),
                                        int(result['atime'].hour),
                                        i]))
                        for i in range(48)]
            result['prices_prediction'] = predictor.predict(features)
        return 'ok'
