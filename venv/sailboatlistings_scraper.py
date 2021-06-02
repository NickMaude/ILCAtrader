import mysql.connector
import asyncio
import requests
import re
import listing
import calendar
import SQL_connection_info

from bs4 import BeautifulSoup
from random import randint

db = SQL_connection_info.connect()

mycursor = db.cursor()


# idiomatic conversion from month abbreviation to number
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
        url = "https://www.sailboatlistings.com/cgi-bin/saildata/db.cgi?db=default&uid=default&manufacturer=Laser&view_records=1&sb=date&so=descend&nh=" + \
              str(page)
        source_code = requests.get(url)
        # just the code, no headers
        plain_text = source_code.text
        # BeautifulSoup objects
        soup = BeautifulSoup(plain_text, "html.parser")

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

    # gather all bolded words
    items = soup.findAll('font', {'face': 'Arial, Helvetica, sans-serif'})
    main_image = soup.find('img', {'class': 'mainsailboatphoto'})

    all_images = []
    images = soup.findAll('img', {'class': 'tns'})

    if main_image is not None:
        main_image = "https://www.sailboatlistings.com/" + main_image.get('src')
        main_image = '<img src =' + main_image + '  "Trulli" width="100" height="66">'
    if images is not None:
        for img in images[:-1]:
            img = "https://www.sailboatlistings.com/" + img.get('src')
            img = '<img src =' + img + '  "Trulli" width="100" height="66">'
            all_images.append(img)
    all_images.insert(0, main_image)
    if len(all_images) == 0:
        all_images = None
    else:
        # flatten array of html images
        all_images = ' '.join(map(str, all_images))

    cost = items[11].string

    if cost == '$' or cost is None:
        cost = None
    else:
        cost = cost.replace(',', '')[1:]
    # return the year, location, cost, image from the posting
    #   year = items[6].string
    #   location = items[10].string
    #   cost = items[11].string
    return items[6].string, items[10].string, cost, all_images
