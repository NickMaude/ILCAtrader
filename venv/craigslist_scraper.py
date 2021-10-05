import mysql.connector
import asyncio
import requests
import re
import listing
import calendar
import SQL_connection_info
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from random import randint

db = SQL_connection_info.connect()

mycursor = db.cursor()


# idiomatic conversion from month abbreviation to number
def month_to_abriv(s):
    if s == '01':
        return 'Jan'
    if s == '02':
        return 'Feb'
    if s == '03':
        return 'Mar'
    if s == '04':
        return 'Apr'
    if s == '05':
        return 'May'
    if s == '06':
        return 'Jun'
    if s == '07':
        return 'Jul'
    if s == '08':
        return 'Aug'
    if s == '09':
        return 'Sep'
    if s == '10':
        return 'Oct'
    if s == '11':
        return 'Nov'
    if s == '12':
        return 'Dec'
    return 'N/A'


def find_all_postings(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://clsearchengine.com/results.html?cx=000995238168550899204%3A73jyduttcf8&cof=FORID%3A10&ie=UTF-8&q=laser+sailboat#gsc.tab=0&gsc.q=laser%20sailboat&gsc.page='+str(page)

        options = Options()
        options.headless = True
        browser = webdriver.Chrome(os.path.abspath(r'C:\Users\nicho\Desktop\chromedriver_win32\chromedriver.exe'),
                                   options=options)


        browser.implicitly_wait(10)
        browser.get(url)
        wait_for_listings = browser.find_element_by_xpath(r'//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div/div')

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')


        it = 0
        # find link to each posting
        for postings in soup.findAll('div', {'class': 'gsc-webResult gsc-result'}):
            link = postings.find('a', {'class': 'gs-title'})
            href = "" + link.get('href')
            # just the text, not the HTML
            if link.find('b') != None:
                title = link.find('b').text +" "+ link.text


            if len(title) > 75:
                title = title[0:75] + "..."
            title = '<p><a href=' + href + '>' + title + '</a></p>'

            # get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            # if the post is still up and its not a wanted post
            if (data is not None) and ('wanted' not in title):
                mycursor.execute(
                   "INSERT INTO listings (date_posted, title, location ,year ,cost ,image ,date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (data[0], title, data[1], None, data[2], data[3], data[4])
                )
            db.commit()
            it = it + 1
        page += 1
    return list


def get_listing_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    date = soup.find('time', {'class': 'date timeago'})

    # if the post has been removed
    if date is None:
        return None

    numrical_date = date.text.strip()[0:10]
    date_posted = month_to_abriv(numrical_date[5:7]) + " " + numrical_date[8:10] + " ," + numrical_date[0:4]

    price = soup.find('span', {'class': 'price'})

    if price is not None:
        price = price.text

    images = []

    thumbs = soup.findAll('a',{'class': 'thumb'})
    for thumb in thumbs:
        image = thumb.get('href')
        image = '<img src =' + image + '  "Trulli" width="100" height="66">'
        images.append(image)

    location = soup.find('li', {"class": 'crumb area'})
    location = location.find('a').text.title()

    if len(images) == 0:
        images = None
    else:
        # flatten array of html images
        images = ' '.join(map(str, images))

    if price == '$' or price is None:
        price = None
    else:
        price = price.replace(',', '')[1:]

    return date_posted, location, price, images, numrical_date



