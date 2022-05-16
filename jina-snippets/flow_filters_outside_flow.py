from jina import Flow, Executor, requests
from docarray import Document, DocumentArray

class DummyExecutor(Executor):
    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter
    
    @requests(on="/dummy")
    def some_method(self, docs, **kwargs):
        print("[INFO] printing text attribute from each Document in DocumentArray")
        for doc in docs:
            print(doc)
            print(doc.tags)

# Jina Flows allow you to use the DocArray query language to filter a condition for every Executor
# Its helpful when you want to, for example, send images to one Executor, and text to a different Executor
# To do this, you pass a condition to the when parameter in flow.add()
f = (
    Flow()
    .add(
        uses=DummyExecutor,
        uses_with={"parameter" : "some_initial_state"},
        when={"tags__some_random_tag" : {"$eq" : 5}}
    )
)

with f:
    f.post(
        on="/dummy", 
        inputs=DocumentArray(
            [
                Document(
                    some_random_tag=5, text="some_documents_text"
                ), 
                Document(
                    text="some_other_documents_text", some_random_tag=10
                )
            ]
        )
    )

# in the use case where you are trying to seperate Documents according to the data modality they hold, you need to choose a condition accordingly.
# define text and tensor filters
text_condition = {"text" : {"$exists" : True}}
tensor_condition = {"tensor" : {"$exists" : True}}

# ^^ these conditions specify that only Documents that hold data of a specific modality can pass the filter

# Try filters outside the FLow