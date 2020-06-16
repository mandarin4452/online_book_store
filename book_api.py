import requests
import xml.etree.ElementTree as elemTree

api_key = 'B347CF224CD153FA32B826B37A7DB701385D3B611617C07EA8BCE4A5B9314CCF'

r = requests.get('http://book.interpark.com/api/search.api?key=B347CF224CD153FA32B826B37A7DB701385D3B611617C07EA8BCE4A5B9314CCF&query=%EC%82%BC%EA%B5%AD%EC%A7%80')
best = requests.get(f'http://book.interpark.com/api/bestSeller.api?key={api_key}&categoryId=100').text
new = requests.get(f'http://book.interpark.com/api/newBook.api?key={api_key}&categoryId=100').text
recommend = requests.get(f'http://book.interpark.com/api/recommend.api?key={api_key}&categoryId=100').text

def get_books_data(api_type):
    if api_type == "new":
        tree = elemTree.fromstring(new)
    elif api_type == "best":
        tree = elemTree.fromstring(best)
    else:
        tree = elemTree.fromstring(recommend)
    books = []
    for item in tree.findall('./item'):
        title = item.find('title').text
        if len(title) > 15:
            title = title[:15] + "..."
        link = item.find('link').text
        imageUrl = item.find('coverSmallUrl').text
        price = item.find('priceSales').text
        try:
            url = item.find('url').text
        except:
            url = "None"
        author = item.find('author').text
        books.append([title,link,imageUrl,price,url,author])
    return books

def search_books(keyword,query_type,page):
    if query_type[-1] == ".":
        query_type = "all"
    r = requests.get(f'http://book.interpark.com/api/search.api?key={api_key}&query={keyword}&queryType={query_type}&maxResults=10&start={page}')
    tree = elemTree.fromstring(r.text)
    books = []
    for item in tree.findall('./item'):
        title = item.find('title').text
        if len(title) > 15:
            title = title[:15] + "..."
        link = item.find('link').text
        imageUrl = item.find('coverSmallUrl').text
        price = item.find('priceSales').text
        try:
            url = item.find('url').text
        except:
            url = "None"
        author = item.find('author').text
        books.append([title,link,imageUrl,price,url,author])
    return books


