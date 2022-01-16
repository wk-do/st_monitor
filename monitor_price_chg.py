# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 16:01:15 2021

@author: DoW
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread
import time
import threading
# import pyautogui as pg
import queue

BASE_URL = 'https://finance.naver.com/item/main.nhn?code='

st_symbol_list = []
elements = []  # lists
prices = []  # lists
price_list = []  # lists
price_info = []  # lists
is_alive = True
message_queue = queue.Queue()
read_code_lists = []


def getHtml(url):
    resp = requests.get(url)
    time.sleep(1)
    print(url, len(resp.text), ' chars')


def th2_main_loop():
    is_popup = False
    while is_alive:
        # print('th2_main_loop', is_alive)
        received_message = message_queue.get()
        if (received_message == 'ALERT'):
            if (is_popup == False):
                pg_alert = pg.alert(text='conext', title='bad', button='OK')
                is_popup = True;

    return


def dd_view_mode_no_info(res_get_url):
    bs_obj = BeautifulSoup(res_get_url.content, "html.parser")
    # print(bs_obj)
    no_info = bs_obj.find('table', class_='no_info')

    # old_price = no_info.find('td', class_='first')
    # print(old_price.text)
    # high_price = no_info.find('td', class_='sp_txt4')
    # print(high_price.text)
    # begin_price = no_info.find('td', class_='first')
    # print(begin_price.text)
    # low_price = no_info.find('td', class_='sp_txt5')
    # print(low_price.text)

    price_ext_info = []
    count = 0
    for no_info_find in no_info.find_all('span', class_='blind'):
        count += 1
        if count == 3 or count == 4 or count == 7:
            continue

        # old_price, high_price, begin_price, low_price
        price_ext_info.append(no_info_find.text)

    # high_percentage = (price_ext_info[1] - price_ext_info[0]) / price_ext_info[0]
    # low_percnetage = (price_ext_info[3] - price_ext_info[0]) / price_ext_info[0]
    # price_ext_info.append(high_percentage)

    print(price_ext_info)
    return price_ext_info


def dd_view_no_exday(res_get_url):
    bs_obj = BeautifulSoup(res_get_url.content, "html.parser")
    # print(bs_obj)
    no_exday = bs_obj.find('p', class_='no_exday')
    check_data = False

    no_icon = no_exday.find('span', class_="ico plus")
    if no_icon == None:
        no_icon = no_exday.find('span', class_="ico minus")
        if no_icon == None:
            no_icon = ''

    for no_exday_find in no_exday.find_all('span', class_='blind'):
        # print(no_exday_find)
        if not check_data:
            try:
                today_price = no_icon.text + no_exday_find.text
            except:
                today_price = '0'
            check_data = True
        else:
            try:
                today_percent = no_icon.text + no_exday_find.text + '%'
            except:
                today_percent = '0.00%'

    # print(today_price, today_percent)
    # price_list.append(today_percent)
    # return today_price, today_percent
    return today_percent


def dd_view_mode2(res_get_url):
    res_get_url.raise_for_status()
    html = res_get_url.text
    soup = BeautifulSoup(html, 'html.parser')
    today = soup.select_one('#chart_area > div.rate_info > div')
    # print(today)
    # price = today.select_one('.blind')
    # elements.append(today.select('.ico minus'))
    # elements.append(today.select('.ico plus'))
    price = today.select('.blind')
    # chg_minus = today.select('.ico minus')
    # chg_plus = today.select('.ico plus')
    # elements.append(today.select('.blind'))
    # print(elements)

    # for i in elements:
    index = 0
    for i in price:
        if (index != 0):
            prices.append(i.get_text())
        else:
            prices.append(no_icon.text)
        index += 1
        if (index > 2):
            index = 0


def th1_main_loop(arg_codes):
    prices.clear()
    price_list.clear()
    price_info.clear()
    for code in arg_codes:
        response = requests.get(BASE_URL + code)
        price_list.append(dd_view_no_exday(response))
        price_info.append(dd_view_mode_no_info(response))
        time.sleep(1)

    now = datetime.now()
    print(format(now.hour, '02'), '{:02d}'.format(now.minute), '{:02d}'.format(now.second), price_list)

    # a = prices.pop()
    # b = prices.pop()
    # c = prices.pop()
    # print(a, b, c)
    # print(prices.count(), prices.index)
    # if (a < '24750'):
    #    message_queue.put('ALERT')
    #    pg_alert = pg.alert(text='conext', title='bad', button='OK')

    # elif (a > 37800):
    #    pg_alert = pg.alert(text='conext', title='goodtitle', button='OK')
    # print(pg_alert)


def read_code_from_file(open_file):
    f = open(open_file, 'r', encoding='utf-8')
    # f = open('st_angel_list.txt', 'r', encoding='cp949')
    # memo = f.read()
    # read_code_lists = memo.find('peep_code_lists')

    code_lists = []

    while True:
        line = f.readline()
        if not line: break
        if line.find('#') == 0: break
        if len(line) == 1: break

        line = line.strip()
        code_lists.append(line)

    print(code_lists)
    f.close()
    return code_lists


def work(id, start, end, result):
    # total = 0

    # file_name = 'st_angel_list.txt'
    # read_code_lists = read_code_from_file(file_name)

    # read_code_lists = ['069500', '005930', '005950', '348030', '090460', '271940', '101490']
    read_code_lists = ['005950']
    # read_code_lists = ['005950', '090460', '348030']
    print(len(read_code_lists))

    while is_alive:
        # for i in range(start, end):
        #    total += i
        #    result.append(total)
        # print(result)
        time.sleep(2)
        th1_main_loop(read_code_lists)
    return


if __name__ == "__main__":
    START, END = 0, 1000000
    result = list()
    th1 = Thread(target=work, args=(1, START, END, result))
    # th1 = threading.Thread(target=work, args=(1, START, END, result))
    # th1 = threading.Thread(target=th1_main_loop, args=(codes,))
    th1.daemon = True
    th1.start()
    # th1.join()

    # th2 = threading.Thread(target=getHtml, args=('http://google.com',))
    th2 = threading.Thread(target=th2_main_loop)
    th2.daemon = True
    th2.start()
    # g_alert = pg.alert(text='conext', title='bad', button='OK')
    while True:
        is_stop = int(input('if you want to quit, press 9'))
        if is_stop == 9:
            break

    is_alive = False
    th1.join()  # wait until exting the threading

print(f"Result: {sum(result)}")
print('program out')

