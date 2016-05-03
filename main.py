# -*- coding: utf-8 -*-
import requests
import bs4
import json
import re

def get_num_vec_from_str(str):
    return re.findall('\d+', str)

save_file = open("waimai_chaoren_json_data.txt", 'w')
##软件园 高新区 桐梓林
urls = ["http://waimaichaoren.com/restaurants/21886761/"
       , "http://waimaichaoren.com/restaurants/21876902/"
       , "http://waimaichaoren.com/restaurants/21876614/"]

is_already_save_all = False
for url in urls:
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text)
    mydivs = soup.findAll("div", { "class" : "restaurant-introduce fl" })
    for div in mydivs:
        tmpOneRestaunt = div.find('h3', {'class':'ellipsis'})
        if tmpOneRestaunt is None:
            continue

        tmpName = tmpOneRestaunt.get_text()
        tmpDelivery = div.find('p')
        tmpClasses = div.find('p', attrs = {'class':'fl'})
        tmpTotalSell = div.find('dt', attrs={'class':'fl ellipsis'})

        if tmpDelivery is not None:
            tmpDeliveryVec = get_num_vec_from_str(tmpDelivery.get_text())
            if len(tmpDeliveryVec) == 2:
                deliveryBegin = int(tmpDeliveryVec[0])
                deliveryMoney = int(tmpDeliveryVec[1])

        if tmpTotalSell is not None:
            tmpTotalSellNumVec = get_num_vec_from_str(tmpTotalSell.get_text())
            if len(tmpTotalSellNumVec) > 0:
                tmpTotalSell = int(tmpTotalSellNumVec[0])
        else:
            tmpTotalSell = 10

        tmpUrl = div.find('a', href=True)
        if tmpUrl is not None:
            tmpUrl = tmpUrl.get('href')
        else:
            continue

        oneRestatantUrl = "http://waimaichaoren.com" + tmpUrl
        oneRest = requests.get(oneRestatantUrl)
        oneSoup = bs4.BeautifulSoup(oneRest.text).find_all("ul", {"class":"clearfix menu-group menu-group-img menu-first-load"})

        tmpMap = {}
        tmpNameVec = tmpName.split(' ')

        if len(tmpNameVec) >= 2:
            tmpName = tmpNameVec[1]

        tmpMap["restrantName"] = tmpName
        tmpMap["deliveryBegin"] = deliveryBegin
        tmpMap["deliveryMoney"] = deliveryMoney
        tmpMap["classes"] = tmpClasses.get_text()
        tmpMap["totalSell"] = tmpTotalSell

        allFoods = []
        for oneSoupItem in oneSoup:
            tmpOneMap = {}
            oneSoupItemName = oneSoupItem.find("div", {"class":"meun-item-name"})
            oneSoupItemPrice = oneSoupItem.find("span", {"class":"price"})
            sellPrice = 0
            if len(oneSoupItemPrice.get_text()) > 0:
                sellPrices = re.findall("\d+\.\d+", oneSoupItemPrice.get_text())
                if len(sellPrices) > 0:
                    sellPrice = float(sellPrices[0])
            oneSoupItemSellnum = oneSoupItem.find("span", {"class": "fr"})
            sellNum = 0
            if len(oneSoupItemSellnum.get_text()) > 0:
                sellNums = get_num_vec_from_str(oneSoupItemSellnum.get_text())
                if len(sellNums) > 0:
                    sellNum = int(sellNums[0])
            tmpOneMap["name"] = oneSoupItemName.get_text()
            tmpOneMap["price"] = sellPrice
            tmpOneMap["sellNum"] = sellNum
            allFoods.append(tmpOneMap)
        tmpMap["restrantFoods"] = allFoods
        encodedjson = json.dumps(tmpMap)
        save_file.write(encodedjson)
save_file.close()