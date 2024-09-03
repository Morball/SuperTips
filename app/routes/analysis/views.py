from app import app
import json 
from flask import render_template
import requests
from datetime import datetime
from app.util.matchdata import getLiveNow
from app.util.analysis.match_analysis import get_openai_analysis,get_team_link
from app.db.models import MatchAnalysis,db,ProfileBet
from app.util.authutil.login import login_required
from flask import flash
from datetime import timedelta
from app.util.apiscrape import load_get_response
from flask import redirect,url_for,session

@app.route("/analysis/<match_id>")
def analysis(match_id):

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    
    today=datetime.now()-timedelta(days=1)
    analysis_today=len(MatchAnalysis.query.filter(MatchAnalysis.date_created>=today,MatchAnalysis.created_by==session["user_id"]).all())
    if analysis_today>=2:
        flash("Maximum number of daily new analyses reached.","error")
        return redirect(url_for("dashboard"))
    
    
    
    
    try:
        match=MatchAnalysis.query.filter_by(match_id=match_id).first()
        if match is not None:
            
            if ProfileBet.query.filter_by(match_id=match_id,user_id=session["user_id"]).first() is None:
                return render_template("analysis.html",ctx=json.loads(match.match_analysis_content))
            else:
                return render_template("analysis.html",ctx=json.loads(match.match_analysis_content),has_fav=True)   
            
        
        event=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-US&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={match_id}")
        event["startDate"]=datetime.strptime(event["startDate"],"%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y, %H:%M")

        for competitor in event["competitors"]:
            teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
            if len(teamsearchresults)!=0:
                if len(teamsearchresults[0]["images"])!=0:
                    for res in teamsearchresults:
                        if res["participantTypes"]:
                            for partype in res["participantTypes"]:
                                if partype["name"]=="Player" and event["sport"]["id"] not in [77,68,72,71,84,81]:
                                    if len(res["images"]) !=0:
                                        competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[1]["images"][0]["path"]
                                else:
                                    if len(res["images"]) !=0:
                                        competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]
                                        
        if "sport" in event:                                  
            for ev in json.loads(getLiveNow(sportid=event["sport"]["id"], leagueid=event["champ"]["id"])):
                if ev["id"]==event["id"]:
                    event["isLive"]=True
                        
    
                        
        match_analysis=MatchAnalysis.query.filter_by(match_id=match_id).first()
        if match_analysis is not None: 
            
            event["openai_analysis"]=json.loads(match_analysis.match_analysis_content)
            return render_template("analysis.html",ctx=event)

        
        
        else:
            
                            
            bets=event["odds"]
            print(f"getting team lins for {event["odds"][0]["name"]} and  {event["odds"][2]["name"]}")
            teamlinks=(get_team_link(event["odds"][0]["name"],event["sport"]["name"]),get_team_link(event["odds"][2]["name"],event["sport"]["name"]))
            print(teamlinks)
            
            sport=event["sport"]["name"]
            team1=f"NO TEAM LINK PROVIDED, PLEASE FETCH HISTORIC DATA FROM FLASHSCORE.COM FOR {event["competitors"][0]["name"]} AND FILL team1"
            team2=f"NO TEAM LINK PROVIDED, PLEASE FETCH HISTORIC DATA FROM FLASHSCORE.COM FOR {event["competitors"][1]["name"]} AND FILL team2"
    
            if teamlinks[0] != '' and teamlinks[0] is not None :
                team1=requests.get(teamlinks[0]).text
            
            if teamlinks[1] != '' and teamlinks[1] is not None:
                team2=requests.get(teamlinks[1]).text
            
        
        
            if len(bets)<300:
                    
                openai_analysis=get_openai_analysis(team1,team2,sport, bets)
            else:
                openai_analysis=get_openai_analysis(team1,team2,sport, bets[0:300])

            print(openai_analysis)
            event["openai_analysis"]=json.loads(openai_analysis)
            
            
            match_analysis=MatchAnalysis(match_id=match_id,match_analysis_content=json.dumps(event), created_by=session["user_id"])
            db.session.add(match_analysis)
            db.session.commit()
        
            return render_template("analysis.html",ctx=event)
    except Exception as e:
      
        flash("Could not create match analysis, please try again later","error")
        print("FOUND EXCEPTION IN ANALYSIS",e)
        return redirect(url_for("dashboard"))
