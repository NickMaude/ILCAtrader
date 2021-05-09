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
        url = "https://www.sailboatlistings.com/cgi-bin/saildata/db.cgi?db=default&uid=default&manufacturer=Laser&view_records=1&sb=date&so=descend&nh=" + str(page)
        source_code = requests.get(url)
        # just the code, no headers
        plain_text = source_code.text
        # BeautifulSoup objects
        soup = BeautifulSoup(plain_text, "html.parser")
        dates_posted = soup.find_all('span', {'class': {'details'}})

        it = 0
        #find link to each posting
        for link in soup.findAll('a', {'class': 'sailheader'}):
            href = "" + link.get('href')
            # just the text, not the HTML
            title = link.string

            #get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            date_posted = soup.find_all('span', {'class': {'details'}})

            if 'Featured Sailboat' in date_posted[it].text:
                date_posted = date_posted[it].text[25:35]
            else:
                date_posted = date_posted[it].text[16:26]


            # create new listing object and add it to the list
            list.append(listing.listing(date_posted, title,href,data[1],data[0],data[2],data[3]))
            print(list[-1])
            it = it+1
        page += 1
    return list

def get_listing_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    #gather all boled words
    items = soup.findAll('font', {'face': 'Arial, Helvetica, sans-serif'})
    image = soup.find('img',{'class':'mainsailboatphoto'})
    #if posting has
    if image != None:
        image = "https://www.sailboatlistings.com/" + image.get('src')

    #return the year, location, cost, image from the posting
    #   year = items[6].string
    #   location = items[10].string
    #   cost = items[11].string

    return (items[6].string,items[10].string,items[11].string,image)

def sort_by_datePosted(list):
    for posting in list:
        print(posting)
    list.sort(key=lambda x : x.year, reverse=True)
    for posting in list:
        print(posting)


find_all_postings(2)