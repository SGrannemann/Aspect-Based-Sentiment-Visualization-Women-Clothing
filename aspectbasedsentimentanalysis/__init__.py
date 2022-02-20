from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.reader.farm import FARMReader
from haystack.pipeline import ExtractiveQAPipeline
from flask_restful import Resource, Api




app = Flask(__name__)
# TODO: Change to environment variable before launching
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

"""Database setup"""

basedir = os.path.abspath(os.path.dirname(__file__))
# TODO: Change to environment variable before launching
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'reviews.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
Migrate(app, db)

api = Api(app)

"""HuggingFace/Haystack setup"""
MODEL = 'mrm8488/bert-tiny-5-finetuned-squadv2'

# DocStore Setup
document_store = InMemoryDocumentStore()
from aspectbasedsentimentanalysis.models import Reviews
reviews = Reviews.query.all()
review_texts  = [{'text': entry.Review_Text} for entry in reviews if entry.Review_Text]
document_store.write_documents(review_texts)

# Pipe Setup

retriever = TfidfRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path=MODEL, progress_bar=False, return_no_answer=False)
pipe = ExtractiveQAPipeline(reader, retriever)



from aspectbasedsentimentanalysis.views import bp
app.register_blueprint(bp)




"""REST API for the user queries"""
from aspectbasedsentimentanalysis.models import UserQuery
class UserQueries(Resource):
    def get(self):
        queries = UserQuery.query.all()
        return [query.json() for query in queries]


api.add_resource(UserQueries, '/queries')