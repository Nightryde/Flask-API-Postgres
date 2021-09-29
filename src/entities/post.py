from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


# post table, including all columns
class Post(Entity, Base):

    __tablename__ = "posts"

    user_name = Column(String)
    post_category = Column(String)
    post_title = Column(String)
    post_text = Column(String)
    post_image = Column(String)
    post_date = Column(String)
    post_time = Column(String)
    post_clicks = Column(Integer)
    post_reports = Column(Integer)

    def __init__(self, user_name, post_category, post_title, post_text, 
                 post_image, post_date, post_time): 
        Entity.__init__(self)
        self.user_name = user_name
        self.post_category = post_category
        self.post_title = post_title
        self.post_text = post_text
        self.post_image = post_image
        self.post_date = post_date
        self.post_time = post_time
        self.post_clicks = 0
        self.post_reports = 0


# post schema to make the data easier to work with
class PostSchema(Schema):
    
    id = fields.Number()
    user_name = fields.Str()
    post_category = fields.Str()
    post_title = fields.Str()
    post_text = fields.Str()
    post_image = fields.Str()
    post_date = fields.Str()
    post_time = fields.Str()
    post_clicks = fields.Int()
    post_reports = fields.Int()
