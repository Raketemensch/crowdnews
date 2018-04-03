#!/usr/local/bin/python

import praw
# import requests
import urllib
from bs4 import BeautifulSoup
import ssl
import datetime
from mongoengine import *
context = ssl._create_unverified_context()

connect('mongoengine_test', host='localhost', port=27017)
# db = client['reddit_news']


class Post(Document):
    url = StringField(required=True, max_length=50)
    title = StringField(required=True, max_length=200)
    description = StringField(required=True)
    image = StringField(required=True, max_length=50)
    published = DateTimeField(default=datetime.datetime.now)


# @app.route('/')
def main():
    # create a list of dicts of article metadata
    articleData = {}
    reddit = praw.Reddit(client_id='BdOx6GxL8Q4QYA',
                         client_secret='HFTc7-a2dxldsEUAcOWPpq-mOhs',
                         user_agent='my user agent')

    for submission in reddit.subreddit('news').hot(limit=10):
        url = submission.url
        articleData['url'] = url
        articleData['title'] = submission.title
        article = urllib.request.urlopen(url, context=context).read()
        soup = BeautifulSoup(article, 'html.parser')
        articleData['description'] = soup.find("meta", {"name": "description"})['content']
        try:
            articleData['image'] = soup.find("meta", {"property": "og:image"})['content']
        except Exception:
            articleData['image'] = None

        # print('Adding ' + submission.title + ' to the list.')
        # for key, value in articleData.items():
        #     print(key + ', ' + value)
        #print(articleData)
        posts = db.posts
        result = posts.insert_one(articleData)
        print('One post: {0}'.format(result.inserted_id))

        # articleList.append(articleData)

    # for article in articleList:
    #     # for key, value in article.items():
    #     #     print(key + ', ' + value)
    #     print(article)
    # print(article[1])
    # i = 0
    # while i < len(articleList):
    #     # for article in articleList:
    #     print(articleList[i])
    #     i = i + 1

    # return render_template('news.html', articleList=articleList)
    # return render_template('other.html', articleList=articleList)
    # return('hello')


if __name__ == '__main__':
    # app.run(debug=True)
    main()
