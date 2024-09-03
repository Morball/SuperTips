from flask import Flask
from openai import OpenAI
import datetime
openai_client=OpenAI(
      organization='org-5EO5OxiG8eThUSaTNI9jiHGZ',
      project="proj_4andCRGA26fkGE9mPggGUj9i",
      api_key="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"
)

from flask_migrate import Migrate



request_proxies={
"http":"13.81.217.201:80",
"http":"1.0.170.50:80",
"http":"102.68.128.212:8080",
"http":"13.250.96.183:8080"
 
    
    
    
}




request_headers={
         "User-Agent":"PostmanRuntime/7.41.0",
         "Accept":"*/*",
         "authority":"b2frontend-altenar2.biahosted.com"
                
         }
app=Flask(__name__)
app.config.from_pyfile("config.py")


from app.db.models import db




migrate=Migrate(app,db)









with app.app_context():
    db.create_all()








@app.after_request
def add_security_headers(resp):
    resp.headers["Access-Control-Allow-Origin"]="*"
    resp.headers["Access-Control-Allow-Headers"]="*"
    resp.headers["Access-Control-Allow-Methods"]="*"
    return resp

@app.template_filter('strftime')
def strftime_filter(value, format='%Y-%m-%d'):
    if isinstance(value, datetime.datetime):
        return value.strftime(format)
    return value


from app.routes.home import views
from app.routes.contact import views
from app.routes.profile import views
from app.routes.auth import views
from app.routes.dashboard import views
from app.routes.api import views
from app.routes.analysis import views
from app.routes.favourite import views
from app.routes.payments import views
from app.routes.legal import views
from app.routes.admin import views