"""
This file is for practice with Flow topology and controlling what input Documents go to which Executor. There is a lot of fine tuned control with how Jina lets you control the Flow, so it's important be familiar with how the Documents move through the Flow, in particular, with respect to the @requests(on="/index") decorator, as well as how default parameters for Executors (e.g., super().__init__(**kwargs)) are passed in the Flow (e.g, uses_with={"param1" : "some_starting_state"}) when you define it.

Sidenote:
Notice here that even though we are only specifying the /start_me endpoint to be used by the first Executor, its important to notice that the second Executor is still used, because the Flow topology states that after we go to the first Executor the documents will be passed to the second Executor. Thats why we don't have to call the "/identify" enpoint explicitly, the Flow handles that for us. If we were to uncomment the requests(on="/identify") in the second Executor, however, this behavior would change because we would have to specify specifically that we wanted to go to "/identify". By default, if you use requests WITHOUT a specific (on="/something_explicit_to_come_here"), then that method will be called by default when you go to that Executor. Also note that your default states "parameter1" and "parameter2" for the first Executor are declared in the Flow when you define the toplogy, NOT when you actually do a flow.post() to that endpoint. The flow.post() just takes the input DA and some configuration arguments that handle pretty printing, etc.
TIP: don't forget backslashes with requests(on="/index") and flow.post(on="/index") 

5-12-22
KZ
"""


from jina import Flow, Executor, Document, DocumentArray, requests
from docarray import dataclass
from docarray.typing import JSON, Text, Image


class StartExec(Executor):
    def __init__(self, parameter1, parameter2, **kwargs):
        super().__init__(**kwargs)
        self.parameter1 = parameter1
        self.parameter2 = parameter2
    
    @requests(on="/start_me")
    def start_me(self, docs, **kwargs):
        for doc in docs:
            print(doc)


class Identifier(Executor):
    def __init__(self, starting_state, **kwargs):
        super().__init__(**kwargs)
        self.starting_state = starting_state

    # @requests(on="/identify") # NOTE: much different behavior if you do this
    @requests # allows "fall through" of first Executor to this one (as defined by Flow)
    def identify(self, docs, **kwargs):
        print("[INFO] identifying default starting state...")
        print(self.starting_state)

        print("[INFO] printing docs again....")
        for doc in docs:
            print(doc)

        
@dataclass
class MultiModal:
    txt: Text # docarray dataclass type --> sibling Document
    img: Image # docarray dataclass type --> sibling Document
    prim_type: str # primitive python type --> tag of parent doc

# siblings
d1 = Document(uri="/Users/peppermint/Desktop/codes/python/jina-fun/jina-slack-snippets/data/images/fashion_images_very_small/1163.jpg")
d2 = Document(text="hello")

# dictionary will go in parent b/c primitive python type, would go as sibling instead of on parent if used docarray JSON type instead
dictionary = {"some key" : "some value"}

# parent
mmdoc = Document(**dictionary, chunks=[d1, d2])
mmdc = Document(mmdoc)
mmdc.summary()

flow = (
    Flow()
    .add(
        uses=StartExec,
        name="start_exec",
        uses_with={"parameter1" : "param1", "parameter2" : "param2"}, 
    ).add(
        uses=Identifier, 
        name="identifier",
        uses_with={"starting_state" : "ready for action"}
    )
)

with flow:
    returned_docs1 = flow.post(
                    on="/start_me", 
                    inputs=DocumentArray([mmdc]),
                    return_responses=True,
                    show_progress=True
                )

# NOTE: BELOW is much DIFFERENT than ABOVE (especially w/r/t flow.post() and @requests in Executors....this is a "must understand" concept)
# with flow:
#     returned_docs1 = flow.post(
#                     on="/start_me", 
#                     inputs=DocumentArray([mmdc]),
#                     return_responses=True,
#                     show_progress=True
#                 )
#     returned_docs2 = flow.post(
#                     on="/identify", 
#                     inputs=DocumentArray(Document(text="some other document")),
#                     return_responses=True,
#                     show_progress=True
#                 )

print("[INFO] program complete.")
# print(returned_docs.summary()) # cant do this, returns LIST of Request not DocumentArray

