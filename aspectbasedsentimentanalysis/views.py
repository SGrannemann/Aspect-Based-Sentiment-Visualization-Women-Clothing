""" Views for the app"""
import base64
from flask import Blueprint, redirect, render_template, url_for
from aspectbasedsentimentanalysis import db, pipe
from aspectbasedsentimentanalysis.models import UserQuery
from aspectbasedsentimentanalysis.forms import QuestionForm
from collections import Counter
from wordcloud import WordCloud
import io

bp = Blueprint('bp', __name__)

# TODO: Home 
@bp.route('/')
def index():
    return render_template("home.html")


# TODO: About
@bp.route('/about')
def about():
    return render_template('about.html')

# TODO: Question View
@bp.route('/question', methods=['GET', 'POST'])
def question():
    
    form = QuestionForm()
    if form.validate_on_submit():
        user_question = form.question.data
        user_query = UserQuery(user_question)
        db.session.add(user_query)
        db.session.commit()
        
        return redirect(url_for('bp.result', question=user_question))
    

    return render_template('question.html', form=form)



@bp.route('/result/<question>')
def result(question):
    
    answers = pipe.run(query=question, params={'Retriever': {'top_k': 100}, 'Reader': {'top_k': 20}})
    results = []
    for answer in answers['answers']:
        results.append(answer['answer'])
    counter = Counter(results)
    cloud = WordCloud()
    cloud.generate_from_frequencies(counter)
    
    image = cloud.to_image()
    file_obj = io.BytesIO()
    image.save(file_obj, 'PNG')
    
    encoded_image = base64.b64encode(file_obj.getvalue())
    return render_template("result.html", question=question, cloud=encoded_image.decode('utf-8'))



