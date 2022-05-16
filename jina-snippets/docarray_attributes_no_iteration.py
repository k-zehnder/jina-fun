import os
import webbrowser
from pathlib import Path
from jina import Flow, Executor, requests
from jina.logging.predefined import default_logger
from docarray.document.generators import from_csv
from jina import Document, DocumentArray, Flow, Executor, requests


d1 = Document(id=1, some_key="some_value1")
d2 = Document(id=2, some_key="some_value2")
d3 = Document(id=3, some_key="some_value3")

da = DocumentArray([d1, d2, d3])
da.summary()
print(da[:, "tags__some_key"])




