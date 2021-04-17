#!/usr/bin/env python3

import json
import random
import requests
import threading
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter

# 文件互斥锁
lock = threading.Lock()

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=2))
s.mount('https://', HTTPAdapter(max_retries=2))


# 从ip池获取代理ip
def get_proxy():
    return requests.get("http://localhost:5010/get/").json()


# 删除失效ip
def delete_proxy(proxy):
    requests.get("http://localhost:5010/delete/?proxy={}".format(proxy))

class IPBlockedException(Exception):
    pass


class OtherException(Exception):
    pass


class TimeoutException(Exception):
    pass


def save_point(tp, args, thread_id=None):
    """
    保存断点
    :param thread_id:
    :param tp: 断点类型
    :param args: 参数列表
    """
    with open('../data/checkpoints.json', 'r') as f:
        j = json.load(f)
    if tp == 'prices':
        j[tp] = args
    else:
        j[tp][thread_id] = args
    with open('../data/checkpoints.json', 'w') as f:
        json.dump(j, f)


def load_point(tp):
    """
    读取断点
    :return: 返回断点
    """
    with open('../data/checkpoints.json', 'r') as f:
        j = json.load(f)
        return j[tp]


def get_cities():
    """
    获取主要城市
    :return: json格式城市列表
    """
    headers = {'Host': 'm.ctrip.com',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
               'Accept': 'application/json',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Content-Type': 'application/json',
               'Origin': 'https://m.ctrip.com',
               'Connection': 'keep-alive',
               'Referer': 'https://m.ctrip.com/webapp/flight/schedule/getInlandCity?&_fxpcqlniredt=09031049311771044837',
               'TE': 'Trailers'}
    url = 'https://m.ctrip.com/webapp/flight/schedule/getInlandCity?&_fxpcqlniredt=09031049311771044837'
    response = requests.get(url=url, headers=headers)
    return response.json()


def user_agent():
    """
    随机返回User Agent
    :return: ua list
    """
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    ]
    return random.choice(ua_list)


def get_lowest_prices(source, destination, proxy=None):
    """
    获取今天购买的90天的机票最低价
    :param source: 出发地
    :param destination: 目的地
    :param proxy: 代理
    :return: price list
    """
    weeks = {'周一': '1', '周二': '2', '周三': '3', '周四': '4', '周五': '5', '周六': '6', '周日': '7'}
    url = 'https://m.ctrip.com/restapi/flight/html5/swift/getLowestPriceCalendar?_fxpcqlniredt=09031033112988560870'
    j = {"stype": 1, "dCty": source, "aCty": destination, "flag": None, "start": "", "end": "", "classLevels": ["Y"],
         "head": {"cid": "09031033112988560870", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                  "syscode": "09", "auth": None,
                  "extension": [{"name": "aid", "value": "4899"}, {"name": "sid", "value": "135371"},
                                {"name": "protocal", "value": "https"}]}, "contentType": "json"}
    headers = {
        'Host': 'm.ctrip.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,en-US;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'Content-Length': '335',
        'Origin': 'https://m.ctrip.com',
        'Connection': 'keep-alive',
        'Referer': 'https://m.ctrip.com/html5/flight/swift/domestic/%s/%s/2021-04-30' % (source, destination),
        'TE': 'Trailers'}
    try:
        response = s.post(url=url, headers=headers, json=j,
                          timeout=7)  # , proxies={"https": "http://{}".format(proxy)})
        prices_item = json.loads(response.text).get('prices', [])
        prices = []
        for p in prices_item:
            if not p['price']:
                continue
            line = [source,
                    destination,
                    p['dDate'],
                    weeks[p['dweek']],
                    p['price'],
                    p['discount'],
                    p['flightNo'],
                    p['airline'],
                    p['airname'],
                    datetime.strftime(datetime.now(), '%Y-%m-%d')]
            prices.append(','.join([str(i) for i in line]) + '\n')
    except requests.exceptions.RequestException:
        raise TimeoutException
    except Exception:
        raise OtherException
    else:
        return prices


