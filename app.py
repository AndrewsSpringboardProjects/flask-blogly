"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = 'secret123'

toolbar = DebugToolbarExtension(app)

connect_db(app)

#ctx = app.app_context()
#ctx.push()

#db.drop_all()
db.create_all()

@app.route('/')
def base():
    """ """
    return redirect("/users")

@app.route('/users')
def showUsers():
    """ """
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users/new')
def showAdd():
    """ """
    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def addUser():
    """ """
    newUser = User(
    	first_name = request.form['first_name'],
    	last_name = request.form['last_name'],
    	image_url = request.form['user_img'] or None
    )

    db.session.add(newUser)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<userID>')
def showUser(userID):
    """ """
    user = User.query.get(userID)
    return render_template('user.html', user=user)

@app.route('/users/<userID>/edit')
def showEdit(userID):
    """ """
    user = User.query.get(userID)
    return render_template('edit.html', user=user)

@app.route('/users/<userID>/edit', methods=["POST"])
def updateUser(userID):
    """ """
    user = User.query.get(userID)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['user_img'] or None

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<userID>/delete', methods=["POST"])
def deleteUser(userID):
    """ """
    user = User.query.get(userID)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



@app.route('/users/<userID>/posts/new')
def showPosting(userID):
    """Show posting form"""
    user = User.query.get(userID)
    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<userID>/posts/new', methods=["POST"])
def addPost(userID):
    """Handle post adding"""
    user = User.query.get(userID)
    tagIDS = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tagIDS)).all()
    newPost = Post(
    	title = request.form['title'],
    	content = request.form['content'],
    	user_id = userID,
        tags=tags
    )

    db.session.add(newPost)
    db.session.commit()

    return redirect(f"/users/{userID}")

@app.route('/posts/<postID>')
def showPost(postID):
    """ """
    post = Post.query.get(postID)
    return render_template('post.html', post=post)

@app.route('/posts/<postID>/edit')
def showPostEdit(postID):
    """ """
    post = Post.query.get(postID)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<postID>/edit', methods=["POST"])
def updatePost(postID):
    """ """
    post = Post.query.get(postID)
    post.title = request.form['title']
    post.content = request.form['content']

    tagIDS = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tagIDS)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{postID}")

@app.route('/posts/<postID>/delete', methods=["POST"])
def deletePost(postID):
    """ """
    post = Post.query.get(postID)
    db.session.delete(post)
    db.session.commit()

    return redirect("/users")



@app.route('/tags')
def showAllTags():

    tags = Tag.query.all()
    return render_template('all_tags.html', tags=tags)

@app.route('/tags/<tagID>')
def showTag(tagID):

    tag = Tag.query.get(tagID)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/new')
def showAddTag():

    posts = Post.query.all()
    return render_template('new_tag.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def addTag():

    """
    user = User.query.get(userID)
    newPost = Post(
        title = request.form['title'],
        content = request.form['content'],
        user_id = userID
    )

    posts = Post.query.filter(Post.id.in_).all()
    """

    tag = Tag(
        name=request.form['name'],
    )

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tagID>/edit')
def showEditTag(tagID):

    tag = Tag.query.get(tagID)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<tagID>/edit', methods=["POST"])
def editTag(tagID):

    tag = Tag.query.get(tagID)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tagID>/delete', methods=["POST"])
def deleteTag(tagID):

    tag = Tag.query.get(tagID)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')