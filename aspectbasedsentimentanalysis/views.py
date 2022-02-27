"""Views for the app.
Views included:
- The homepage
- The About page
- The Ask Question page
- The Result Page
"""
import base64
import io
from collections import Counter
from flask import Blueprint, redirect, render_template, url_for
from wordcloud import WordCloud
from aspectbasedsentimentanalysis import db, pipe
from aspectbasedsentimentanalysis.models import UserQuery
from aspectbasedsentimentanalysis.forms import QuestionForm

# Create a single blueprint that we can register with the app in __init__
bp = Blueprint('bp', __name__)


@bp.route('/')
def index():
    """
    View for that starting page. Simply returns the respective html template.
    """
    return render_template("home.html")



@bp.route('/about')
def about():
    """
    View for the About page. Returns the respective HTML template.
    """
    return render_template('about.html')


@bp.route('/question', methods=['GET', 'POST'])
def question():
    """
    View for the page where the user can ask a question as Input for the QA pipeline.
    Redirects to the results page if the presented form was submitted. Also writes user questions to the database.
    """
    
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
    """
    View for the result presentation. Target of a redirect from the Ask Question page.
    Uses HayStack to get answers to the question, then generates a wordcloud that is then returned to the user as part of the template.
    """
    # use pipeline from __init__ go get answers
    answers = pipe.run(query=question, params={'Retriever': {'top_k': 100}, 'Reader': {'top_k': 20}})
    # collect only the answer text (and not start index etc.)
    results = []
    for answer in answers['answers']:
        results.append(answer['answer'])
    
    # Make a WordCloud
    counter = Counter(results)
    cloud = WordCloud()
    cloud.generate_from_frequencies(counter)
    
    # Convert the image so it can be rendered by browsers
    image = cloud.to_image()
    file_obj = io.BytesIO()
    image.save(file_obj, 'PNG')
    encoded_image = base64.b64encode(file_obj.getvalue())

    return render_template("result.html", question=question, cloud=encoded_image.decode('utf-8'))



