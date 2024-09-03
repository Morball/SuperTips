from app import app
from flask import jsonify, make_response, request
import requests
from app.util.matchdata import getLiveNow
import random
import json
from app.util.apiscrape import load_get_response
from datetime import datetime

from flask import session





headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }






@app.post("/getUpcoming")
def getUpcoming():
    if "user_id" not in session:
        return make_response(jsonify({"error":"not authorised"}),400)
    events=[]
    upcoming_events=request.json
    if len(upcoming_events)==0:
        allevents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&timezoneOffset=0&integration=mrbitro&deviceType=1&numFormat=en-GB&sportId=66&eventCount=0")
        for event in allevents["events"]:

            eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
            event["odds"]=eventdetails["odds"]
            event["startDate"]=datetime.strptime(event["startDate"],"%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y, %H:%M")

            for competitor in eventdetails["competitors"]:
                teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
                if len(teamsearchresults)!=0:
                    
                    if len(teamsearchresults[0]["images"])!=0:
                        for res in teamsearchresults:
                                if res["participantTypes"]:
                                    for partype in res["participantTypes"]:
                                        if partype["name"]=="Player" and event["sportId"] not in [77,68,72,71,84,81]:
                                            if len(res) >1:
                                                
                                                competitor["img"]="https://static.flashscore.com/res/image/data/"+res[1]["images"][0]["path"]

                                        else:
                                            if len(res["images"]) !=0:
                  
                                                competitor["img"]="https://static.flashscore.com/res/image/data/"+res[0]["images"][0]["path"]
                                           
                
            event["competitors"]=eventdetails["competitors"]
            event["isLive"]=False
            live=json.loads(getLiveNow(sportid=66,leagueid=16808))
            for match in live:
                events.append(match)
            events.append(event)
        return make_response(jsonify(events),200)
    
    
    for upcoming in upcoming_events:
        sportid=int(upcoming["sportid"])
        compid=int(upcoming["leagueid"])
        #https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=145&eventCount=20
        allevents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&integration=mrbitro&deviceType=1&numFormat=en-GB&sportId={sportid}&eventCount=0")
        
        for event in allevents["events"]:
            if str(event["champId"])==str(compid):
                eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-180&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&eventId={event["id"]}")
                event["odds"]=eventdetails["odds"]
                event["startDate"]=datetime.strptime(event["startDate"],"%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y, %H:%M")
    
                for competitor in eventdetails["competitors"]:
                    teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
                    if len(teamsearchresults)!=0:
                        if len(teamsearchresults[0]["images"])!=0:
                            for res in teamsearchresults:
                                if res["participantTypes"]:
                                    for partype in res["participantTypes"]:
                                        if partype["name"]=="Jucător" and event["sportId"] not in [77,68,72,71,84,81]:
                                            if len(res["images"]) >1:
                                                competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[1]["images"][0]["path"]
                                        else:
                                            if len(res["images"]) !=0:
                                                competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]
                        
                event["competitors"]=eventdetails["competitors"]
                event["isLive"]=False
                events.append(event)
                
        live=json.loads(getLiveNow(sportid,compid))
        for match in live:
           match["isLive"]=True
           events.append(match)

    return make_response(jsonify(events),200)



@app.post("/betCalculator")
def betcalculator():
    body=request.json








@app.post("/getLiveNow")
def getLiveNowRoute():
    sportsdict=load_get_response("https://sb2frontend-altenar2.biahosted.com/api/widget/GetSportMenu?culture=en-US&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&period=0")["sports"]
    events=[]
    upcoming_events=request.json
    for upcoming in upcoming_events:
        sportid=upcoming["sportid"]
        compid=upcoming["leagueid"]
        if sportid is None:
            return make_response(
                jsonify(getLiveNow(sportid=66)),200
            )

        events.append(getLiveNow(sportid=sportid,leagueid=compid))
        
    
    

    return make_response(
            jsonify(events),200
        )