""" Views for the app"""
from flask import Blueprint
from aspectbasedsentimentanalysis import db
from aspectbasedsentimentanalysis.models import Reviews, UserQuery

bp = Blueprint('bp', __name__)
# TODO: About


# TODO: Question View


# TODO: Display results


# TODO: Home 
@bp.route('/')
def index():
    return "this is working"

@bp.route('/list')
def list_all():
    u = UserQuery.query.all()
    output = [entry.userquery for entry in u]
    return f'{output}'

@bp.route('/add')
def add():
    new_userquery = UserQuery('some text')
    db.session.add(new_userquery)
    db.session.commit()
    return 'added user'   

@bp.route('/list_reviews')
def list_all_reviews():
    u = Reviews.query.all()
    output = [entry.Review_Text for entry in u]
    return f'{output}'
