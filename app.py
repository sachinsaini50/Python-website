from flask import Flask, render_template, request, redirect, url_for, make_response
from flask import session
import mysql.connector as sql

def connect():
    db= sql.connect(database="website", host="localhost", port=3306, user="root", password="sachin@4545")
    cursor = db.cursor()
    return db, cursor

def validate(password: str):
    if len(password)>=8:
        lower = 0
        upper = 0
        number = 0
        special = 0
    
        for i in password:
            if i.islower():
                lower += 1
            if i.isupper():
                upper += 1
            if i.isnumeric():
                number += 1
            if i in "'!@#$%^&*_+,()":
                special += 1
            
        if lower>=1 and upper>=1 and number>=1 and special>=1:
            return True
        return False
    return False

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("nav.html")

@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/index/")
def index():
    return render_template("index.html")

@app.route("/login/")
def login():
    if session.get("islogin"):
        return render_template("index.html")
    return render_template("login.html")

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/aftersignup/", methods=['GET', 'POST'])
def aftersignup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        first_name=request.form.get("first_name")
        last_name=request.form.get("last_name")
        email=request.form.get("email")
        password=request.form.get("password")
        
        db , cursor =connect()
        cmd = f"select email from signup where email='{email}"
        cursor.execute(cmd)
        data = cursor.fetchall()
        
        if data:
            msg = "Email Already Exits"
            return render_template("signup.html",msg=msg)
        
        else:
           # out = password_validation(password)
            
            if validate(password):
                cmd = f"insert into signup values('{first_name}','{last_name}','{email}','{password}')"
                cursor.execute(cmd)
                db.commit()
                msg = "successfully registered. Login to continue"
                return render_template("login.html", msg=msg)
            else:
                msg = "password does not follow password condition"
                return render_template("signup.html",msg=msg)
            
            
@app.route("/afterlogin/", methods=['GET', 'POST'])
def afterslogin():
    if request.method == 'GET':
        return redirect(url_for('login'))
    else:
        email=request.form.get("email")
        password=request.form.get("password")
        
        db , cursor =connect()
        cmd = f"select email from signup where email='{email}' and password = '{password}'"
        cursor.execute(cmd)
        data = cursor.fetchall()
        
        if data:
            session['email']= email
            session['islogin']="True"
            return render_template("index.html",msg=msg)
        
        else:
            msg = "Email or password is incorrect"
            return render_template("login.html",msg=msg)
        

@app.route("/logout/")
def logout():
    del session["email"]
    del session["islogin"]
    return render_template("nav.html")
    
            
if __name__ == "__main__":
    app.run(debug=True, passthrough_errors=True, use_debugger=False, use_reloader=False)
