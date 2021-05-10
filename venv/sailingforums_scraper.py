import mysql.connector
import asyncio
import requests
import re
import listing

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


def find_all_postings(max_pages):
    # list of listing objects
    list = []

    page = 1
    while page <= max_pages:
        url = "https://sailingforums.com/forums/Laser_Sales/page-" + str(page)
        source_code = requests.get(url)
        # just the code, no headers
        plain_text = source_code.text
        # BeautifulSoup objects
        soup = BeautifulSoup(plain_text, "html.parser")
        dates_posted = soup.find_all('time', {'data-date-string'})

        it = 0
        # find link to each posting
        for item in soup.findAll('div', {'class': 'structItem-title'}):
            link = item.find('a')

            href = "https://sailingforums.com/" + link.get('href')
            # just the text, not the HTML
            title = link.string
            title = '<p><a href=' + href + '>' + title + '</a></p>'
            # get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            # create new listing object and add it to the list
            list.append(listing.listing(data[4], title, href, data[1], data[0], data[2], data[3]))

            # data[4] = date_posted
            # data[3] = array of images
            # data[2] = cost
            # data[1] = title
            # data[0] = year

            mycursor.execute(
                "INSERT INTO listings (date_posted, title, location ,year ,cost ,image) VALUES (%s,%s,%s,%s,%s,%s)",
                (data[4], title, data[1], data[0], data[2], data[3])
            )
            db.commit()

            # print(list[-1])
            it = it + 1
        page += 1


def get_listing_data(item_url):
    images = []
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    date_posted = soup.find('time', {'class': 'u-dt'}).text
    items = soup.findAll('dl', {'class': 'pairs pairs--columns pairs--fixedSmall'})
    if len(items) > 1:
        cost = items[0].find('dd').text.strip()
        cost = "$" + '{:,}'.format(int(cost))
        location = items[1].find('dd').text.strip()
    else:
        cost = None
        location = None

    attachments = soup.findAll('li', {'class': 'attachment'})

    # find images from post attachments
    for attachment in attachments:
        image = attachment.find('img')
        if image is not None:
            image = 'https://sailingforums.com' + image.get('src')
            image = '<img src =' + image + ' "Trulli" width="100" height="66">'
            images.append(str(image))

    if len(images) == 0:
        images = None
    else:
        # flatten array of html images
        images = ' '.join(map(str, images))

    return None, location, str(cost), images, date_posted
