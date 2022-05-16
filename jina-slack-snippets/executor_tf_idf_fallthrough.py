from docarray import Document, DocumentArray
from jina import Flow, Executor, requests
import numpy as np


class TFidf(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter
    
    @requests
    def prep_documents(self, docs, **kwargs):
        vocab = set()
        for doc in docs:
            for word in doc.text.split(" "):
                if word not in vocab:
                    vocab.add(word)
        return DocumentArray(Document(vocab=list(vocab)))

class Debugger(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter

    @requests 
    def show_vocab(self, docs, **kwargs):
        print(docs[:, ("id", "tags__vocab")])

f = (
    Flow()
    .add(
        uses=TFidf,
        uses_with={"parameter" : "some default executor state 1."}
    ).add(
        uses=Debugger,
        uses_with={"parameter" : "some default executor state 2."}
    )
)
d1 = Document(text="I am doc1")
d2 = Document(text="I am an alien from mars doc2")
d3 = Document(text="I am an pilot from the sun doc3")
d4 = Document(embedding=np.random.random(3))
mixed_da = DocumentArray([d1, d2, d3])

# show how you would get just the d in this da using a text filter
text_filter = mixed_da.find({"text" : {"$exists" : True}})
assert len(text_filter) == 3 # filter excludes d without .text set

with f:
    r = f.index(text_filter) # best practice to use f.index() (not f.post()) for indexing re: docs 
    print(f"results: {r}")
    
print("[INFO] program complete.")
r.summary()