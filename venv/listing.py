class listing:
    def __init__(self,date_posted, title, url, location, year, cost, image):
        self.title = title
        self.date_posted = date_posted
        self.location = location
        self.url = url
        self.year = year
        self.cost = cost
        self.image = image


    def __str__(self):
        return "Date Posted: % s || Title: % s || Location: % s || URL: % s || Year: % s || Cost: % s || Image: % s" % \
               (self.date_posted, self.title, self.location, self.url, self.year,self.cost,self.image)

    def __repr__(self):
        return "Title: % s || Location: % s || URL: % s || Year: % s || Cost: % s || Image: % s" % \
               (self.title, self.location, self.url, self.year,self.cost,self.image)