import asyncio
import requests
import re
import listing

from bs4 import BeautifulSoup
from random import randint


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

            #date_posted = soup.find_all('span', {'class': {'details'}})



            # create new listing object and add it to the list
            list.append(listing.listing(data[4], title, href, data[1], data[0], data[2], data[3]))
            print(list[-1])
            it = it+1
        page += 1
    return list

def get_listing_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")


    date_posted = soup.find('time', {'class': 'u-dt'}).text
    items = soup.findAll('dl', {'class': 'pairs pairs--columns pairs--fixedSmall'})
    cost = items[0].find('dd').text.strip()
    location = items[1].find('dd').text.strip()
    images=[]

    attachments = soup.findAll('li',{'class':'attachment'})
    for attachment in attachments:
        image = attachment.find('img')
        #print(attachment)
        if image != None:
            image = 'https://sailingforums.com' + image.get('src')
            images.append(str(image))

    if len(images) == 0:
        images = None
    else:
        images = str(images)

    return (None,location,cost,images,date_posted)

def sort_by_datePosted(list):
    for posting in list:
        print(posting)
    list.sort(key=lambda x : x.year, reverse=True)
    for posting in list:
        print(posting)


find_all_postings(2)