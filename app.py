import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
from datetime import timedelta
import time
import atexit
# from book.bookList import getBookList

# from apscheduler.scheduler import Scheduler

app = Flask(__name__)
app.secret_key = b'1234qweasdzxc'

DATABASE = './database.db'


# # 매일 하루에 한번 bookList DB 업데이트 수정예정
# cron = Scheduler(daemon=True)
# cron.start()


# @cron.interval_schedule(second=10)
# def job_function():
#     getBookList()
#     print("update complete")


@app.route('/')
def index():
    user = 'Unknown'
    if 'userEmail' in session:
        user = session['userEmail']
        return render_template('index.html', user=user, action="Logout")
    return render_template('index.html', user=user, action="")

# 네이버 북 api 요청


def search_book(query):
    CLIENT_ID = "UQDh6UhuGYrRhhQvg3eI"
    CLIENT_SECRET = "UVeMYwBp9v"
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode, quote
    import json
    request = Request(
        'https://openapi.naver.com/v1/search/book?query=' + quote(query))
    request.add_header('X-Naver-Client-Id', CLIENT_ID)
    request.add_header('X-Naver-Client-Secret', CLIENT_SECRET)
    response = urlopen(request).read().decode('utf-8')
    search_result = json.loads(response)
    return search_result


# bestseller list 테스트페이지- 임시
@app.route('/bestseller', methods=['GET'])
def bestseller_page():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    sql = 'select * from bookLists'
    cur.execute(sql)
    bookLists = cur.fetchall()
    print("책리스트", bookLists)
    if bookLists is None:
        conn.close()
        # bookList DB 업데이트 실시
        return False  # 추후 에러페이지..
    else:
        conn.close()
        book = render_template('bestseller.html', data_list=bookLists)
        return book


# search 페이지 - 임시
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_name = request.form['input']
    else:
        search_name = request.args.get('input')
    book_name = search_name
    search_result = search_book('%s' % book_name)['items']
    return render_template('search.html', search_result=search_result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login action")
    if request.method == 'POST':
        print(request.form['userEmail'])
        print(request.form['userPassword'])
        userEmail = request.form['userEmail']
        userPassword = request.form['userPassword']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try:
            sql = 'select * from members where email = ? and password = ?'
            cur.execute(sql, (userEmail, userPassword))
            res = cur.fetchone()
            print(res)
            if res is None:
                conn.close()
                return render_template('login.html')
            else:
                conn.close()
                session['userEmail'] = request.form['userEmail']
                return redirect(url_for('index'))
        except:
            print("No such user")
            return render_template('login.html', msg="Please check email or password")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userEmail = request.form['userEmail']
        userPassword = request.form['userPassword']
        userName = request.form['userName']
        userPhoneNumber = request.form['userPhoneNumber']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        try:
            sql = 'insert into members(email,password,name,phone_number) values (?,?,?,?)'
            print(sql)
            cur.execute(sql, (userEmail, userPassword,
                              userName, userPhoneNumber))
            conn.commit()
            return redirect(url_for('index'))

        except:
            print("User exists")
            return render_template('signup.html', msg="User exists! Try another email or Check your info")


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')


@app.route('/sign_up_page')
def sign_up_page():
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('userEmail', None)
    return render_template('index.html', action="")


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
