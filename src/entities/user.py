from marshmallow import Schema, fields
from sqlalchemy import Column, String
from .entity import Entity, Base


# user table, including all columns
class User(Entity, Base):

	__tablename__ = "users"
	
	username = Column(String)
	password = Column(String)

	def __init__(self, username, password):

		Entity.__init__(self)
		self.username = username
		self.password = password

# user schema to make the data easier to work with
class UserSchema(Schema):

	id = fields.Number()
	username = fields.Str()
	password = fields.Str()

