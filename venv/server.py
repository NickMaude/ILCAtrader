import mysql.connector
import sailingforums_scraper
import sailboatlistings_scraper

db=mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Fuzyman#123",
    database = "posting",
    port='3306'
)

mycursor = db.cursor()

def rebase():
    mycursor.execute("DROP TABLE IF EXISTS listings")
    mycursor.execute(
        "CREATE TABLE listings (date_posted VARCHAR(50), title VARCHAR(150), url VARCHAR(500), location VARCHAR(200), year VARCHAR(10), cost VARCHAR(10),image VARCHAR(5000))"
    )
    sailingforums_scraper.find_all_postings(10)
    sailboatlistings_scraper.find_all_postings(2)
rebase()