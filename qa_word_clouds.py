import pandas as pd
import matplotlib.pyplot as plt
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.reader.farm import FARMReader
from haystack.pipeline import ExtractiveQAPipeline
from collections import Counter
from wordcloud import WordCloud


# load and transform data and put it in a document store
data = pd.read_csv('QA-WordClouds/Womens Clothing E-Commerce Reviews.csv')

# convert dataframe to docs
docs = [{"text": str(text)} for text in data['Review Text']]

print('done')

doc_store = InMemoryDocumentStore()
doc_store.write_documents(docs)
# get haystack pipe with reader and retriever
# get retriever
retriever = TfidfRetriever(document_store=doc_store)
# model for question answering:
model_name = 'distilbert-base-cased-distilled-squad'
reader = FARMReader(model_name_or_path=model_name, progress_bar=False, return_no_answer=False)

# finally the pipe
pipe = ExtractiveQAPipeline(reader, retriever)


# ask questions and get results from the pipe
question='How are the colors?'

answers = pipe.run(query=question, params={'Retriever': {'top_k': 100}, 'Reader': {'top_k': 25}})


print('Got the answers!')
# visualize them with word clouds

results = []
for answer in answers['answers']:
    results.append(answer['answer'])
counter = Counter(results)

# wordcloud
cloud = WordCloud()
cloud.generate_from_frequencies(counter)
plt.figure(figsize=(16,8))
plt.imshow(cloud)
plt.axis('off')
plt.savefig('testcloud.png')