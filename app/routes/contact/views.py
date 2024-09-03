from app import app
from flask import render_template
from app.util.contactform import send_form
from flask import request,redirect,flash,url_for
import re



email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_email(email):
    return re.match(email_pattern, email) is not None



@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name=request.form["firstname"]+" "+request.form["lastname"]
        email=request.form["email"]
        content=request.form["content"]
        if name !="" and email !="" and content !="":
            if is_valid_email(email):

                send_form(name,email,content)
                flash("Message sent.","success")
                return redirect(url_for("contact"))
            else:
                flash("Invalid email address.","error")
                return redirect(url_for("contact"))
        
        
        else:
            flash("Missing fields.","error")
            return redirect(url_for("contact"))
    
    return render_template("contact.html")