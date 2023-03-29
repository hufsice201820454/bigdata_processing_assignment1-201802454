# bigdata_processing_assignment1-201802454import os
#basic_url ="https://www.kyochon.com/shop/domestic.asp"이며, 교촌 매장은 서울부터 제주까지 총 17개
si_dict = {"서울":1, "부산":2, "대구":3, "인천":4,"광주":5, "대전":6, "울산":7, "세종":8,"경기":9, "강원": 10, "충북":11, "충남":12, "전북":13,"전남": 14, "경북":15, "경남":16,"제주":17}
#각 시마다, 도/군 이 몇개있는지를 매칭하는 딕셔너리 서울 -> 1 -> 25의 형태로 타고가도록 해둠
do_gun_dict = {"1":25, "2":16, "3":8, "4":10, "5":5,"6":5, "7":5, "8":16, "9":44, "10":18,"11":15, "12":17, "13":15, "14":22,"15":24, "16":22, "17":2}
def kyochon(url):
    res = requests.get(url)#request라이브러리
    res.raise_for_status()#교촌 서버에 오류가 존재하는지 확인하는 코드
    soup = BeautifulSoup(res.text, 'html.parser')#BeautifulSoup로 확인
    shop_tag = soup.find(name = 'div', attrs={'class':'shopSchList'})#tag확인 div .shopSchList에 매장 정보가 들어있음
    shop_infos = shop_tag.find_all(name = 'li')#한 페이지에 매장이 여러개이기에, find_all을 통해 li태그를 전부 파싱
    name = []
    si = []
    do = []
    address = []
    phonenum = []
    #각 정보를 담는 리스트
    for shop_info in shop_infos:
        shop_information = []
        shop_name_tag = shop_info.find(name = 'span', attrs = {'class':'store_item'})#li 태그 내에 store_item을 파싱
        try:
            shop_name = shop_name_tag.find(name = 'strong')#매장이름은 strong태그 내에 존재
            shopname = shop_name.get_text()#1
            shop_info_tags = shop_name_tag.find(name = 'em')
            shop = shop_info_tags.find_all(name = 'br')#shop의 주소는 li태그 내 em br태그에 존재하며, li. er br의 태그로 아루어짐
            count = 0#br태그 내에 정보가 여러개, 원하는 정보만을 추출하기 위해 count로 조절예정
            s1 = 'none'
            d1 = 'none'
            a1 = 'none'
            p1 = 'none'
            for shop_address_tag in shop:
                if count == 0:
                    text = shop_address_tag.next_sibling.strip()#br태그는 여러개이기에, 형제노드를 찾아서 들어감
                    text = text.replace('(', '')#count = 0라면, 그 정보안에 주소와, 시, 군/도의 정보가 들어가있음
                    text = text.replace(')', '')#특수문자 () 제거
                    try:#주소 정보가 없을 가능성이 존재하기에, try로 예외처리를 진행
                        location = list(text.split())
                        s1 = location[0]#2
                        d1 = location[1]#3
                        a1 = text#4
                    except IndexError:#indexError인 경우 loop를 다음루프로
                        continue
                else:
                    text = shop_address_tag.next_sibling.strip()#전화번호 
                    p1 = text
                count += 1
            try:
                name.append(shopname)
                si.append(s1)
                do.append(d1)
                address.append(a1)
                phonenum.append(p1)
            except:#한번에 정보를 넣어야 나중에 딕셔너리 상에서 길이가달라 Dataframe으로 변환이 안되는 상황을 막을 수 있음
                name.append('none')
                si.append('none')
                do.append('none')
                address.append('none')
                phonenum.append('none') 
        except AttributeError:#ex) 세종시 무슨 구에 매장이 한개도 없는 경우 크롤링 자체가 불가능하기에, try except으로 예외처리
            continue
        print("크롤링 성공")
    return name, si, do, address, phonenum
print("교촌 크롤링>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
basic_url ="https://www.kyochon.com/shop/domestic.asp"
for i in si_dict.items():
    si_value = i[1]
    si_name = i[0]
    do_value = do_gun_dict[str(si_value) ]
    print("{0}시의 교촌매장을 크롤링 시작합니다".format(si_name))
    for j in range(1, do_value+1):
        url = basic_url + "?sido1={0}&sido2={1}&txtsearch=".format(si_value, j)#si,do dictionary를 이용하여 크롤링 진행할 url을 만듬
        n,s,d,a,p = kyochon(url)
        name = name + n
        si = si + s
        do = do + d
        address = address + a
        phone = phone + p
        time.sleep(1)#서버 과부하시 오류코드 500이 뜨는것을 막기위해 강제로 time.sleep(1)을 진행

dict_data = {'name': name, 'si':si,'do':do,'address':address,'phone':phone}#원할한 데이터 프레임으로의 변환을 위해, 각 정보들을 dictionary로 저장
df_data = pd.DataFrame(dict_data)#dictionary를 데이터프레임으로 변환
df_data.to_csv('C:/Users/이광호/Desktop/programming/itshirt-cat/websraping_basic/kyochon_information.csv',encoding = 'cp949',mode = 'w', index = 'True')#데이터프레임을 csv로 변환
