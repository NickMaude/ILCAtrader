import mysql.connector
import sailingforums_scraper
import sailboatlistings_scraper
import export_to_HTML

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
        "CREATE TABLE listings (date_posted VARCHAR(50), title VARCHAR(500), location VARCHAR(500), year VARCHAR(10), cost VARCHAR(10),image TEXT(90000))"
    )
    sailingforums_scraper.find_all_postings(13)
    sailboatlistings_scraper.find_all_postings(2)
    export_to_HTML.export()
rebase()