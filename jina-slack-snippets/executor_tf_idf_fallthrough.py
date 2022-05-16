from docarray import Document, DocumentArray
from jina import Flow, Executor, requests


class TFidf(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter
    
    @requests
    # @requests(on="/prep")
    # @requests(on="/index") # use this decorator when want to do f.index(inp)
    def prep_documents(self, docs, **kwargs):
        # split_docs = list(map(lambda d: d.text.split(), docs))
        vocab = set()
        for doc in docs:
            for word in doc.text.split(" "):
                if word not in vocab:
                    vocab.add(word)
        voc = DocumentArray(Document(vocab=list(vocab)))
        return voc

class Debugger(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter

    @requests 
    # NOTE: this "bare" requests is how we get the above Executor to "fallthrough" the flow to this executor b/c thats how the Flow specifies how out Documents should go through the Flow
    # if you didnt use a "bare" requests decorator, then this Executor wouldnt be visited by the Flow because it wouldn't know "where to go"
    def show_vocab(self, docs, **kwargs):
        docs.summary()
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
inp = DocumentArray([d1, d2, d3])

with f:
    # r = f.post(on="/prep", inputs=inp)
    r = f.index(inp) # best practice for production re: docs
    print(f"results: {r}")
    
print("[INFO] program complete.")
r.summary()