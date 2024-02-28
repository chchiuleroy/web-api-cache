# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:11:17 2024

@author: User
"""

from flask import Flask, request, jsonify
from flask_caching import Cache
from elasticsearch import Elasticsearch
import mysql.connector, pymongo, secrets
from waitress import serve


app = Flask(__name__)
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = 'D:/cves/cache'
app.config['CACHE_THRESHOLD']=2**20
cache = Cache(app)

es = Elasticsearch("http://127.0.0.1:9200/", timeout = 120, max_retries = 10, retry_on_timeout = True)

mydb = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  port = 3306,
  password = "your_password",
  database = "your_db",
)

mycursor = mydb.cursor()

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["your_db"]
mycol = mydb["your_data"]

app.config['PORT'] = 8080
app.config['API_TOKEN'] = "your_token" ## generating from token_generate with your length

def token_generate(length):
    return secrets.token_hex(length)

'''
insert your ETL or function here
'''

def authenticate(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != app.config['API_TOKEN']:
            return jsonify({'error': 'Authentication failed'}), 401
        return func(*args, **kwargs)
    return wrapper

def make_key():
   user_data = request.get_json()
   return ",".join([f"{key}={value}" for key, value in user_data.items()])

@app.route('/api/v1/products', methods=['POST']) ## or GET
@authenticate
@cache.cached(timeout=0, make_cache_key=make_key, forced_update=True)
def get_products(): 
    data = request.get_json()
    '''
    insert your scripts as follows
    '''
    def process_data(data):
        results = data
        return sum(results, [])
    final = process_data(data)
    return final

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=app.config['PORT'], threads=1) ### you can chage the host for your server
