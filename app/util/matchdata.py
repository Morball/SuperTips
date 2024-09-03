import requests
import json
import random
from datetime import datetime
from app.util.analysis.match_analysis import get_team_link
from app.util.apiscrape import load_get_response
from app import request_headers,request_proxies
from app.db.models import MatchAnalysis
#get all live matches from sport id ["events"]

#https://sb2frontend-altenar2.biahosted.com/api/widget/GetLivenow?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&eventCount=2000&sportId=66




#https://sb2frontend-altenar2.biahosted.com/api/widget/GetLiveOverview?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=66

#same as above, not sure 





#get details on event, from liveoverview route https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&eventId=9439065

#Also contains odds and everything needed for bet calculation, merge data from getlivenow and geteventdetails to get bets overview on live events




#end of live match section  


#https://sb2widgetsstatic-altenar2.biahosted.com/assets/sprites/sport-icons-pack-1.4/stack/sprite.svg#tennis   ICONS

#https://sb2frontend-altenar2.biahosted.com/api/widget/GetEvents?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&eventCount=0&sportId=66&couponType=3
#https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=145&eventCount=20
#get upcoming events football, event format same as in getliveoverview and getliveevents
#both live and upcoming also include championships



#get all sports ids https://sb2frontend-altenar2.biahosted.com/api/widget/GetSportMenu?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&period=0

def get_sports_and_leagues():
    sports_leagues=[]
    leagues_array=[]

    allsports_competitions=load_get_response("https://sb2frontend-altenar2.biahosted.com/api/widget/GetSportMenu?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GBO&period=0")

    for sport in allsports_competitions["sports"]:

        for id in sport["catIds"]:


            for category in allsports_competitions["categories"]:
                
                

                
                if id==category["id"]:
                    for champid in category["champIds"]:
                        for champ in allsports_competitions["champs"]:
                            if champ["id"]==champid:
                                leagues_array.append(champ)
                    
                    
        sports_leagues.append({
            "sport":sport,
            "leagues":leagues_array       
                                        
                                        
            })
        leagues_array=[]

    return json.dumps(sports_leagues)



def getDashboardLive():
    liveevents=[]
    all_liveEvents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetLivenow?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventCount=0&sportId=66")

    for event in all_liveEvents["events"]:
        if event["champId"] in [2936,2941,3087,3111,8697,9835,32735,3140,4004,4927,3164,3793,4767,5282,2950]:
            eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
            if eventdetails is not None:

                event["odds"]=eventdetails["odds"]

                            
                            
                            
                for competitor in eventdetails["competitors"]:
                    teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
                    if len(teamsearchresults)!=0:
                        if len(teamsearchresults[0]["images"])!=0:
                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]
                            
                event["competitors"]=eventdetails["competitors"]
                event["isLive"]=True
                if MatchAnalysis.query.filter_by(match_id=event["id"]).first() is not None:
                    event["analysed"]=True
                liveevents.append(
                        event
                    )

    return liveevents

