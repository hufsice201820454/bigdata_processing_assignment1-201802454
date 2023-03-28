import os
import pandas as pd
import math
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import requests
import time
import re

si_dict = {
    "서울":1, "부산":2, "대구":3, "인천":4,
    "광주":5, "대전":6, "울산":7, "세종":8,
    "경기":9, "강원": 10, "충북":11, "충남":12, "전북":13,
    "전남": 14, "경북":15, "경남":16,"제주":17
}

do_gun_dict = {
    "1":25, "2":16, "3":8, "4":10, "5":5,
    "6":5, "7":5, "8":16, "9":44, "10":18,
    "11":15, "12":17, "13":15, "14":22,
    "15":24, "16":22, "17":2
}

def kyochon(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    shop_tag = soup.find(name = 'div', attrs={'class':'shopSchList'})
    shop_infos = shop_tag.find_all(name = 'li')
    name = []
    si = []
    do = []
    address = []
    phonenum = []
    for shop_info in shop_infos:
        shop_information = []
        shop_name_tag = shop_info.find(name = 'span', attrs = {'class':'store_item'})
        try:
            shop_name = shop_name_tag.find(name = 'strong')
            shopname = shop_name.get_text()#1
            shop_info_tags = shop_name_tag.find(name = 'em')
            shop = shop_info_tags.find_all(name = 'br')
            count = 0
            s1 = 'none'
            d1 = 'none'
            a1 = 'none'
            p1 = 'none'
            for shop_address_tag in shop:
                if count == 0:
                    text = shop_address_tag.next_sibling.strip()
                    text = text.replace('(', '')
                    text = text.replace(')', '')
                    try:
                        location = list(text.split())
                        s1 = location[0]#2
                        d1 = location[1]#3
                        a1 = text#4
                    except IndexError:
                        continue
                else:
                    text = shop_address_tag.next_sibling.strip()
                    p1 = text
                count += 1
            try:
                name.append(shopname)
                si.append(s1)
                do.append(d1)
                address.append(a1)
                phonenum.append(p1)
            except:
                name.append('none')
                si.append('none')
                do.append('none')
                address.append('none')
                phonenum.append('none') 
        except AttributeError:
            continue
        print("크롤링 성공")

    return name, si, do, address, phonenum
print("교촌 크롤링>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
basic_url ="https://www.kyochon.com/shop/domestic.asp"

name = []
si = []
do = []
address = []
phone = []

for i in si_dict.items():
    si_value = i[1]
    si_name = i[0]
    do_value = do_gun_dict[str(si_value) ]
    print("{0}시의 교촌매장을 크롤링 시작합니다".format(si_name))
    for j in range(1, do_value+1):
        url = basic_url + "?sido1={0}&sido2={1}&txtsearch=".format(si_value, j)
        n,s,d,a,p = kyochon(url)
        name = name + n
        si = si + s
        do = do + d
        address = address + a
        phone = phone + p
        time.sleep(1)

dict_data = {
    'name': name,
    'si':si,
    'do':do,
    'address':address,
    'phone':phone
}
print(len(name))
print(len(si))
print(len(do))
print(len(address))
print(len(phone))
df_data = pd.DataFrame(dict_data)
df_data.to_csv('C:/Users/이광호/Desktop/programming/itshirt-cat/websraping_basic/kyochon_information.csv',encoding = 'cp949',mode = 'w', index = 'True')
