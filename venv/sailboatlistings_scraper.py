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
            title = '<p><a href=' + href+'>' + title+'</a></p>'

            #get location, year, cost, image and date posted from listing
            data = get_listing_data(href)

            date_posted = soup.find_all('span', {'class': {'details'}})

            if 'Featured Sailboat' in date_posted[it].text:
                date_posted = date_posted[it].text[25:35]
            else:
                date_posted = date_posted[it].text[16:26]


            # create new listing object and add it to the list
            list.append(listing.listing(date_posted, title,href,data[1],data[0],data[2],data[3]))
            post = listing.listing(date_posted, title, href, data[1], data[0], data[2], data[3])
            #data[1] == date_posted
            #data[0] == location

            mycursor.execute(
                "INSERT INTO listings (date_posted, title, location ,year ,cost ,image) VALUES (%s,%s,%s,%s,%s,%s)",
                (date_posted, title, data[1], data[0], data[2], data[3])
            )
            db.commit()
            #mycursor.execute()
            #print(list[-1])
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
        image = '<img src =' + image + '  "Trulli" width="100" height="66">'

    #return the year, location, cost, image from the posting
    #   year = items[6].string
    #   location = items[10].string
    #   cost = items[11].string

    return (items[6].string,items[10].string,items[11].string,image)
