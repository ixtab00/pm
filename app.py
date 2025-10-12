from model.model import Credentials, User, init_DB
from model.crypt import Encrypt
from model.auth_utils import send_email
from ext_api.pwnage import collect_results
from flask import Flask, render_template, request, redirect, session
from os import environ
import secrets, time
import asyncio

app = Flask(__name__)
app.config["SECRET_KEY"] = environ["PM_SECRET_KEY"]

db_session = init_DB(environ["PM_DB_PATH"])
encryptor = Encrypt(
    environ["PM_SECRET_KEY"],
    "%Y-%m-%d %H:%M:%S"  
)

OTP_EXPIRATION_TIME = 300

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        email = request.form.get("email", None)
        try:
            assert email
        except AssertionError:
            return "No email address specified", 400
        
        code = str(secrets.randbelow(1000000)).zfill(6)

        session["OTP_CODE"] = code
        session["OTP_TIME"] = time.time()
        session["email"] = email

        email_sent = send_email(email, code)
        if email_sent:
            return redirect("/verify")
        else:
            return "Could not send the email.", 400
        
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "GET":
        return render_template("verify.html")
    elif request.method == "POST":
        code = request.form.get("code", None)
        try:
            assert code
        except AssertionError:
            return "No code specidied.", 400
        
        if session.get("OTP_CODE") == code and time.time() - session.get("OTP_TIME") < OTP_EXPIRATION_TIME:
            session["logged_in"] = True
            user = db_session.query(User).filter(User.email == session.get("email")).first()
            if not user:
                db_session.add(
                    User(
                        email=session.get("email")
                    )
                )
                db_session.commit()
            return redirect("/")

        else:
            return "Invalid or expired code.", 403
       

@app.route("/", methods = ["GET"])
def index():
    if session.get("logged_in", False):
        user = db_session.query(User).filter(User.email==session.get("email")).first()
        if not user:
            return redirect("/login")
        user_id = user.id
        creds = db_session.query(Credentials).filter(Credentials.user_id==user_id).all()
        cred_list = []
        pwd_list = []
        for cred in creds:
            iv, password = cred.iv, cred.password
            dpwd = encryptor.decrypt(password, iv)
            pwd_list.append(dpwd)
            cred_list.append([cred.account, cred.login, dpwd, cred.date, cred.id])
        pwnage = asyncio.run(collect_results(pwd_list))
        for cred in cred_list:
            cred.append(pwnage[cred[2]])
        return render_template("index.html", ctx=cred_list)
    else:
        return redirect("/login")

@app.route("/add", methods = ["GET", "POST"])
def add():
    if session.get("logged_in", False):
        if request.method == "GET":
            return render_template("add_form.html")
        
        elif request.method == "POST":
            account = request.form.get("account", None)
            login = request.form.get("login", None)
            password = request.form.get("password", None)

            if not all([account, login, password]):
                return "Missing parameters", 400
            
            user = db_session.query(User).filter(User.email==session["email"]).all()
            user = user[0] if user else None
            if not user:
                user = User(
                    email = session.get("email")
                )
                db_session.add(
                    user
                )
                db_session.commit()
            user_id = user.id
            db_session.add(encryptor.create_record(
                user_id=user_id,
                account=account,
                login=login,
                pwd=password
            ))
            db_session.commit()
            return redirect("/")
    else:
        return redirect("/login")

@app.route("/delete/<int:cred_id>", methods=["POST"])
def delete(cred_id):
    if session.get("logged_in", False):
        creds = db_session.query(Credentials).filter(Credentials.id==cred_id).first()
        if creds:
            db_session.delete(creds)
            db_session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=environ["PM_DEBUG"])