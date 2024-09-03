from flask import redirect,url_for,flash,session
from app import app
from app.db.models import db, MatchAnalysis,ProfileBet


@app.get("/favourite/<match_id>")
def favourite(match_id):
    if "user_id" not in session:
        flash("Authorization required",'error')
        return redirect(url_for("login"))
    if MatchAnalysis.query.filter_by(match_id=match_id).first() is None:
        flash("Could not find match","error")
        return redirect(url_for("analysis"),match_id=match_id)
    
    if "user_id" not in session:
        flash("Authorization required",'error')
        return redirect(url_for("login"))
    
    if ProfileBet.query.filter_by(match_id=match_id,user_id=session["user_id"]).first() is None:
        newprofilebet=ProfileBet(match_id=match_id,user_id=session["user_id"])
        db.session.add(newprofilebet)
        db.session.commit()
    else:
        db.session.delete(ProfileBet.query.filter_by(match_id=match_id,user_id=session["user_id"]).first())
        db.session.commit()
    
    flash("Success","success")
    return redirect(url_for("analysis",match_id=match_id))