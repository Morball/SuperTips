from app import app
from flask import render_template,flash,redirect,url_for,request
from app.db.models import User,Subs_Bought,MOTD
from datetime import datetime, timedelta
from flask import session,make_response,jsonify
import json
from app.db.models import MatchAnalysis,db,AnalysisReport
@app.route("/admin",methods=["GET","POST"])
def admin():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    all_analysis_reports=AnalysisReport.query.all()
    thirty_days_ago = datetime.now() - timedelta(days=30)

    subs_this_month=Subs_Bought.query.filter(Subs_Bought.date >= thirty_days_ago).all()
    all_users=User.query.all()[-8:]
    active_subs=User.query.filter(User.sub_expire>datetime.now()).all()
    est_earnings=0
    all_subs=Subs_Bought.query.all()
    motd=MOTD.query.all()[-1]
    expected_costs=0.33*len(MatchAnalysis.query.filter(MatchAnalysis.date_created>=thirty_days_ago).all())
    for sub in subs_this_month:
        if sub.sub_type==1:
            est_earnings=est_earnings+25
        elif sub.sub_type==2:
            est_earnings=est_earnings+60    
        if sub.sub_type==3:
            est_earnings=est_earnings+100    
    ctx={
        "users_count":len(all_users),
        "estimated_earnings":est_earnings,
        "active_subs":len(active_subs),
        "est_costs":expected_costs,
        "users":all_users,
        "subs":all_subs,
        "now":datetime.now(),
        "motd":motd,
        "reports":all_analysis_reports
    }
    
    
    if request.method=="GET":
        return render_template("admin.html",ctx=ctx)
    
    
    
    
@app.post("/admin/updateUser")
def updateuser():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    user=User.query.filter_by(id=request.form["id"]).first()
    user.username=request.form["user"]
    user.email=request.form["email"]
    user.sub_expire=datetime.strptime(request.form["sub_expire"],"%Y-%m-%d %H:%M:%S.%f")
    user.signup_date=datetime.strptime(request.form["signup_date"],"%Y-%m-%d %H:%M:%S.%f")
    user.refs=request.form["refs"]
    user.ref_code=request.form["ref_code"]
    user.signup_ref=request.form["signup_ref"]
    if request.form["admin"]=="True":
        user.admin=True
    else:
        user.admin=False
    db.session.commit()
    return redirect(url_for("admin"))


@app.get("/admin/deleteuser/<id>")
def deleteuser(id):
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    user=User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    
@app.post("/admin/updatemotd")
def updatemotd():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    
    motdcontent=request.form["motdcontent"]
    db.session.delete(MOTD.query.all()[-1])
    newmotd=MOTD(date=datetime.now(), content=motdcontent)
    db.session.add(newmotd)
    db.session.commit()
    
    
    
    
    
    return redirect(url_for("admin"))
    
    
    
    
@app.get("/admin/searchuser")
def searchuser():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    id=request.args.get("id")
    
    user=User.query.filter_by(id=id).first()
    if user is not None:
        response={
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "password":user.password,
            "last_seen":user.last_seen,
            "sub_expire":datetime.strftime(user.sub_expire,"%Y-%m-%d %H:%M:%S.%f"),
            "sub_type":user.sub_type,
            "signup_date":datetime.strftime(user.signup_date,"%Y-%m-%d %H:%M:%S.%f"),
            "signup_ref":user.signup_ref,
            "ref_code":user.ref_code,
            "refs":user.refs,
            "admin":user.admin
            
            
        }
        return make_response(jsonify(response),200)
    else:
        return make_response(jsonify({"error":"User not found"}),400)
    
    
    
    
@app.get("/admin/report")
def reportanalysis():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    
    
    
    try:
        match_id=request.args.get("match_id")
        if MatchAnalysis.query.filter_by(match_id=match_id).first() is None:
            flash("Analysis not found","error")
            return redirect(url_for("dashboard"))
        analysisreport=AnalysisReport.query.filter_by(match_id=match_id).first()
        if analysisreport is not None:
            analysisreport.number_of_reports=analysisreport.number_of_reports+1
            db.session.commit()
        else:
            newreport=AnalysisReport(match_id=match_id)
            db.session.add(newreport)
            db.session.commit()
            
        flash("Match analysis reported","success")
        return redirect(url_for("analysis",match_id=match_id))
    except Exception as e:
        flash("We ran into an error, please try again later","error")
        return redirect(url_for("analysis",match_id=match_id))        
    
    
@app.get("/admin/deletereport")
def deletereport():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    
    
    
    try:
        match_id=request.args.get("match_id")
        report=AnalysisReport.query.filter_by(match_id=match_id).first()
        if report is not None:
            db.session.delete(report)
            db.session.commit()
        return redirect(url_for("admin"))
    except Exception as e:
        return redirect(url_for("admin"))
    
    
    
@app.post("/admin/updateAnalysis")
def updateanalysis():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    
    mid=json.loads(request.json)["match_id"]
    
    content=json.loads(request.json)["content"]
    analysis=MatchAnalysis.query.filter_by(match_id=int(mid)).first()
  
    analysis.match_analysis_content=content
    db.session.commit()
    return make_response({"success":"updated record"},200)


@app.get("/admin/getanalysis")
def getanalysis():
    if "user_id" not in session:
        return redirect(url_for("dashboard"))
    if not User.query.filter_by(id=session["user_id"]).first().admin:
        return redirect(url_for("dashboard"))
    return MatchAnalysis.query.filter_by(match_id=request.args.get("id")).first().match_analysis_content