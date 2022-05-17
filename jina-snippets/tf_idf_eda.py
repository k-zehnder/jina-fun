from docarray import Document, DocumentArray
from jina import Flow, Executor, requests
import numpy as np


a = "the car is driven on the road".split()
b = "the truck is driven on the highway".split()

docs = [a, b]
print(docs)

unique_words = set(a + b)
print(unique_words)


def tfidf(word, sentence):
    tf = sentence.count(word) / len(sentence)
    idf = np.log10(len(docs) / sum([1 for doc in docs if word in doc]))
    return round(tf*idf, 4)

print(tfidf("car", docs[0]))

res = []
for doc in docs:
    tmp = []
    for word in unique_words:
        print(doc, word)
        print(tfidf(word, doc))
        print("\n")
        tmp.append(tfidf(word, doc))
    res.append(tmp)
print(res)

class TFIDFer(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter
        self.bows = DocumentArray()

    @requests
    def run(self, docs, **kwargs):
        pass

    def split_docs(self, docs):
        for doc in docs:
            self.bows.extend([doc.text.split(" ")])
d1 = Document(text="the car is driven on the road")
d2 = Document(text="the truck is driven on the highway")