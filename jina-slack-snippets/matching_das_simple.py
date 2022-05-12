from docarray import Document, DocumentArray, dataclass
from docarray.typing import Text, Image, JSON
import numpy as np


doc1 = Document(embedding=np.array([1,2,3]))
doc2 = DocumentArray([Document(embedding=np.array([0,0,0]))])

res = doc1.match(doc2, metric='euclidean', limit=3) # returns Document
res.summary()

print(res.matches[0].scores["euclidean"].value)
# print(res['@m', ('uri', 'scores__cosine__value')]) TypeError: 'Document' object is not subscriptable