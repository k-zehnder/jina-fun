from docarray import Document, DocumentArray
from docarray.document.generators import from_csv
from jina import Flow, Executor, requests


docs = from_csv('dataset.csv', field_resolver={'question': 'text'})


class MyTransformer(Executor):
    _total_calls = 0

    def __init__(self, parameter, **kwargs):
        super().__init__(**kwargs)
        self.parameter = parameter

    @requests(on='/foo')
    def foo(self, **kwargs):
        print(f'foo is doing cool stuff: {kwargs}')
        MyTransformer._total_calls += 1
        print(MyTransformer._total_calls)

class MyIndexer(Executor):
    _total_calls = 0

    @requests(on='/bar')
    def bar(self, **kwargs):
        print(f'bar is doing cool stuff: {kwargs}')
        MyIndexer._total_calls += 1
        print(MyIndexer._total_calls)


flow = (
    Flow()
        .add(name='MyTransformer', uses=MyTransformer,
        uses_with={"parameter" : "default_state1"})
        .add(name='MyIndexer', uses=MyIndexer)
)

with flow:
    res = flow.post(on="/foo", inputs=from_csv('/Users/peppermint/Desktop/codes/python/jina-fun/jina-slack-snippets/data/csv/anime.csv', return_results=False, show_progress=True))

    res2 = flow.post(on="/bar", inputs=from_csv('/Users/peppermint/Desktop/codes/python/jina-fun/jina-slack-snippets/data/csv/anime.csv', return_results=False, show_progress=True))

print("[INFO] program complete.")