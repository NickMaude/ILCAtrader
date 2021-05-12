import mysql.connector
import sailingforums_scraper
import sailboatlistings_scraper
import buildSite

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Fuzyman#123",
    database="posting",
    port='3306'
)

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
    sailingforums_scraper.find_all_postings(15)
    sailboatlistings_scraper.find_all_postings(2)

rebase()
build_site()
