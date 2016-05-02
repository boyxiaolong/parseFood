# -*- coding: utf-8 -*-
import requests
import bs4
import json

save_file = open("waimai_chaoren_json_data.txt", 'w')

url = "http://waimaichaoren.com/restaurants/21886761/"
resp = requests.get(url)
soup = bs4.BeautifulSoup(resp.text)
##get all

mydivs = soup.findAll("div", { "class" : "clearfix restaurant-food" })
for div in mydivs:
    tmp = div.findAll('li')
    for tmpClass in tmp:
        print(tmpClass.get_text())

##get current area restants name
print("get current area restants name: ")

mydivs = soup.findAll("div", { "class" : "restaurant-introduce fl" })
for div in mydivs:
    tmp = div.findAll('h3')
    for tmpClass in tmp:
        oneRestatantUrl = "http://waimaichaoren.com" + tmpClass.find('a', href=True).get('href')
        oneRest = requests.get(oneRestatantUrl)
        oneSoup = bs4.BeautifulSoup(oneRest.text).find_all("ul", {"class":"clearfix menu-group menu-group-img menu-first-load"})
        tmpMap = {}
        tmpMap["restrantName"] = tmpClass.get_text()
        allFoods = []
        for oneSoupItem in oneSoup:
            tmpOneMap = {}
            oneSoupItemName = oneSoupItem.find("div", {"class":"meun-item-name"})
            oneSoupItemPrice = oneSoupItem.find("span", {"class":"price"})
            oneSoupItemSellnum = oneSoupItem.find("span", {"class": "fr"})
            tmpOneMap["name"] = oneSoupItemName.get_text()
            tmpOneMap["price"] = oneSoupItemPrice.get_text()
            tmpOneMap["sellNum"] = oneSoupItemSellnum.get_text()
            allFoods.append(tmpOneMap)
        tmpMap["restrantFoods"] = allFoods
        encodedjson = json.dumps(tmpMap)
        save_file.write(encodedjson)
save_file.close()