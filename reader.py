#!/usr/bin/python3
from flask import Flask
from flask import render_template
from flask import request
from pymongo import MongoClient
import pymongo


client = MongoClient('mongodb://localhost:27017/')
mydb = client['crowdnews']


app = Flask(__name__)
posts = mydb.posts


@app.route('/', methods = ['POST', 'GET'])
def main():
    output = []
    if len(request.form) > 0:
        categoryName =  request.form["category"]
        print(categoryName)
        for post in mydb.post.find({"category": categoryName}).sort('published', pymongo.DESCENDING):
                    output.append(post)
        return render_template('news.html', output=output)
    else:
        for post in mydb.post.find({"category": "news"}).sort('published', pymongo.DESCENDING):
            output.append(post)
        return render_template('news.html', output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
