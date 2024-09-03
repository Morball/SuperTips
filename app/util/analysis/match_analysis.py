
import requests
from app import openai_client
import concurrent.futures
import json
import requests
from bs4 import BeautifulSoup
from app.util.apiscrape import load_get_response
individual_sports = [
    "Archery",
    "Badminton",
    "Bowling",
    "Boxing",
    "Canoeing",
    "Cross-country skiing",
    "Cycling",
    "Darts",
    "Decathlon",
    "Diving",
    "Equestrian",
    "Fencing",
    "Figure skating",
    "Fishing",
    "Golf",
    "Gymnastics",
    "Heptathlon",
    "Judo",
    "Karate",
    "Luge",
    "Mixed martial arts",
    "Mountain biking",
    "Powerlifting",
    "Rowing",
    "Sailing",
    "Shooting",
    "Skateboarding",
    "Skiing",
    "Snowboarding",
    "Speed skating",
    "Surfing",
    "Swimming",
    "Table tennis",
    "Taekwondo",
    "Tennis",
    "Track and field",
    "Triathlon",
    "Weightlifting",
    "Wrestling"
]

team_link_headers={
    
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Accept-Language": "en-US,en;q=0.9",
"Connection": "keep-alive",
"Content-Length": "10",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Host": "stats4cash.com",
"Origin": "https://globalsportsarchive.com",
"Referer": "https://globalsportsarchive.com/",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "cross-site",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows"
    
}

def get_team_link(team_name,sport):
    resp=json.loads(requests.post("http://stats4cash.com/elastic/rest_autosearch.php?v=5",data={"term":team_name},headers=team_link_headers).text)
    print(resp)
    if resp is not None:
        for entity in resp:
            if team_name in entity['0'] and sport in entity['4']:
                print("https://globalsportsarchive.com"+str(entity['7']))
                return "https://globalsportsarchive.com"+str(entity['7'])
    else:
        return ''
        
    



def get_match_bets(mid):
    eventdetails=load_get_response(f"https://sb2frontend-altenar2.biahosted.com/api/widget/GetEventDetails?culture=en-US&timezoneOffset=-120&integration=mrbitro&deviceType=1&numFormat=en-GB&eventId={mid}")
    odds=eventdetails["odds"]
    return odds

def parse_team_history(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # List to store contents of divs
    div_contents = []

    # List of div ids to search for
    div_ids = ['team_season_matches','tn-widget','roster_container']

    # Loop through each id and find corresponding div element
    for div_id in div_ids:
        div_element = soup.find('div', id=div_id)
        if div_element:
            div_contents.append(str(div_element.get_text()))

    # Concatenate the contents of divs
    concatenated_content = '\n'.join(str(div_contents))
    return concatenated_content




def get_openai_analysis(team1,team2,sport, bets):
    team1_parsed=parse_team_history(team1)
    team2_parsed=parse_team_history(team2)
    
    if len(team1_parsed)<100:
        team1_parsed=f"NO TEAM LINK PROVIDED, PLEASE FETCH HISTORIC DATA FROM FLASHSCORE.COM FOR {team1} AND FILL team1"
    if len(team2_parsed)<100:
        team2_parsed=f"NO TEAM LINK PROVIDED, PLEASE FETCH HISTORIC DATA FROM FLASHSCORE.COM FOR {team2} AND FILL team2"
    
    completion_content=f'''Hello, I will give you two team/athlete names and their corresponding recent history, as a html page, i want you to interpret this historic data, you will be provided a list of possible bets for said teams/athletes, please analyse the recent histories and bets list,
    creating a json structure like so, where the variables marked by <> will be completed by you, please provide the 5 best bets you can come up with, taking into account tournament rankings,
    roster, history and news section, tropies and head to head stats, making similarities between the teams/athletes, also please provide a bet risk ranking from 1 to 5 for each bet, 
    also please make up a ~400 character event description, justifying your bet choices based on the data provided and your analysis 
    in bets list, X means draw.
    your data will be provided at the end of the prompt, only return json, nothing else

    please make sure bets do not repeat themselves, and also combine multiple bets into a parlay, also keeping them different, the formula for parlay price is NUMBER_OF_BETS_IN_PARLAY*MEAN_PRICE_OF_BETS, THE PARLAY PRICE CANNOT BE SMALLER THAN NUMBER_OF_BETS, PLEASE MAKE SURE YOU GET THE PARLAY PRICE RIGHT, PLEASE CALCULATE IT YOURSELFM AND DON'T PROVIDE IT AS A PRODUCT OF TWO TERMS, GIVE ME ONLY THE FINAL PRICE ACCORDING TO THE FORMULA SPECIFIED, and round the prices to two decimal points
    the parlay can look something like man city man city first goal over 2.5 goals, it is essential that you include at least one parlay into the best_bets category
    always include 5 recent matches, if 5 matches are not found, please make the json object data with the same keys, but blank values
    
    try to complete team names, for example man utd would be manchester city, man city would be manchester city, etc.
    
    make sure you take into account most well known sports betting strategies and make as much of a compenduous analysis as possible, this product needs to be worth its price
    
    also take into account roster performances for individual players and provide tips regarding those as well
    
    you will also be provided the sport name
    
    team1:{{
        recent_matches[
            {{
            team1_score:<SCORE>
            team2_score:<SCORE>
            form:<FORM>
            date_played:<DATE>
                
            }},
            {{
            team1_score:<SCORE>
            team2_score:<SCORE>
            form:<FORM>
            date_played:<DATE>
                
            }},
            {{
            team1_score:<SCORE>
            team2_score:<SCORE>
            form:<FORM>
            date_played:<DATE>
                
            }}
            
            .......
        ]
    
    }}
    team2:{{
        recent_matches[
            {{
            team1_score:<SCORE>
            team2_score:<SCORE>
            form:<FORM>
            date_played:<DATE>
                
            }},
            {{
            team1_score:<SCORE>
            team2_score:<SCORE>
            form:<FORM>
            date_played:<DATE>
                
            }},
            {{
            team1_score:<SCORE>
            team2_score:<SCORE>
            form:<FORM>
            date_played:<DATE>
                
            }}
            
            .......
        ]
    
    }},
    
    
    best_bets:{{
        bet_name:<BET_NAME>
        bet_price:<BET_PRICE>
        bet_ranking:<BET_RANKING>
        
        
    }},
    
    event_description:{{
        content:<EVENT_DESCRIPTION_CONTENT>
    }}
    
    
    
    
    sometimes you will be prompted messages telling you that no team link has been provided, please try to fetch a history of matches from flashscore.ro for said team and complete the recent matches fields
    
    please do not add any comments in the form of //<comment> to the json structure, only the data
    IF YOU DO NOT HAVE MATCHES FOR TEAM, JUST LEAVE IT AS IS WITH EMPTY DATA, DON'T GIVE ME AN EMPTY SET
    
    
    
    DO NOT REPLACE team1 AND team1 WITH ANYTHING, THEY ARE MEANT TO STAY team1 AND team2
    ---------------------------------
    
    COMPETITOR 1: {team1_parsed}
    
    COMPETITOR 2: {team2_parsed} 
    
    SPORT NAME  : {sport}
    
    BETS {bets}
    
    '''
    stream = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": completion_content}],
        )
    
    print(stream.choices[0].message.content.strip()[7:-3])

    return stream.choices[0].message.content.strip()[7:-3]