import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'1234qweasdzxc'

DATABASE = './database.db'

@app.route('/')
def index():
    user = 'Unknown'
    if 'userEmail' in session:
        user = session['userEmail']
        return render_template('index.html',user = user,action = "Logout")
    return render_template('index.html',user = user, action = "")


@app.route('/login', methods = ['GET','POST'])
def login():
    print("Login action")
    if request.method == 'POST':
        print(request.form['userEmail'])
        print(request.form['userPassword'])
        userEmail = request.form['userEmail']
        userPassword = request.form['userPassword']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try :
            sql = 'select * from members where email = ? and password = ?'
            cur.execute(sql,(userEmail,userPassword))
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
            return render_template('login.html',msg = "Please check email or password")        
    return render_template('login.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        userEmail = request.form['userEmail']
        userPassword = request.form['userPassword']
        userName = request.form['userName']
        userPhoneNumber = request.form['userPhoneNumber']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        
        try :
            sql = 'insert into members(email,password,name,phone_number) values (?,?,?,?)'
            print(sql)
            cur.execute(sql, (userEmail,userPassword,userName, userPhoneNumber))
            conn.commit()
            return redirect(url_for('index'))
        
        except:
            print("User exists")
            return render_template('signup.html',msg = "User exists! Try another email or Check your info")        


@app.route('/login_page', methods = ['GET','POST'])
def login_page():
    return render_template('login.html')

@app.route('/sign_up_page')
def sign_up_page():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('userEmail',None)
    return render_template('index.html',action = "")

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)