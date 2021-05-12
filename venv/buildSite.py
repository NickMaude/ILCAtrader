import codecs
import os
import export_table_to_html

def build(order):
    html = r"""
        <html> 
        <head>
            <link rel="stylesheet" href="lasers.css">
        </head>
        <h2>ILCA Finder</h2>
        <section class="container">
            <div class="dropdown">
                <select name="one" class="dropdown-select" onchange="location = this.value;">
                    <option value="">Sorting options</option>
                    <option value="state.html">Sort by State</option>
                    <option value="cost.html">Sort by price (low to high)</option>
                    <option value="year.html">sort by year</option>
                    <option value="date.html">Sort by date_posted </option>
                    <option value="4">Sort by verified post </option>


                </select>
            </div>
        </section>
            """

    if os.path.exists(order+".html"):
        os.remove(order+".html")

    table = export_table_to_html.export(order)

    post = r"</html>"
    html = html+table+post
    output = open(order+".html", "x")
    output.write(html)
