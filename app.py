from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_application")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    
    #make auto generated table a bootstrap style table
    mars_data["Mars_Table"]=mars_data["Mars_Table"].replace('<table border="1" class="dataframe">',"<table class='table table-sm'>")
    
    print("--- MONGO DATA ---")
    print(mars_data)
    print("--- END MONGO DATA ---")
    # Return template and data
    return render_template("index.html", mission_mars=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function in Python File
    mars_data = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to index/home page
    return redirect("/", 302)


if __name__ == "__main__":
    app.run(debug=True)
