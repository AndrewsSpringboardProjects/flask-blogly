
from unittest import TestCase
from app import app
#from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

class BloglyTests(TestCase):
	""" """

	def setUp(self):

		Post.query.delete()
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



	def test_post_new_page(self):
		newUser = User(first_name = "yams", last_name = "b", image_url = None)
		db.session.add(newUser)
		db.session.commit()

		with app.test_client() as client:
			resp = client.get(f"/users/{newUser.id}/posts/new")
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("yams b", html)

	def test_post_new(self):
		newUser = User(first_name = "yams", last_name = "b", image_url = None)
		db.session.add(newUser)
		db.session.commit()

		with app.test_client() as client:
			d = {"title": "grapple", "content": "apple"}
			resp = client.post(f"/users/{newUser.id}/posts/new",  data=d, follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("grapple", html)

	def test_post_edit(self):
		newUser = User(first_name = "yams", last_name = "b", image_url = None)
		db.session.add(newUser)
		db.session.commit()

		newPost = Post(title = "r", content = "apple", user_id = newUser.id)
		db.session.add(newPost)
		db.session.commit()

		with app.test_client() as client:
			d = {"title": "r", "content": "banana"}
			resp = client.post("/posts/1/edit",  data=d, follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("banana", html)		


