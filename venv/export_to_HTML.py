import SQL_connection_info
import mysql.connector
import listing
import os

db = SQL_connection_info.connect()

mycursor = db.cursor()

def is_null(s):
    if s is None:
        return "None"
    return str(s)

def export():
    html = r"""
    <html> 
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Data</title>
    </head>
    <body>
    <table border=0>
    <tr>
    <td bgcolor=#87cefa class='medium'>date_posted</td>
    <td bgcolor=#87cefa class='medium'>title</td>
    <td bgcolor=#87cefa class='medium'>location</td>
    <td bgcolor=#87cefa class='medium'>year</td>
    <td bgcolor=#87cefa class='medium'>cost</td>
    <td bgcolor=#87cefa class='medium'>image</td>
    </tr>"""

    mycursor.execute("SELECT * FROM listings")
    result = mycursor.fetchall()
    for posting in result:

        # row orders for reference
        # date = posting[0]
        # title = posting[1]
        # location = posting[2]
        # year = posting[3]
        # cost = posting[4]
        # image = posting[5]

        itemHTML =  ("<tr>"+
                     r"<td class='normal' valign='top'>" + is_null(posting[0]) + r"</td>" +
                     r"<td class='normal' valign='top'>" + is_null(posting[1]) + r"</td>" +
                     r"<td class='normal' valign='top'>" + is_null(posting[2]) + r"</td>" +
                     r"<td class='normal' valign='top'>" + is_null(posting[3]) + r"</td>" +
                     r"<td class='normal' valign='top'>" + is_null(posting[4]) + r"</td>" +
                     r"<td class='normal' valign='top'>" + is_null(posting[5]) + r"</td>" +
                     "</tr>")
        html = html + itemHTML
    post = r"</tr></table></body></html>"
    html = html + post

    if os.path.exists("lasers.html"):
        os.remove("lasers.html")

    output = open("lasers.html", "x")
    output.write(html)
