# modules
from flask import Flask, render_template, request, redirect, url_for
from verify_email import verify_email
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///static/data.db")

def email_verifier(email):
    verify = verify_email(email)
    if verify == True:
        return True
    return False

def check_user(username):
    data = db.execute("select * from table1;")
    for i in data:
        if i[5] == username:
            return False
    return True


#INDEX PAGE
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/savedata", methods = ["post"])
def savedata():
    data = db.execute("select * from table1;")
    if request.form.get("gotHelp"):
        first_name = request.form.get("first_name").capitalize()
        last_name = request.form.get("last_name").capitalize()
        email = request.form.get("email")
        numb = request.form.get("numb")
        new_username = request.form.get("new_username").capitalize()
        new_pass = request.form.get("new_pass")
        confirm_pass = request.form.get("confirm_pass")
        if new_pass == confirm_pass:
            if check_user(new_username):
                if email_verifier(email):
                    db.execute("insert into table1 values (?, ?, ?, ?, ?, ?)", first_name, last_name, email, numb, new_username, new_pass)
                    data = db.execute("select * from table1;")
                    return render_template("loggedin.html", fname = first_name, lname = last_name, email = email, number = numb, user = new_username, passwrd = new_pass)
                else:
                    return render_template("login.html", emailvernot = True)
            else:
                return render_template("login.html", userex = True)
        else:
            return_template("login.html", passmatchnot = True)
    else:
        user = request.form.get("username")
        passwrd = request.form.get("password")
        for i in data:
            if i["username"]==user:
                if i["pass"] == passwrd:
                    return render_template("loggedin.html", fname = i["fname"], lname = i["lname"], email = i["email"], number = i["numb"], user = i["username"], passwrd = i["pass"], money = i["money"])
        else:
            return render_template("login.html", correctnot = True)


@app.route("/editamount", methods = ["post"])
def amount():
    data = db.execute("select * from table1;")
    if request.form.get("money"):
        money = request.form.get("money")
        user = request.form.get("username")
        for i in data:
            if i["username"] == user:
                db.execute
                return render_template("loggedin.html", fname = i["fname"], lname = i["lname"], email = i["email"], number = i["numb"], user = i["username"], passwrd = i["pass"], money = i["money"], edited = True)

@app.route("/showtable", methods = ["post"])
def table():
    return render_template("database.html", data = db.execute("select * from table1;")
)

@app.route("/contact", methods = ["post"])
def contact_page():
    return render_template("contact.html")



