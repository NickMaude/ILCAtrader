import mysql.connector
import asyncio
import requests
import re
import listing

from bs4 import BeautifulSoup
from random import randint

db=mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Fuzyman#123",
    database = "posting",
    port='3306'
)

mycursor = db.cursor()


def find_all_postings(max_pages):
    #list of listing objects
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
        #find link to each posting
        for item in soup.findAll('div', {'class': 'structItem-title'}):
            link = item.find('a')

            href = "https://sailingforums.com/" + link.get('href')
            # just the text, not the HTML
            title = link.string
            #get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            # create new listing object and add it to the list
            list.append(listing.listing(data[4], title, href, data[1], data[0], data[2], data[3]))

            mycursor.execute(
                "INSERT INTO listings (date_posted, title, location ,url ,year ,cost ,image) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (data[4], title, href, data[1], data[0], data[2], data[3])
            )
            db.commit()

            #print(list[-1])

            it = it+1
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
        location = items[1].find('dd').text.strip()
    else:
        cost = None
        location = None

    attachments = soup.findAll('li',{'class':'attachment'})

    #find images from post attachements
    for attachment in attachments:
        image = attachment.find('img')
        if image != None:
            image = 'https://sailingforums.com' + image.get('src')
            images.append(str(image))

    if len(images) == 0:
        images = None
    else:
        images = str(images)

    return (None,location,cost,images,date_posted)

