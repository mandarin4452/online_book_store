import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
import sqlite3

conn = sqlite3.connect('../database.db')
cur = conn.cursor()
title = ""
author = ""
summary = ""
publisher = ""
pubDate = ""
imageUrl = ""
price = ""


def getBookList():
    key = "AF35301F1A1CA9972DAA684E3ED296C6E96A184DC8D803FDDE45055FF7426D1A"
    url = "http://book.interpark.com/api/bestSeller.api?key=" + \
        key+"&categoryId=100&output=json"

    request = Request(url)
    response = urlopen(request).read().decode('utf-8')

    data = json.loads(response)
    books = data['item']
    print('--------InsertDB---------')
    for book in books:
        # print('title: {}'.format(book['title']))
        # print('author: {}'.format(book['author']))
        # print('summary: {}'.format(book['description']))
        # print('publisher: {}'.format(book['publisher']))
        # print('pubdate: {}'.format(book['pubDate']))
        # print('imgUrl: {}'.format(book['coverLargeUrl']))

        title = book['title']
        author = book['author']
        summary = book['description']
        publisher = book['publisher']
        pubDate = book['pubDate']
        imageUrl = book['coverLargeUrl']
        price = book['priceStandard']
        sql = 'insert into bookLists(title,author,summary,publisher,pubDate,imageUrl,price) values (?,?,?,?,?,?,?)'
        cur.execute(sql, (title, author, summary,
                          publisher, pubDate, imageUrl, price))
        conn.commit()
        conn.close()
    print("Book List Insert Complete")


def insertDB():
    getBookList()

    # sql = 'insert into bookLists(title,author,summary,publisher,pubDate,imageUrl) values (?,?,?,?,?,?)'
    # cur.execute(sql, (title, author, summary, publisher, pubDate, imageUrl))
    # conn.commit()
    # print("Book List Update Complete")

# 중복 삽입 방지


def updateDB():
    print("UpdateDB....")
    conn.close()


cur.execute(
    "SELECT count(*) from bookLists")
count = cur.fetchone()
if(count[0] > 0):
    updateDB()
else:
    insertDB()
