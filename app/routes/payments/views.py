import json
import os
import stripe
from app import app
from app.db.models import User
from app import db
from datetime import datetime
from flask import Flask, jsonify, request,render_template,redirect,url_for,session,redirect,flash
from datetime import timedelta
from app.db.models import Subs_Bought
# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "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"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_VjAYjtxNoDfEEYswCsuQ19KuiY8oqqjA'


@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
                
        user=User.query.filter_by(id=payment_intent["metadata"]["user_id"]).first()
        print(payment_intent["metadata"])
        subdays=0
        
        subtype=payment_intent["metadata"]["sub_type"]
        
        if str(subtype)=='1':
            subdays=30
        elif str(subtype)=='2':
            subdays=90
        elif str(subtype)=='3':
            subdays=180
            
        if user is not None:
            user.sub_expire=datetime.now()+timedelta(days=subdays)
            if user.signup_ref:
                reffered_by=User.query.filter_by(ref_code=user.signup_ref).first()
                reffered_by.refs=reffered_by.refs+1
            
            newsub=Subs_Bought(date=datetime.now(),user_id=user.id,sub_type=subtype)
            db.session.add(newsub)
            db.session.commit()  
            
            print("updated user")
        
      
      
      
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


    


@app.route("/checkout/<int:product_id>")
def checkout(product_id):
    if "user_id" not in session:
        flash("Authorization required",'error')
        return redirect(url_for("login"))
    amount_pay=0
    if product_id==1:
        amount_pay=2499
    elif product_id==2:
        amount_pay=5999
    elif product_id==3:
        amount_pay=9999
    else:
        return redirect(url_for("home"))
    pi=stripe.PaymentIntent.create(
    amount=amount_pay,
    currency="usd",
    metadata={"user_id":session["user_id"],"sub_type":product_id}

    )
    
    
    product_context={}
    product_context["amount"]=amount_pay/100
    if product_id==1:
        product_context["name"]="Novice"
        product_context["months"]=1
    if product_id==2:
        product_context["name"]="Intermediate"
        product_context["months"]=3
    if product_id==3:
        product_context["name"]="Advanced"
        product_context["months"]=6
    
    
    return render_template("checkout.html",client_secret=pi["client_secret"],ctx=product_context)