from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer
from .entity import Entity, Base


# reply table, including all columns
class Reply(Entity, Base):

    __tablename__ = "replies"

    user_name = Column(String)
    post_id = Column(Integer)
    reply_text = Column(String)
    reply_date = Column(String)
    reply_time = Column(String)
    post_category = Column(String)
    post_reports = Column(String)

    def __init__(self, user_name, post_id, post_category,
                 reply_text, reply_date, reply_time):
        Entity.__init__(self)
        self.user_name = user_name
        self.post_id = post_id
        self.reply_text = reply_text
        self.reply_date = reply_date
        self.reply_time = reply_time
        self.post_category = post_category
        self.reports = 0


# reply schema to make the data easier to work with
class ReplySchema(Schema):

    id = fields.Integer()
    user_name = fields.Str()
    post_id = fields.Integer()
    reply_text = fields.Str()
    reply_date = fields.Str()
    reply_time = fields.Str()
    post_category = fields.Str()
    reports = fields.Str()

