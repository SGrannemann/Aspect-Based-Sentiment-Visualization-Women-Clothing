""" Views for the app"""
from flask import Blueprint, redirect, render_template, url_for
from aspectbasedsentimentanalysis import db
from aspectbasedsentimentanalysis.models import Reviews, UserQuery
from aspectbasedsentimentanalysis.forms import QuestionForm

bp = Blueprint('bp', __name__)

# TODO: About
@bp.route('/about')
def about():
    return 'this will be the about page'

# TODO: Question View
@bp.route('/question')
def question():
    # TODO: add to query database
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.question
        return redirect(url_for('bp.result', question=question))
    

    return render_template('question.html', form=form)

# TODO: Display results
@bp.route('/result/<question>')
def result(question):
    # TODO: get result via haystack
    return f'{question}'

# TODO: Home 
@bp.route('/')
def index():
    return "this is working"




# @bp.route('/list')
# def list_all():
#     u = UserQuery.query.all()
#     output = [entry.userquery for entry in u]
#     return f'{output}'

# @bp.route('/add')
# def add():
#     new_userquery = UserQuery('some text')
#     db.session.add(new_userquery)
#     db.session.commit()
#     return 'added user'   

# @bp.route('/list_reviews')
# def list_all_reviews():
#     u = Reviews.query.all()
#     output = [entry.Review_Text for entry in u]
#     return f'{output}'
