import mysql.connector
import sailingforums_scraper
import sailboatlistings_scraper
import export_to_HTML
import export_to_HTML1

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
        "CREATE TABLE listings (date_posted VARCHAR(50), title VARCHAR(500), location VARCHAR(500), year VARCHAR(10), cost VARCHAR(10),image TEXT(90000), date DATE)"
    )
    sailingforums_scraper.find_all_postings(10)
    sailboatlistings_scraper.find_all_postings(2)
    export_to_HTML1.export()
rebase()