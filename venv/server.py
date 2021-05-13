import mysql.connector
import sailingforums_scraper
import sailboatlistings_scraper
import buildSite
import SQL_connection_info
import schedule
from time import time, sleep


db = SQL_connection_info.connect()

mycursor = db.cursor()

def run_server():
    rebase()
    build_site()

def build_site():
    buildSite.build("date")
    buildSite.build("state")
    buildSite.build("cost")
    buildSite.build("year")

def rebase():
    print('rebaseing..')
    mycursor.execute("DROP TABLE IF EXISTS listings")
    mycursor.execute(
        "CREATE TABLE listings (date_posted VARCHAR(50), title VARCHAR(500), location VARCHAR(500), year VARCHAR(10), cost INT(10),image TEXT(90000), date DATE)"
    )
    sailingforums_scraper.find_all_postings(10)
    sailboatlistings_scraper.find_all_postings(1)

#run_server()
build_site()