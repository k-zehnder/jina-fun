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

class ThreeExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        print(f"foo was here and got {len(docs)} docs.")

class CommonAIPrep(Executor):
    ...


f = (
    Flow()
    .add(
        uses=CommonAIPrep,
        name='common_stuff'
    ).add(
        uses=DB1
    ).add(
        uses=DB2, 
        needs='common_stuff'
    ).add(
        uses=ThreeExecutor,
        name="threeExecutor"
    ).needs_all()
)

f.plot('/Users/peppermint/Desktop/codes/python/jina-fun/jina-snippets/f.svg')

with f:
    print(f.post('/search1', ))
    print(f.post('/search2', ))
