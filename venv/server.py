import mysql.connector
import sailingforums_scraper
import sailboatlistings_scraper
import buildSite
import SQL_connection_info


db = SQL_connection_info.connect()

mycursor = db.cursor()


def build_site():
    buildSite.build("date")
    buildSite.build("state")
    buildSite.build("cost")
    buildSite.build("year")

def rebase():
    mycursor.execute("DROP TABLE IF EXISTS listings")
    mycursor.execute(
        "CREATE TABLE listings (date_posted VARCHAR(50), title VARCHAR(500), location VARCHAR(500), year VARCHAR(10), cost INT(10),image TEXT(90000), date DATE)"
    )
    sailingforums_scraper.find_all_postings(1)
    sailboatlistings_scraper.find_all_postings(1)

rebase()
build_site()
