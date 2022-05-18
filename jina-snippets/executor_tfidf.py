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
        self.preprocess(docs)
        return self.compute(self.bows)

    def compute(self, bows_docarray):
        res = []
        for doc in bows_docarray:
            sentence, score = " ".join(doc.tags.get("data")), [self.tfidf(voc, doc) for voc in self.vocab]
            res.append([sentence, score])
        return self.results_formatter(res)

    def results_formatter(self, res):
        out = DocumentArray()
        for sentence, score in res:
            print(sentence, score)
            out.append(Document(embedding=np.array(score), tags={"sentence" : sentence, "score" : score}))
        return out

    def tfidf(self, word, sentence):
        tf = sentence.tags.get("data").count(word) / len(sentence.tags.get("data"))
        idf = np.log10(len(self.bows) / sum([1 for doc in self.bows if word in doc.tags.get("data")]))
        return round(tf*idf, 4)

    def preprocess(self, docs):
        bow = [doc.text.lower().split(" ") for doc in docs]
        for bag in bow:
            self.bows.append(Document(tags={"data" : bag}))
            for word in bag:
                self.vocab.add(word)
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

d1 = Document(text="is") # should be top result when matching to all zeros b/c "is" should have no "tdift-multiplier" since the word "is" is so commom in all documents and included in all documents in the collection
d2 = Document(text="The car is driven on the road")
d3 = Document(text="The truck is driven on the highway")
da = DocumentArray([d1, d2, d3])

with f:
    r = f.index(da)
    print(f"results: {r}")
    
print("[INFO] program complete.")
print([[r[i].tags.get("sentence"), r[i].tags.get("score")] for i in range(len(r))])
r.summary()


# example_embedded_query = np.random.random(len(r[0].tags.get("score")))
example_embedded_query = np.array([0.0] * len(r[0].tags.get("score")))
print(f"query embedding: {example_embedded_query}")
q = Document(embedding=example_embedded_query)
q.match(r, use_numpy=True)
q.summary()