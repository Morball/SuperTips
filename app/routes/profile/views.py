from app import app
from flask import render_template,session,redirect,url_for,flash
from app.util.authutil.login import login_required
from app.db.models import db, MatchAnalysis,ProfileBet,User
import json
from flask import make_response,jsonify,request
from datetime import datetime 
from app.routes.auth.views import is_valid_email
from hashlib import sha256
@app.get("/profile")
def profile():
    if "user_id" not in session:
        flash("Authorization required",'error')
        return redirect(url_for("login"))
        
        
    ctx=[]
    sub_active=False
    user=User.query.filter_by(id=session["user_id"]).first()
    
    if user.sub_expire>datetime.now():
        sub_active=True
        
        

    profilebets=ProfileBet.query.filter_by(user_id=user.id).all()

    
    for bet in profilebets:
        
        ctx.append(json.loads(MatchAnalysis.query.filter_by(match_id=bet.match_id).first().match_analysis_content))
    
    
    
    
    return render_template("profile.html",ctx=ctx,user=user,sub_active=sub_active)




@app.post("/updateUser")
def update_user():
    if "user_id" not in session:
        return make_response(jsonify({"err":"unauthorised"}),400)
    user=User.query.filter_by(id=session["user_id"]).first()
    username=request.json["username"]
    password=request.json["password"]
    email=request.json["email"]
    
    if username is not None:
        if len(username)>7:
            user.username=username
                
                
    if email is not None:
        if is_valid_email(email):
                user.email=email    
                
                
    if password is not None:
        if len(password)>11:
            user.password=sha256(password.encode("utf-8")).hexdigest()

    db.session.commit()

    session.pop("user_id")
    flash("Info updated. Please log back in","success")
    return redirect(url_for("login"))