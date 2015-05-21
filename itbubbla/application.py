# -*- coding: utf8 -*-
import requests
import xml.etree.ElementTree as et

from flask import Flask, render_template, url_for

app = Flask(__name__)

BASE_URL = 'http://bubb.la/rss/{}'

CATEGORIES = [
    u'Varlden', u'Sverige', u'Blandat',
    u'Media', u'Politik', u'Opinion',
    u'Europa', u'Amerika', u'Asien',
    u'Ekonomi', u'Teknik', u'Vetenskap'
]


def get_itemized_news(url):
    content = requests.get(url).content
    root = et.fromstring(content)

    items = []
    for item in root.iter('item'):
        items.append({
            'title': item.find('title').text,
            'url': item.find('link').text,
            'category': item.find('category').text,
            'date': item.find('pubDate').text
        })
    return items[:20]


@app.route('/', methods=['GET'])
def index():
    items = get_itemized_news(BASE_URL.format('nyheter'))
    categories = [
        {
            'name': name,
            'url': url_for('category', cat=name.lower()),
        } for name in CATEGORIES
    ]

    return render_template(
        'index.html',
        style=url_for('static', filename='style.css'),
        constr=url_for('static', filename='img/construction.gif'),
        menu=url_for('static', filename='img/menu.gif'),
        home=url_for('static', filename='img/home.gif'),
        home_url=url_for('index'),
        mail=url_for('static', filename='img/mail.gif'),
        mail_url='http://bubb.la',
        anacap=url_for('static', filename='img/anacapflag.jpg'),
        categories=categories,
        items=items
    )


@app.route('/<cat>', methods=['GET'])
def category(cat):
    items = get_itemized_news(BASE_URL.format(cat))
    categories = [
        {
            'name': name,
            'url': url_for('category', cat=name.lower()),
        } for name in CATEGORIES
    ]

    return render_template(
        'index.html',
        style=url_for('static', filename='style.css'),
        constr=url_for('static', filename='img/construction.gif'),
        menu=url_for('static', filename='img/menu.gif'),
        home=url_for('static', filename='img/home.gif'),
        home_url=url_for('index'),
        mail=url_for('static', filename='img/mail.gif'),
        mail_url='http://bubb.la',
        anacap=url_for('static', filename='img/anacapflag.jpg'),
        categories=categories,
        items=items
    )


if __name__ == '__main__':
    app.run(debug=True)
