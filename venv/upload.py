import FTP_connection_info
from ftplib import FTP
import os

ftp = FTP_connection_info.connect()


def getfile(filename):
    localfile = open("pages\\" + filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()


def placeFile(filename):
    if not os.path.exists("pages\\" + filename):
        return print("UPLOAD.py::PlaceFile-" + filename + " NOT FOUND")
    ftp.storbinary('STOR ' + filename, open("pages\\" + filename, 'rb'))


def upload_All_Files():
    placeFile('date.html')
    placeFile('cost.html')
    placeFile('state.html')
    placeFile('year.html')
    placeFile('lasers.css')
    ftp.quit()