def getLiveNow(sportid=None, leagueid=None):
    liveevents=[]

    if sportid is not None and leagueid is not None:
        all_liveEvents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetLivenow?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventCount=10&sportId={sportid}")

        for event in all_liveEvents["events"]:
            if int(event["champId"]) ==int(leagueid):

                eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
                if eventdetails is None:
                    return ""
                event["odds"]=eventdetails["odds"]

                    
                    
                    
                for competitor in eventdetails["competitors"]:
                    teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
                    if len(teamsearchresults)!=0:
                        if len(teamsearchresults[0]["images"])!=0:
                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]
                    
                event["competitors"]=eventdetails["competitors"]
                event["isLive"]=True
                if MatchAnalysis.query.filter_by(match_id=event["id"]).first() is not None:
                    event["analysed"]=True
                liveevents.append(
                            event
                        )

        return json.dumps(liveevents)
    elif sportid is not None and leagueid is None:
        all_liveEvents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetLivenow?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventCount=0&sportId={sportid}")

        for event in all_liveEvents["events"]:
            if event["champId"] in [2936,2941,3087,3111,8697,9835,32735,3140,4004,4927,3164,3793,4767,5282,2950]:

                eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
                if eventdetails is None:
                    return ""
                event["odds"]=eventdetails["odds"]

                    
                    
                    
                for competitor in eventdetails["competitors"]:
                    teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
                    if len(teamsearchresults)!=0:
                        if len(teamsearchresults[0]["images"])!=0:
                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]
                    
                event["competitors"]=eventdetails["competitors"]
                event["isLive"]=True
                if MatchAnalysis.query.filter_by(match_id=event["id"]).first() is not None:
                    event["analysed"]=True
                liveevents.append(
                            event
                        )

        return json.dumps(liveevents)
    
    elif sportid is None and leagueid is None:
        all_liveEvents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetLivenow?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventCount=10&sportId=66")

        for event in all_liveEvents["events"]:
            eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
            if eventdetails is not None:

                event["odds"]=eventdetails["odds"]

                        
                        
                        
                for competitor in eventdetails["competitors"]:
                    teamsearchresults=requests.get(f"https://s.livesport.services/api/v2/search/",params={"q":competitor["name"]}).json()
                    if len(teamsearchresults)!=0:
                        if len(teamsearchresults[0]["images"])!=0:
                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]
                        
                event["competitors"]=eventdetails["competitors"]
                event["isLive"]=True
                if MatchAnalysis.query.filter_by(match_id=event["id"]).first() is not None:
                    event["analysed"]=True
                liveevents.append(
                                event
                    )

        return json.dumps(liveevents)
    
    

def getevents(sportid,leagueid):
    events=[]
    allevents=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId={sportid}&eventCount=0")
     
    #https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=145&eventCount=20
    for event in allevents["events"]:
        if str(event["champId"])==str(leagueid):
            eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
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
                                        if len(res["images"]) !=0:
                                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[1]["images"][0]["path"]
                                    else:
                                        if len(res["images"]) !=0:
                                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]                 
                

            event["competitors"]=eventdetails["competitors"]
            event["isLive"]=False
            if MatchAnalysis.query.filter_by(match_id=event["id"]).first() is not None:
                event["analysed"]=True
            events.append(event)
    print(events)
    return events        
            
            





def getmotd():
    events=[]
    print(load_get_response("https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=66&eventCount=0"))
    allevents=load_get_response("https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=66&eventCount=0")
     
    #https://sb2frontend-altenar2.biahosted.com/api/widget/GetUpcoming?culture=en-GB&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&countryCode=RO&sportId=145&eventCount=20
    for event in allevents["events"]:
        
        if str(event["champId"]) in ["3793","2813","17146","2942","3102","2941","2950","2954","9376","2943","3143","3145","3032","4600","2961","3024"]:
            eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-GB&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={event["id"]}")
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
                                        if len(res["images"]) !=0:
                                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[1]["images"][0]["path"]
                                    else:
                                        if len(res["images"]) !=0:
                                            competitor["img"]="https://static.flashscore.com/res/image/data/"+teamsearchresults[0]["images"][0]["path"]                 
                

            event["competitors"]=eventdetails["competitors"]
            event["isLive"]=False
            if MatchAnalysis.query.filter_by(match_id=event["id"]).first() is not None:
                event["analysed"]=True
            if get_team_link(event["odds"][0]["name"],eventdetails["sport"]["name"]) !='' and get_team_link(event["odds"][2]["name"],eventdetails["sport"]["name"])!='0':
                events.append(event)


    live=getDashboardLive()
    for match in live:
        match["isLive"]=True
        events.append(match)

    for match in events:
        odds = match['odds']
        odds_difference = abs(odds[0]["price"] - odds[2]["price"])
        match['odds_difference'] = odds_difference

    # Sort matches by odds difference (high to low)
    sorted_matches = sorted(events, key=lambda x: x['odds_difference'], reverse=True)

    return sorted_matches[0:7]
    
