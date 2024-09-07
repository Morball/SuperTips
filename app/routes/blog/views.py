from app import app
from app.db.models import BlogPost
from flask import render_template, redirect, url_for
from datetime import datetime
from sqlalchemy import desc


@app.route("/blog")
def blog():
    allposts = BlogPost.query.order_by(desc(BlogPost.date_created)).all()
    posts=[]
    for post in allposts:
        posts.append({
            "id":post.id,
            "title":post.title,
            "subtitle":post.subtitle,
            "date_created":post.date_created.strftime('%B %d, %Y')
            })
    
    return render_template("blog/index.html", posts=posts)



@app.route("/blog/post/<postid>")
def blogpost(postid):
    postquery=BlogPost.query.filter_by(id=postid).first_or_404()
    post={
        "title":postquery.title,
        "subtitle":postquery.subtitle,
        "date_created":postquery.date_created.strftime('%B %d, %Y'),
        "content":postquery.content
    }
    return render_template("blog/post.html", post=post)