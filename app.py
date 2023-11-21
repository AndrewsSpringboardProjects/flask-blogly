"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

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

db.drop_all()
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
    ####################################################

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