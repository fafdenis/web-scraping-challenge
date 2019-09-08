from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:5000/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    try:
        mars_data = mongo.db.mars_data.find_one()
        return render_template("index.html", mars_data=mars_data)
    except:
        return redirect("http://localhost:5000/scrape", code=302)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_data_scrape = scrape_mars.scrape()
    mars_data.update({}, mars_data_scrape, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
