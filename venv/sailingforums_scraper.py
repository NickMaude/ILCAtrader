import mysql.connector
import asyncio
import requests
import re
import listing
from datetime import date

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
        url = "https://sailingforums.com/forums/Laser_Sales/page-" + str(page)
        source_code = requests.get(url)
        # just the code, no headers
        plain_text = source_code.text
        # BeautifulSoup objects
        soup = BeautifulSoup(plain_text, "html.parser")

        # find link to each posting
        for item in soup.findAll('div', {'class': 'structItem-title'}):
            link = item.find('a')

            href = "https://sailingforums.com/" + link.get('href')
            # just the text, not the HTML
            title = link.string.lower().title()
            if len(title) > 60:
                title = title[0:60] + "..."
            title = '<p><a href=' + href + '>' + title + '</a></p>'

            # get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            # indexes for reference
            # data[5] = numrical_date
            # data[4] = date_posted
            # data[3] = array of images
            # data[2] = cost
            # data[1] = title
            # data[0] = year

            mycursor.execute(
                "INSERT INTO listings (date_posted, title, location ,year ,cost ,image ,date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (data[4], title, data[1], data[0], data[2], data[3], data[5])
            )
            db.commit()
        page += 1


# convert date (month name, day, year) to SQL Date type (month number-day-year)
#   ex - May 05, 2021 to 2021-
def get_numrical_date(date_posted):
    if len(date_posted) > 15:
        return date.today().strftime("%Y-%m-%d")

    year = date_posted[-4:]
    month = month_to_number(date_posted[0:3])
    day = date_posted[4:6]
    if ',' in day:
        day = '0' + day[0]
    return year + '-' + month + '-' + day

# scrape data from the individual listings page
def get_listing_data(item_url):
    # array of image hrefs
    images = []

    # all the source code
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    # date to be displayed
    date_posted = soup.find('time', {'class': 'u-dt'}).text
    # SQL date type to be searched
    numerical_date = get_numrical_date(date_posted)

    # find cost and location if provided
    items = soup.findAll('dl', {'class': 'pairs pairs--columns pairs--fixedSmall'})
    if len(items) > 0:
        cost = items[0].find('dd').text.strip()
        #cost = "$" + '{:,}'.format(int(cost))
        location = items[1].find('dd').text.strip().lower().title()
    else:
        cost = None
        location = None

    attachments = soup.findAll('li', {'class': 'attachment'})

    # if there is image attachments then there is no need to search for other images
    is_attachment = False

    # find images from post attachments
    for attachment in attachments[0:10]:
        image = attachment.find('img')
        if image is not None:
            is_attachment = True
            image = 'https://sailingforums.com' + image.get('src')
            image = '<img src =' + image + ' "Trulli" width="100" height="66">'
            images.append(str(image))

    # find images in post if there are no image attachments
    if not is_attachment:
        pictures = soup.find('div', {'class': 'bbWrapper'})
        if pictures is not None:
            pictures = pictures.findAll('img', {'class': 'bbImage'})
            if pictures is not None:
                for picture in pictures:
                    picture = 'http://sailingforums.com' + picture.get('src')
                    picture = '<img src =' + picture + ' "Trulli" width="100" height="66">'
                    images.append(str(picture))

    if len(images) == 0:
        images = None
    else:
        # flatten array of html images
        images = ' '.join(map(str, images))

    return None, location, cost, images, date_posted, numerical_date
