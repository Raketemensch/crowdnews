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


class Post(Document):
    url = StringField(required=True, max_length=500)
    title = StringField(required=True, max_length=500)
    description = StringField(required=True)
    image = StringField(required=True, max_length=500)
    redditLink = StringField(required=True, max_length=500)
    published = DateTimeField(default=datetime.datetime.now)
    meta = {'strict': False}


def main():
    reddit = praw.Reddit(client_id='BdOx6GxL8Q4QYA',
                         client_secret='HFTc7-a2dxldsEUAcOWPpq-mOhs',
                         user_agent='my user agent')

    for submission in reddit.subreddit('news').hot(limit=50):
        url = submission.url
        print(url)
        title = submission.title
        redditLink = 'http://reddit.com/' + submission.id
        print(redditLink)
        try:
            article = urllib.request.urlopen(url, context=context).read()
        except Exception:
            continue
        soup = BeautifulSoup(article, 'html.parser')
        try:
            description = soup.find("meta", {"name": "description"})['content']
        except Exception:
            description = 'Description meta tag not found.'
        try:
            image = soup.find("meta", {"property": "og:image"})['content']
        except Exception:
            image = 'None'

        post = Post(
            url=url,
            title=title,
            description=description,
            image=image,
            redditLink=redditLink
        )

        if not Post.objects(url=url):
            post.save()


if __name__ == '__main__':
    main()
