from flask import render_template

from blog import app
from .database import session
from .models import Post

import mistune
from flask import request, redirect, url_for

# @app.route("/")
# def posts():
#     posts = session.query(Post)
#     posts = posts.order_by(Post.datetime.desc())
#     posts = posts.all()
#     return render_template("posts.html",
#         posts=posts
#     )

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

# /post/<id>
# Allows you to view a single post
# Should be accessed by clicking on the title of a post
# Should use the render_post macro to display the post
@app.route("/post/<int:id>")
def post(id = None):
    post = session.query(Post)
    post = post.filter_by(id=id).first()
    return render_template("post.html", post=post)

# /post/<id>/edit
# Allows you to edit a post
# Should be accessed via a link in the metadata div
# Should display a similar form to the add_post view
# The form should be prepopulated with the existing post data
@app.route("/post/<int:id>/edit", methods=["GET"])
def edit_post(id = None):
    post = session.query(Post)
    post = post.filter_by(id=id).first()
    return render_template("edit_post.html", post=post)

@app.route("/post/<int:id>/edit", methods=["POST"])
def edit_post_post(id=None):
    post = session.query(Post)
    post = post.filter_by(id=id).first()
    post.title = request.form["title"]
    post.content = mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))

# /post/<id>/delete
# Allows you to delete a post
# Should be accessed via a link in the metadata div
# Should display buttons asking you to confirm or cancel the deletion
@app.route("/post/<int:id>/delete", methods=["GET"])
def delete_post(id=None):
    post = session.query(Post)
    post = post.filter_by(id=id).first()
    return render_template("delete_post.html", post=post)

@app.route("/post/<int:id>/delete", methods=["POST"])
def delete_post_post(id=None):
    post = session.query(Post)
    post = post.filter_by(id=id).first()
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))