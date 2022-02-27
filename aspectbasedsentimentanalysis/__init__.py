"""Central module for the Flask app.
Takes care of registering blueprints etc. as well as of setting up the Haystack pipeline & HuggingFace model.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.reader.farm import FARMReader
from haystack.pipeline import ExtractiveQAPipeline
from flask_restful import Resource, Api




app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# reflect because the database exists already and its metadata shall be used in the ORM mapping.
db.Model.metadata.reflect(db.engine)
Migrate(app, db)

# Enable Flask-Restful for REST API implementation
api = Api(app)


# Setup HuggingFace/Haystack model and pipeline

# Use the tiny model to save on space
MODEL = 'mrm8488/bert-tiny-5-finetuned-squadv2'

# DocStore Setup
document_store = InMemoryDocumentStore()

# import here because we first need to create db which is imported by the models module.
from aspectbasedsentimentanalysis.models import Reviews
# get all reviews and write them to the DocumentStore
reviews = Reviews.query.all()
review_texts  = [{'text': entry.Review_Text} for entry in reviews if entry.Review_Text]
document_store.write_documents(review_texts)

# Pipe Setup
retriever = TfidfRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path=MODEL, progress_bar=False, return_no_answer=False)
pipe = ExtractiveQAPipeline(reader, retriever)



from aspectbasedsentimentanalysis.views import bp
app.register_blueprint(bp)




# Setup the REST API so we can get userqueries easily
from aspectbasedsentimentanalysis.models import UserQuery
class UserQueries(Resource):
    def get(self):
        queries = UserQuery.query.all()
        return [query.json() for query in queries]

api.add_resource(UserQueries, '/queries')