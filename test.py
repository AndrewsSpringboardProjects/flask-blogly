
from unittest import TestCase
from app import app
#from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

class BloglyTests(TestCase):
	""" """

	def setUp(self):

		User.query.delete()

	def tearDown(self):

		db.session.rollback()

	def test_index(self):
		newUser = User(first_name = "yams", last_name = "b", image_url = None)
		db.session.add(newUser)
		db.session.commit()

		with app.test_client() as client:
			resp = client.get("/users")
			html = resp.get_data(as_text=True)
			
			self.assertEqual(resp.status_code, 200)
			self.assertIn("yams", html)

	def test_user(self):
		newUser = User(first_name = "yams", last_name = "b", image_url = None)
		db.session.add(newUser)
		db.session.commit()

		with app.test_client() as client:
			resp = client.get(f"/users/{newUser.id}")
			html = resp.get_data(as_text=True)
			
			self.assertEqual(resp.status_code, 200)
			self.assertIn("<h1>yams", html)

	def test_add(self):
		with app.test_client() as client:
			d = {"first_name": "yams", "last_name": "b", "user_img": ""}
			resp = client.post("/users/new",  data=d, follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("yams", html)


	def test_edit(self):
		newUser = User(first_name = "yams", last_name = "b", image_url = None)
		db.session.add(newUser)
		db.session.commit()

		with app.test_client() as client:
			d = {"first_name": "jams", "last_name": "b", "user_img": ""}
			resp = client.post(f"/users/{newUser.id}/edit",  data=d, follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("jams", html)