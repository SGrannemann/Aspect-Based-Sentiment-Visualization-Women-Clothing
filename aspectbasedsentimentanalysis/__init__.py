from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.reader.farm import FARMReader
from haystack.pipeline import ExtractiveQAPipeline




app = Flask(__name__)
# TODO: Change to environment variable before launching
app.config['SECRET_KEY'] = 'mysecretkey'

"""Database setup"""

basedir = os.path.abspath(os.path.dirname(__file__))
# TODO: Change to environment variable before launching
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'reviews.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
Migrate(app, db)
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



@app.route('/test')
def test():
    return ' '.join([doc.text for doc in document_store.get_all_documents()])


   






"""REST API for the haystack pipeline"""
# TODO: build REST API endpoint with GET for inference results


