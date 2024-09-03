from app import app
from app.util.matchdata import get_sports_and_leagues,getLiveNow, getmotd,getDashboardLive,getevents
import json
import random
from app.db.models import MOTD,db,User,MatchAnalysis
from datetime import datetime
from app.util.authutil.login import login_required
from flask import session,redirect,url_for,flash,request,render_template

@app.get("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Authorization required",'error')
        return redirect(url_for("login"))
    
    if User.query.filter_by(id=session["user_id"]).first().sub_expire<datetime.now():
        flash("No subscriptions active","error")
        return redirect(url_for("profile"))
    print("hit dashboard route")
    
    if request.args.get("sport") or request.args.get("league"):
        if request.args.get("live"):
            sport=request.args.get("sport")
            league=request.args.get("league")
            if not request.args.get("q"):
                print(json.loads(getLiveNow(sportid=sport,leagueid=league)))
                return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()),motd_list=json.loads(getLiveNow(sportid=sport,leagueid=league)))
            else:
                motd_list=[]
                events=json.loads(getLiveNow(sportid=sport,leagueid=league))
                for event in events:
                    if request.args.get("q") in str(event["odds"]+event["competitors"]):
                        motd_list.append(event)
                for m in motd_list:
                    if MatchAnalysis.query.filter_by(id=m["id"]).first() is not None:
                        m["analysed"]=True
                return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()),motd_list=motd_list)
        else:
            if not request.args.get("q"):
                return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()),motd_list=getevents(request.args.get("sport"), request.args.get("league")))
            else:
                motd_list=[]
                events=getevents(request.args.get("sport"), request.args.get("league"))
                for event in events:
                    if request.args.get("q") in str(event["odds"]+event["competitors"]):
                        motd_list.append(event) 
                for m in motd_list:
                    if MatchAnalysis.query.filter_by(match_id=m["id"]).first() is not None:
                        m["analysed"]=True
                return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()),motd_list=motd_list)

        
        
        
    if len(MOTD.query.all()) ==0:
        
        motd=getmotd()
       # if len(motd)<8:
        #    motd=getmotd()
        motd_list=[]
        for match in motd:
            if not match["isLive"]:
                motd_list.append(match)
                
        for m in motd_list:
            if MatchAnalysis.query.filter_by(match_id=m["id"]).first() is not None:
                m["analysed"]=True
                print(m)
                
        newmotd=MOTD(content=json.dumps(motd),date=datetime.now())
        db.session.add(newmotd)
        db.session.commit()
        
        return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()), motd_list=motd_list)
    else:
        if (datetime.now()-MOTD.query.all()[-1].date).total_seconds()>24*3600:
            print("old motd recorded, getting new motd")
            motd=getmotd()
            motd_list=[]
            for match in motd:
                if not match["isLive"]:
                    motd_list.append(match)
            for m in motd_list:
                if MatchAnalysis.query.filter_by(match_id=m["id"]).first() is not None:
                    m["analysed"]=True
                    print(m)
            #if len(motd)<8:
             #   motd=getmotd()
            newmotd=MOTD(content=json.dumps(motd),date=datetime.now())
            db.session.add(newmotd)
            db.session.commit()
        
            return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()), motd_list=motd_list)
        else:
            print("getting latest motd")
            motd=json.loads(MOTD.query.all()[-1].content)
            motd_list=[]
            for match in motd:
                if not match["isLive"]:
                    motd_list.append(match)
            for m in motd_list:
                if MatchAnalysis.query.filter_by(match_id=m["id"]).first() is not None:
                    m["analysed"]=True
                    print(m)
            while motd is None:
                motd=MOTD.query.all()[-1]
            return render_template("dashboard.html",ctx=json.loads(get_sports_and_leagues()), motd_list=motd_list)
        

