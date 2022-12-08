import json
import urllib
import requests
from .database import *

# for background scheduling
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from flask import Flask, request
app = Flask(__name__)

# this is the API for fetching data
where = urllib.parse.quote_plus("""
{
    "Year": {
        "$gte": 2012
    }
}
""")
url = 'https://parseapi.back4app.com/classes/Car_Model_List?count=1&limit=0&order=Year&where=%s' % where

# Headers for the online API provided
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z', 
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW' 
}

# Search API
@app.route('/get')
def search():
    year = request.args.get('year')
    make = request.args.get('make')
    model = request.args.get('model')
    return search_db(make,model,year)


# method which will be used to fetch data from API and insert it into local database
def car_model():
        print("Background Process Started")
        total_count = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) 
        count = total_count["count"]
        data_url = url.replace('limit=0','limit='+str(count))
        data = json.loads(requests.get(data_url, headers=headers).content.decode('utf-8')) 
        for i in data["results"]:
            insert(tuple(i.values()))
        commit()
        print("Background Process Stopped")

# before first request from the Flask app, this method will be called which 
# will start the execution of method once a day
@app.before_first_request
def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=car_model, trigger="interval", seconds=86700)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())