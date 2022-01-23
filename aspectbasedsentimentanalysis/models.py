# TODO: Setup model for Reviews
from aspectbasedsentimentanalysis import db

class Reviews(db.Model):
    __table__ = db.Model.metadata.tables['reviews']
    #index = db.Column(db.Integer, primary_key=True)
    #Review_Text = db.Column(db.Text)

    def __init__(self, review_text):
        self.Review_Text = review_text
class UserQuery(db.Model):
    __table__ = db.Model.metadata.tables['user_query']

    def __init__(self, userquery):
        self.userquery = userquery




# TODO: Setup model for user questions (log usage data)

