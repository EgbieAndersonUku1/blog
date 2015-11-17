from google.appengine.ext import db
from json_maker import Json


class PostsDb(db.Model):
	"""This class stores all the users posts"""
	
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	last_created = db.DateTimeProperty(auto_now_add=True)

	@classmethod
	def add(cls, subject, content):
		"""Add the subject and content to the database"""

		content = content.replace("\n", "<br>") #replace newlines with page breaks
		post = cls(subject=subject, content=content)
		post.put()
		return post.key().id()

	@classmethod
	def find_path(cls, uid):
		"""Finds the path for a given uid"""
		key  = db.Key.from_path('PostsDb', int(uid))
		return db.get(key)
	
	@classmethod
	def get_all(cls):
		"""Return all the posts in order of lastest first"""
		return cls.all().order("-created")

class Users(db.Model):
	"""User class database stores the username,
	password hash and email to the database
	"""

	user_name   = db.StringProperty(required=True)
	passwd_hash = db.StringProperty(required=True)
	email       = db.StringProperty()

	@classmethod
	def by_name(cls, name):
		"""returns a user by name"""
		return cls.all().filter('user_name =', name).get()

	@classmethod
	def get_id(cls, user):
		"""return the user's id number"""
		return cls.get_by_id(user)

	@classmethod
	def add(cls, name, password, email=None):
		"""add(str, str) -> return(str)
		Adds a user along with their password
		to the database
		"""
		val = cls(user_name=name, passwd_hash=password, email=email)
		val.put()
		return val

	
		