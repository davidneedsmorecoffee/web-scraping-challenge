from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# similar to module 09
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# main route that calls in index.html 
# similar to module 09 on craiglist scraping
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# route that starts the scraping
# re: upsert = False; https://docs.mongodb.com/manual/reference/method/db.collection.update/
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=False)
    return redirect("/", code=302) 


if __name__ == "__main__":
    app.run(debug=True)

