#!/usr/bin/python3
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import pymongo


client = MongoClient('mongodb://localhost:27017/')
mydb = client['mongoengine_test']


app = Flask(__name__)
posts = mydb.posts


@app.route('/')
def main():
    output = []
    for post in mydb.post.find().sort('published', pymongo.DESCENDING):
        output.append(post)
        # print(post)
    return render_template('news.html', output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
