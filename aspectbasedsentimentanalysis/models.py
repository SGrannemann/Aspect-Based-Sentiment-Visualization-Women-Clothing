"""
Module that provides the classes for the ORM mapping.
Included classes"
- Reviews: Class for the product reviews that can be searched for answers/
- UserQuery: For logging the questions that were asked in a database.

"""
from aspectbasedsentimentanalysis import db

class Reviews(db.Model):
    """
    Class for ORM of the product reviews in the SQLite database.
    As it works with an already existing database, it uses the metadata present in the database.
    Only works in combination with the reflect call in __init__.
    """
    __table__ = db.Model.metadata.tables['reviews']
    

    def __init__(self, review_text):
        self.Review_Text = review_text

        
class UserQuery(db.Model):
    """
    Class for ORM of the asked questions in the SQLite database.
    As it works with an already existing database, it uses the metadata present in the database.
    Only works in combination with the reflect call in __init__.
    Provides json() that can be returned via the REST API defined in __init__.
    """
    __table__ = db.Model.metadata.tables['user_query']

    def __init__(self, userquery):
        self.user_query = userquery

    def json(self):
        """Returns a dictionary representation of a query object. Used for REST API in __init__."""
        return {'query': self.user_query}    






