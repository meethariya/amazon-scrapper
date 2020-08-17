# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:57:29 2020

@author: Meet Hariya
"""


import requests
from bs4 import BeautifulSoup
import json

dictionary = {}
element = input("enter item to be searched:: ")
url = "https://www.amazon.com/s?k="+element

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
raw = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(raw.text, 'html5lib')
div = soup.findAll("div", {"class": "a-section a-spacing-medium"})

for counter, data in enumerate(div):
    temp = {}
    name = data.findAll("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
    rating = data.findAll("span", {"class": "a-icon-alt"})
    reviews = data.findAll("span", {"class": "a-size-base"})
    price = data.findAll("span", {"class": "a-offscreen"})
    image = data.findAll("img", {"class": "s-image"})
    best = data.findAll("span", {"class": "a-badge-text"})
    if name and rating and reviews and price and image:
        temp['name'] = temp.get('name', name[0].text)
        temp['rating'] = temp.get('rating', rating[0].text.split()[0])
        temp['review'] = temp.get('review', reviews[0].text)
        temp['price'] = temp.get('price', price[0].text)
        temp['image'] = temp.get('image', image[0]['src'])
    else:
        continue
    # only applicable if product is best seller
    if best:
        field = data.findAll("span", {"class": "a-badge-supplementary-text a-text-ellipsis"})
        temp['best seller'] = temp.get('best seller', field[0].text)
    dictionary['product '+str(counter+1)] = dictionary.get('product'+str(counter+1), temp)
json_object = json.dumps(dictionary, indent=4)
# Writing to sample.json
with open("products.json", "w") as outfile:
    outfile.write(json_object)
print("Details successfully stored in 'products.json' file")
