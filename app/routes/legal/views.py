from flask import render_template
from app import app


@app.route("/legal")
def legal():
    return render_template("legal.html")