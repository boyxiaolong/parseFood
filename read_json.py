# -*- coding: utf-8 -*-
import json
from pprint import pprint

with open('waimai_chaoren_json_data.txt') as data_file:
    data = json.load(data_file)

pprint(data)