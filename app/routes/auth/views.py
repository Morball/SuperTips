from app import app
from flask import render_template,request, flash,redirect,url_for,session
from hashlib import sha256
from app.db.models import User,db
import re


def is_valid_email(email):
    # Regular expression for basic email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)


@app.route("/login", methods=["GET","POST"])
def login():
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        passwd_hash=sha256(password.encode("utf-8")).hexdigest()

        if username is None:
            flash('Username cannot be none', 'error')
            return redirect(url_for('login'))
        if password is None:
            flash('Password cannot be none', 'error')
            return redirect(url_for('login'))
        
        user=User.query.filter_by(username=username, password=passwd_hash).first()
        if user is None:
            flash('Incorrect login details', 'error')
            return redirect(url_for('login'))



        ip_address=request.headers.get("X-Forwarded-For",request.remote_addr)
        user.ip=ip_address    #update to latest ip address login
        db.session.commit()
        session["user_id"]=user.id
        return redirect(url_for('profile'))
        
    return render_template("signIn.html")    
    

@app.route("/register", methods=["GET","POST"])
def register():
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_conf=request.form["password_conf"]
        signup_ref=request.form["signup_ref"]
        ip_address=request.headers.get("X-Forwarded-For",request.remote_addr)

        if User.query.filter_by(email=email).first() is not None:
            flash('This email is already in use', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first() is not None: 
            flash('This username is already in use', 'error')
            return redirect(url_for('register'))       
        
        
        if len(username) < 8:
            flash('Username must be at least 8 characters long', 'error')
            return redirect(url_for('register'))
        if len(password) < 12:
            flash('Password must be at least 12 characters long', 'error')
            return redirect(url_for('register'))
        if not is_valid_email(email):
            flash('Invalid email address', 'error')
            return redirect(url_for('register'))
        if password!=password_conf:
            flash('Passwords don\'t match', 'error')
            return redirect(url_for('register'))

        if signup_ref !="":
            refferal=User.query.filter_by(ref_code=signup_ref).first()
            if refferal is None:
                flash('Refferal not found', 'error')
                return redirect(url_for('register'))
            refferal.refs=refferal.refs+1
            db.session.commit()
        
        passwd_hash=sha256(password.encode("utf-8")).hexdigest()
        
        
        newuser=User(username=username,email=email,password=passwd_hash, signup_ref=signup_ref,ip=ip_address)
        db.session.add(newuser)
        db.session.commit()
        flash('Sign up successful', 'success')
        return redirect(url_for('login'))
    
    
    
    
    
    return render_template("signUp.html")







@app.get("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id")
        flash('Logged out', 'success')
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))