def request(source, destination, date, proxy):
    """
    爬取一次数据
    :param source: 出发地
    :param destination: 目的地
    :param date: 日期
    :param proxy: 代理
    :return: flight list
    """
    url = 'https://m.ctrip.com/restapi/soa2/14022/flightListSearch?_fxpcqlniredt=09031124412121055112'
    j = {"contentType": "json", "flag": 8,
         "head": {"auth": None, "cid": "09031124412121055112", "ctok": "", "cver": "1.0",
                  "extension": [{"name": "appId", "value": "100008344"}, {"name": "aid", "value": "66672"},
                                {"name": "sid", "value": "508668"}, {"name": "protocal", "value": "https"}],
                  "lang": "01", "sid": "8888", "syscode": "09"}, "preprdid": "",
         "rid": "BBE0515DAAFC4CB09A66E7C70B095E6F", "rtoken": "p0a7d551282e59075325029534b6fbdbd8326e82cfbee",
         "searchitem": [{"accode": destination, "dccode": source, "dtime": date}], "subchannel": None,
         "tid": "{d03ed6d8-24f3-4eab-b26e-2d49ddb865fc}", "trptpe": 1}
    headers = {'Host': 'm.ctrip.com',
               'User-Agent': user_agent(),
               'Accept': 'application/json',
               'Accept-Language': 'zh-CN,en-US;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/json',
               'Origin': 'https://m.ctrip.com',
               'Connection': 'keep-alive',
               'Referer': 'https://m.ctrip.com/html5/flight/swift/domestic/' + source + '/' + destination + '/' + date,
               'TE': 'Trailers'}

    try:
        response = s.post(url=url, headers=headers, json=j, timeout=10, proxies={"https": "http://{}".format(proxy)})
        fltitem = json.loads(response.text).get('fltitem', None)
        flights = []
        if fltitem:
            for f in fltitem:
                if len(f['mutilstn']) == 2:
                    continue

                punctuality = [i['stip'] for i in f['mutilstn'][0]['comlist'] if i['type'] == 2]
                line = [f['mutilstn'][0]['dportinfo']['aport'],
                        f['mutilstn'][0]['dportinfo']['aportsname'],
                        f['mutilstn'][0]['dportinfo']['bsname'],
                        f['mutilstn'][0]['dportinfo']['city'],
                        f['mutilstn'][0]['dportinfo']['cityname'],
                        f['mutilstn'][0]['aportinfo']['aport'],
                        f['mutilstn'][0]['aportinfo']['aportsname'],
                        f['mutilstn'][0]['aportinfo']['bsname'],
                        f['mutilstn'][0]['aportinfo']['city'],
                        f['mutilstn'][0]['aportinfo']['cityname'],
                        f['mutilstn'][0]['basinfo']['aircode'],
                        f['mutilstn'][0]['basinfo']['airsname'],
                        f['mutilstn'][0]['basinfo']['flgno'],
                        f['mutilstn'][0]['craftinfo']['craft'],
                        f['mutilstn'][0]['craftinfo']['kind'],
                        f['mutilstn'][0]['craftinfo']['cname'],
                        f['mutilstn'][0]['dateinfo']['ddate'],
                        f['mutilstn'][0]['dateinfo']['adate'],
                        f['policyinfo'][0]['priceinfo'][0]['price'],
                        f['policyinfo'][0]['priceinfo'][0]['drate'],
                        f['policyinfo'][0]['classinfor'][0]['display'],
                        punctuality[0] if punctuality else '',
                        len(f['mutilstn'][0]['fsitem']),
                        datetime.strftime(datetime.now(), '%Y-%m-%d')]
                flights.append(','.join([str(i) for i in line]) + '\n')
    except requests.exceptions.RequestException as e:
        raise TimeoutException
    except Exception:
        raise OtherException
    else:
        rlt = json.loads(response.text).get('rlt', None)
        if rlt == 508 or rlt == 509:
            raise IPBlockedException
        elif rlt != 0:
            print('No flight', end='\t')
            raise Exception('No flight')
        return flights


