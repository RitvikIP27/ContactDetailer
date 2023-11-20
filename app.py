# modules
from flask import Flask, render_template, request, redirect, url_for
from verify_email import verify_email
from flask_mail import Mail, Message
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
        if i["username"] == username:
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
        first_name = request.form.get("first_name").upper()
        last_name = request.form.get("last_name").upper()
        email = request.form.get("email")
        numb = request.form.get("numb")
        new_username = request.form.get("new_username").upper()
        new_pass = request.form.get("new_pass")
        confirm_pass = request.form.get("confirm_pass")
        if new_pass == confirm_pass:
            if check_user(new_username):
                if email_verifier(email):
                    db.execute("insert into table1 values (?, ?, ?, ?, ?, ?, 0)", first_name, last_name, email, numb, new_username, new_pass)
                    data = db.execute("select * from table1;")
                    return render_template("loggedin.html", fname = first_name, lname = last_name, email = email, number = numb, user = new_username, passwrd = new_pass)
                else:
                    return render_template("login.html", emailvernot = True)
            else:
                return render_template("login.html", userex = True)
        else:
            return_template("login.html", passmatchnot = True)
    else:
        user = request.form.get("username").upper()
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
                db.execute("UPDATE table1 SET money = ? WHERE username = ?", money, user)
                return render_template("loggedin.html", fname = i["fname"], lname = i["lname"], email = i["email"], number = i["numb"], user = i["username"], passwrd = i["pass"], money = money, edited = True)

@app.route("/showtable", methods = ["post"])
def table():
    return render_template("database.html", data = db.execute("select * from table1 order by fname, lname;")
)

@app.route("/contact", methods = ["post"])
def contact_page():
    return render_template("contact.html")

@app.route("/rankings", methods = ["post"])
def rankingspage():
    data = db.execute("select * from table1 order by money desc limit 5;")
    n1 = data[0]["fname"] + " " + data[0]["lname"]
    n2 = data[1]["fname"] + " " + data[1]["lname"]
    n3 = data[2]["fname"] + " " + data[2]["lname"]
    n4 = data[3]["fname"] + " " + data[3]["lname"]
    n5 = data[4]["fname"] + " " + data[4]["lname"]
    return render_template("solution.html", first = n1, second = n2, third = n3, fourth = n4, fifth = n5)

@app.route("/submitform", methods = ["post"])
def submitform():
    return render_template("login.html")
    ######### use flask mail, connect smtp etc



