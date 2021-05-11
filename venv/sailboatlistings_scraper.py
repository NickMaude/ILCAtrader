import mysql.connector
import asyncio
import requests
import re
import listing
import calendar

from bs4 import BeautifulSoup
from random import randint

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Fuzyman#123",
    database="posting",
    port='3306'
)

mycursor = db.cursor()


def month_to_number(s):
    if s == 'Jan':
        return '01'
    if s == 'Feb':
        return '02'
    if s == 'Mar':
        return '03'
    if s == 'Apr':
        return '04'
    if s == 'May':
        return '05'
    if s == 'Jun':
        return '06'
    if s == 'Jul':
        return '07'
    if s == 'Aug':
        return '08'
    if s == 'Sep':
        return '09'
    if s == 'Oct':
        return '10'
    if s == 'Nov':
        return '11'
    if s == 'Dec':
        return '12'
    return 'N/A'


def find_all_postings(max_pages):
    page = 1
    while page <= max_pages:
        url = "https://www.sailboatlistings.com/cgi-bin/saildata/db.cgi?db=default&uid=default&manufacturer=Laser&view_records=1&sb=date&so=descend&nh=" + str(
            page)
        source_code = requests.get(url)
        # just the code, no headers
        plain_text = source_code.text
        # BeautifulSoup objects
        soup = BeautifulSoup(plain_text, "html.parser")
        dates_posted = soup.find_all('span', {'class': {'details'}})

        it = 0
        # find link to each posting
        for link in soup.findAll('a', {'class': 'sailheader'}):
            href = "" + link.get('href')
            # just the text, not the HTML
            title = link.string

            # shorten title if greater that 75chars
            if len(title) > 75:
                title = title[0:75] + "..."
            title = '<p><a href=' + href + '>' + title + '</a></p>'

            # get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            date_posted = soup.find_all('span', {'class': {'details'}})

            if 'Featured Sailboat' in date_posted[it].text:
                date_posted = date_posted[it].text[24:35]
            else:
                date_posted = date_posted[it].text[15:26]

            year = date_posted[-4:]
            day = date_posted[0:2]
            month = date_posted[3:6]
            date_posted = month + " " + day + " ," + year

            number_date = year + "-" + month_to_number(month) + "-" + day


            # data[1] == date_posted
            # data[0] == location

            mycursor.execute(
                "INSERT INTO listings (date_posted, title, location ,year ,cost ,image ,date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (date_posted, title, data[1], data[0], data[2], data[3], number_date)
            )
            db.commit()
            it = it + 1
        page += 1
    return list


def get_listing_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    # gather all boled words
    items = soup.findAll('font', {'face': 'Arial, Helvetica, sans-serif'})
    image = soup.find('img', {'class': 'mainsailboatphoto'})
    # if posting has
    if image != None:
        image = "https://www.sailboatlistings.com/" + image.get('src')
        image = '<img src =' + image + '  "Trulli" width="100" height="66">'

    # return the year, location, cost, image from the posting
    #   year = items[6].string
    #   location = items[10].string
    #   cost = items[11].string

    return (items[6].string, items[10].string, items[11].string, image)
