import codecs
import os
import export_table_to_html

def build(order):
    html = r"""
        <html> 
        <head>
            <link rel="stylesheet" href="lasers.css">
        </head>
        <button class="button" onclick="location.href = 'https://ilcafinder.com/about.html';">About</button>
        <h2>Used Laser Sailboats for sale</h2>
        <section class="container">
            <div class="dropdown">
                <select name="one" class="dropdown-select" onchange="location = this.value;">
                    <option value="">Sorting options</option>
                    <option value="date.html">Sort by date posted </option>
                    <option value="cost.html">Sort by price </option>
                    <option value="state.html">Sort by State</option>
                    <option value="year.html">sort by year</option>
                    <option value="4">verified posts (Coming Soon) </option>
                    <option value="5">create posting (Coming Soon) </option>
                </select>
            </div>
        </section>
            """
    path = 'pages\\'

    if os.path.exists(path+order+".html"):
        os.remove(path+order+".html")

    table = export_table_to_html.export(order)

    post = r"</html>"
    html = html+table+post
    output = open(path+order+".html", "x")
    output.write(html)
