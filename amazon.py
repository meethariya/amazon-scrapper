# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 09:57:29 2020

@author: Meet Hariya
"""

import re
import requests
from bs4 import BeautifulSoup
import ssl
import json
from automator import *

# =============================================================================
# These will manage certificates of websites for python
# =============================================================================
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

dictionary = {}


# =============================================================================
#  This will check the exixtance of value and then append it to temp dictonary
# or else it will provide a value as null
# =============================================================================
def appender(temp, text, fun):
    if text:
        temp[fun] = temp.get(fun, text[0])
    else:
        temp[fun] = temp.get(fun, "Null")


# =============================================================================
# Enter element to be searched or press enter to search for mens sunglasses as
# default
# =============================================================================
element = input("enter item to be searched:: ")
if element == "":
    url = "https://www.amazon.com/s?k=mens+sunglasses&crid=236UYYWAA3GDI&sprefix=mens+sun%2Caps%2C1679&ref=nb_sb_ss_i_1_8"
else:
    # using function from automater to open amazon.com and search
    url = searcher(element)
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
detail_page = requests.session().get(url, headers=HEADERS, verify=False, allow_redirects=True)
raw = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(raw.text, 'html5lib')
div = soup.findAll("div", {"class": "a-section a-spacing-medium"})

for counter, data in enumerate(div):
    temp = {}
    # name
    name = data.findAll("span", {"class": "a-size-base-plus a-color-base a-text-normal"})
    n = re.findall('>(.+)<', str(name))
    appender(temp, n, 'name')
    # rating
    rating = data.findAll("span", {"class": "a-icon-alt"})
    r = re.findall('>(.+)<', str(rating))
    if r:
        r = r[0].split()
        appender(temp, r, 'rating')
    # review
    reviews = data.findAll("span", {"class": "a-size-base"})
    rw = re.findall('>(.+[0-9])<', str(reviews))
    appender(temp, rw, 'reviews')
    # price
    price = data.findAll("span", {"class": "a-offscreen"})
    p = re.findall('>(.+?)<', str(price))
    appender(temp, p, 'price')
    # image
    image = data.findAll("img", {"class": "s-image"})
    img = re.findall('src=\"(.+?jpg)', str(image))
    appender(temp, img, 'image')
    # only applicabel if product is best seller
    best = data.findAll("span", {"class": "a-badge-text"})
    if best:
        field = data.findAll("span", {"class": "a-badge-supplementary-text a-text-ellipsis"})
        f = re.findall('>(.+)<', str(field))
        appender(temp, f, 'best seller')
    # appending the temp dict in dictonary with key as "product number"
    dictionary['product '+str(counter+1)] = dictionary.get('product'+str(counter+1), temp)
# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("products.json", "w") as outfile:
    outfile.write(json_object)
