from docarray import Document, DocumentArray
from jina import Flow, Executor, requests
import numpy as np
import pandas as pd


class TFIDFer(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter
        self.bows = DocumentArray()
        self.vocab = set()

    @requests
    def run(self, docs, **kwargs):
        bows_da = self.preprocess(docs)
        res = self.compute(bows_da)
        print(f"results: {res}")
        return DocumentArray(res=res)

    def compute(self, bows_docarray):
        res = []
        for doc in bows_docarray:
            res.append([self.tfidf(voc, doc) for voc in self.vocab])
        return res

    def tfidf(self, word, sentence):
        tf = sentence.tags.get("data").count(word) / len(sentence.tags.get("data"))
        idf = np.log10(len(self.bows) / sum([1 for doc in self.bows if word in doc.tags.get("data")]))
        return round(tf*idf, 4)

    def preprocess(self, docs):
        bow = [doc.text.lower().split(" ") for doc in docs]
        for bag in bow:
            self.bows.append(Document(tags={"data" : bag}))
            for letter in bag:
                self.vocab.add(letter)
        return self.bows

f = (
    Flow()
    .add(
        uses=TFIDFer,
        uses_with={
            "parameter" : "some default executor state 1",
        }
    )
)

d1 = Document(text="The car is driven on the road")
d2 = Document(text="The truck is driven on the highway")
da = DocumentArray([d1, d2])


with f:
    r = f.index(da)
    print(f"results: {r}")
    
print("[INFO] program complete.")
print([r[i].tags.get("data") for i in range(len(r))])
r.summary()