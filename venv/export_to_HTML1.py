import mysql.connector
import listing
import os

db=mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Fuzyman#123",
    database = "posting",
    port='3306'
)

mycursor = db.cursor()

def is_null(s):
    if s is None:
        return "N/A"
    return str(s)

def export():
    html = r"""
    <html> 
    <head>
        <link rel="stylesheet" href="lasers.css">
    </head>
    <h2>ILCA Finder</h2>
<div class="table-wrapper">
    <table class="fl-table">
        <thead>
            <tr>
                <th> Date Posted</th>
                <th> Title</th>
                <th> Location</th>
                <th> Year </th>
                <th> Cost</th>
                <th> Images</th>
            </tr>
        </thead>
        <body>
        """




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
    post = r"<tbody></table></div></html>"
    html = html + post

    if os.path.exists("lasers.html"):
        os.remove("lasers.html")

    output = open("lasers.html", "x")
    output.write(html)
export()