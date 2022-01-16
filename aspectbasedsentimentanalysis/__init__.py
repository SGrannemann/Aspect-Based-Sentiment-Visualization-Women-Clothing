from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from haystack.document_store.sql import SQLDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.reader.farm import FARMReader
from haystack.pipeline import ExtractiveQAPipeline


app = Flask(__name__)
# TODO: Change to environment variable before launching
app.config['SECRET_KEY'] = 'mysecretkey'

"""Database setup"""

basedir = os.path.abspath(os.path.dirname(__file__))
# TODO: Change to environment variable before launching
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, 'reviews.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

"""HuggingFace/Haystack setup"""

# TODO: Setup model from HuggingFace
#MODEL = 'mrm8488/bert-small-finetuned-squadv2'
# TODO: Setup document store from Haystack
#document_store = SQLDocumentStore()
# get documents via db.query.all

# write to document store
# TODO: Setup pipeline from Haystack
#retriever = TfidfRetriever(document_store=document_store)
#reader = FARMReader(model_name_or_path=MODEL, progress_bar=False, return_no_answer=False)
#pipe = ExtractiveQAPipeline(reader, retriever)

""" Views for the app"""

# TODO: About


# TODO: Question View


# TODO: Display results


# TODO: Home 
@app.route('/')
def index():
    return "this is working"


"""REST API for the haystack pipeline"""
# TODO: build REST API endpoint with GET for inference results