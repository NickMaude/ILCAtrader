import mysql.connector
import listing
import os
import SQL_connection_info

db = SQL_connection_info.connect()

mycursor = db.cursor()


def is_null(s):
    if s is None:
        return "N/A"
    return str(s)


def export(order):
    html = r"""
    <div class="table-wrapper">
        <table width="100%" class="fl-table">
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

    if order == "date":
        mycursor.execute("SELECT * FROM listings ORDER BY date DESC ")
    elif order == "state":
        mycursor.execute("SELECT * FROM listings ORDER BY location DESC")
    elif order == "cost":
        mycursor.execute("SELECT * FROM listings ORDER BY cost")
    elif order == "year":
        mycursor.execute("SELECT * FROM listings ORDER BY year DESC")
    else:
        return print(order + "NOT FOUND")
    result = mycursor.fetchall()
    for posting in result:
        # row orders for reference
        # date = posting[0]
        # title = posting[1]
        # location = posting[2]
        # year = posting[3]
        # cost = posting[4]
        # image = posting[5]
        cost = is_null(posting[4])
        if cost != "N/A":
            cost = "$" + '{:,}'.format(int(cost))

        itemHTML = ("<tr>" +
                    r"<td class='normal' valign='top'>" + is_null(posting[0]) + r"</td>" +
                    r"<td class='normal' valign='top'>" + is_null(posting[1]) + r"</td>" +
                    r"<td class='normal' valign='top'>" + is_null(posting[2]) + r"</td>" +
                    r"<td class='normal' valign='top'>" + is_null(posting[3]) + r"</td>" +
                    r"<td class='normal' valign='top'>" + cost + r"</td>" +
                    r"<td class='normal' valign='top'>" + is_null(posting[5]) + r"</td>" +
                    "</tr>")
        html = html + itemHTML

    post = r"<tbody></table></div>"
    html = html + post
    return html
