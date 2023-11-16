"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret123'

#debug = DebugToolbarExtension(app)

connect_db(app)

ctx = app.app_context()

ctx.push()

db.create_all()
