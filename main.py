# -*- coding: utf-8 -*-
import requests
import bs4

save_file = open("waimai_chaoren_data.txt", 'w')

url = "http://waimaichaoren.com/restaurants/21886761/"
resp = requests.get(url)
soup = bs4.BeautifulSoup(resp.text)
##get all
mydivs = soup.findAll("div", { "class" : "clearfix restaurant-food" })
for div in mydivs:
    tmp = div.findAll('li')
    for tmpClass in tmp:
        save_file.write(tmpClass.get_text()+"\n")

##get current area restants name
print("get current area restants name: ")

mydivs = soup.findAll("div", { "class" : "restaurant-introduce fl" })
for div in mydivs:
    tmp = div.findAll('h3')
    for tmpClass in tmp:
        oneRestatantUrl = "http://waimaichaoren.com" + tmpClass.find('a', href=True).get('href')
        oneRest = requests.get(oneRestatantUrl)
        oneSoup = bs4.BeautifulSoup(oneRest.text).find_all("ul", {"class":"clearfix menu-group menu-group-img menu-first-load"})
        save_file.write(tmpClass.get_text()+"\n")
        for oneSoupItem in oneSoup:
            oneSoupItemName = oneSoupItem.find("div", {"class":"meun-item-name"})
            oneSoupItemPrice = oneSoupItem.find("span", {"class":"price"})
            oneSoupItemSellnum = oneSoupItem.find("span", {"class": "fr"})
            save_str = "name: " + oneSoupItemName.get_text() +\
            " price:" + oneSoupItemPrice.get_text() + " sellNum:" + oneSoupItemSellnum.get_text()\
            + "\n"
            save_file.write(save_str)
save_file.close()