import numpy as np
from docarray import DocumentArray, Document


N, D = 100, 3

documents = DocumentArray(
    storage='sqlite', 
    config={
        'connection': 'data/extending_documents'
    })

with documents:
    documents.extend([
        Document(embedding=np.random.random(D), tags={'channel_id': str(i)}) for i in range(N)
    ])

result = documents.find(np.random.random(3))
print(result)
result.summary()
result[0].summary()