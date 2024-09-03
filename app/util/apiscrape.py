import cloudscraper
import json



def load_get_response(url):
    scraper = cloudscraper.create_scraper()
    return json.loads(scraper.get(url).text)

def load_post_response(url, params,headers):
    scraper=cloudscraper.create_scraper()
    print(scraper.post(url, params=params).text)
    return json.loads(scraper.post(url, params=params,headers=headers).text)