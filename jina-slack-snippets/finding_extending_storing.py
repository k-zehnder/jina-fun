import numpy as np
from docarray import DocumentArray, Document


N, D = 100, 3

documents = DocumentArray(
    storage='sqlite', 
    config={
        'connection': '.sqlite_index'
    })

with documents:
    documents.extend([
        Document(embedding=np.random.random(D), tags={'channel_id': str(i), 'idd' : str(i)}) for i in range(N)
    ])

# result = documents.find(np.random.random(3))
# result = documents.find({'modality': {'$eq': 'D'}})
some_doc = Document(channel_id=str(10005))
documents.extend([some_doc])
result = documents.find({"tags__channel_id" : {"$eq" : "10005"}})
assert len(result) > 0
print(result)
result = documents.find({"tags__channel_id" : {"$eq" : "42"}})
assert len(result) > 0

print(result)
result.summary()
result[0].summary()