def crawl_flights(thread_id):
    # 日期列表
    dates = [datetime.strftime(datetime.now() + timedelta(i), '%Y-%m-%d') for i in range(48)]

    # 城市列表
    with open('../data/mainCities.json') as f:
        cities = list(set([c['code'] for c in json.load(f)['bigCity']]))
        cities.sort()

    # 加载断点
    lock.acquire()
    points = load_point('flights')[thread_id]
    lock.release()
    d, i, j = points[0], points[1], points[2]

    exception = 0
    while d < (thread_id + 1) * 6:
        while i < len(cities):
            while j < len(cities):
                if i == j:
                    j += 1
                    continue
                retry_count = 1  # 重复1次
                proxy = get_proxy().get("proxy")
                while retry_count > 0:
                    try:
                        flights = request(cities[i], cities[j], dates[d], proxy)
                        lock.acquire()
                        with open('../data/flights.csv', 'a') as f:
                            f.writelines(flights)
                        lock.release()
                    except IPBlockedException:
                        print('%s: IP Blocked\t%s\t%s %s --> %s %s\n' %
                              (threading.current_thread().name, dates[d], i, cities[i], j, cities[j]), end='')
                        retry_count -= 1
                    except TimeoutException:
                        print('%s: Time Out\t%s\t%s %s --> %s %s\n' %
                              (threading.current_thread().name, dates[d], i, cities[i], j, cities[j]), end='')
                        retry_count -= 1
                    except:
                        print('%s: Other Error\t%s\t%s %s --> %s %s\n' %
                              (threading.current_thread().name, dates[d], i, cities[i], j, cities[j]), end='')
                        retry_count -= 1
                    else:
                        exception = 0
                        j += 1
                        break
                if retry_count <= 0:
                    print('\tDelete proxy:', proxy)
                    delete_proxy(proxy)
                    exception += 1
                    # if 5 <= exception < 8:
                    #     time.sleep(5)
                    # el
                    if exception >= 8:
                        lock.acquire()
                        save_point('flights', [d, i, j], thread_id)
                        lock.release()
                        return
            j = 0
            i += 1
        i = 0
        d += 1
    lock.acquire()
    save_point('flights', [d, i, j], thread_id)
    lock.release()


def crawl_flights2(thread_id):
    """
    爬取北京到昆明的数据
    :return:
    """
    # 日期列表
    dates = [datetime.strftime(datetime.now() + timedelta(i), '%Y-%m-%d') for i in range(48)]

    # 加载断点
    d = load_point('bjskmg')[thread_id]

    exception = 0
    while d < (thread_id + 1) * 6:
        retry_count = 1  # 重复1次
        proxy = get_proxy().get("proxy")
        while retry_count > 0:
            try:
                flights = request('BJS', 'KMG', dates[d], proxy)
                lock.acquire()
                with open('../data/flights2.csv', 'a') as f:
                    f.writelines(flights)
                lock.release()
            except IPBlockedException:
                print('%s: IP Blocked\t%s\n' % (threading.current_thread().name, dates[d]), end='')
                retry_count -= 1
            except TimeoutException:
                print('%s: Time Out\t%s\n' %
                      (threading.current_thread().name, dates[d]), end='')
                retry_count -= 1
            except:
                print('%s: Other Error\t%s\n' %
                      (threading.current_thread().name, dates[d]), end='')
                retry_count -= 1
            else:
                exception = 0
                d += 1
                break
        if retry_count <= 0:
            print('\tDelete proxy:', proxy)
            delete_proxy(proxy)
            exception += 1
            if exception >= 5:
                lock.acquire()
                save_point('bjskmg', d, thread_id)
                lock.release()
                return
    d += 1

    save_point('bjskmg', d, thread_id)


def crawl_prices():
    """
    爬取今天购买未来90天每日最低价机票
    :return:
    """
    # 城市列表
    with open('../data/mainCities.json') as f:
        cities = list(set([c['code'] for c in json.load(f)['mainCity']]))
        cities.sort()

    # 加载断点
    index = load_point('prices')
    i, j = index[0], index[1]

    exception = 0
    while i < len(cities):
        while j < len(cities):
            if i == j:
                j += 1
                continue
            retry_count = 1  # 重复1次
            # proxy = get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    prices = get_lowest_prices(cities[i], cities[j])
                    with open('../data/prices.csv', 'a') as f:
                        f.writelines(prices)
                except IPBlockedException:
                    print('IP Blocked', i, cities[i], '-->', j, cities[j])
                    retry_count -= 1
                except TimeoutException:
                    print('Time Out', i, cities[i], '-->', j, cities[j])
                    retry_count -= 1
                else:
                    exception = 0
                    j += 1
                    break
            if retry_count <= 0:
                # print('Delete proxy:', proxy)
                # delete_proxy(proxy)
                exception += 1
                if exception >= 5:
                    save_point('prices', [i, j])
                    return
        j = 0
        i += 1

    save_point('prices', [i, j])


if __name__ == '__main__':
    threads = [threading.Thread(target=crawl_flights, name='Thread-%d' % (i + 1), args=(i,)) for i in range(8)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('%s id ended.' % threading.current_thread().name)

    crawl_prices()
