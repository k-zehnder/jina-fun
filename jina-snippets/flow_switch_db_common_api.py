# see 
# https://docs.jina.ai/how-to/flow-switch/#how-to-build-switches-in-a-flow

from jina import Flow, Executor, DocumentArray, requests


class DB1(Executor):
    db = DocumentArray.empty(10)

    @requests(on='/search1')
    def foo(self, **kwargs):
        return self.db


class DB2(Executor):
    db = DocumentArray.empty(5)

    @requests(on='/search2')
    def foo(self, **kwargs):
        return self.db


class CommonAIPrep(Executor):
    ...


f = Flow().add(name='common_stuff', uses=CommonAIPrep).add(uses=DB1).add(uses=DB2, needs='common_stuff').needs_all()

f.plot('f.svg')

with f:
    print(f.post('/search1', ))
    print(f.post('/search2', ))