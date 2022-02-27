"""
Module for the forms that are rendered.
Included forms:
- QuestionForm, form where the user can ask a question we will find answers to.

"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



class QuestionForm(FlaskForm):
    """
    Form used on the question page.
    """
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Find Answers!')