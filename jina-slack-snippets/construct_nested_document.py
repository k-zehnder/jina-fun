from docarray import Document, DocumentArray
import numpy as np


d1 = Document(
        chunks=[
            Document(
                embedding=np.array([1,2,3]), 
                chunks=[
                    Document(embedding=np.array([0,0,1])), 
                    Document(embedding=np.array([1,2,3]))
                ]
            ), 
            Document(
                embedding=np.array([0,0,0])
            ),
        ]
)
d1.summary() 

"""
[REFERENCE GARBAGE -- DO NOTS]
# print(len(d1)) # TypeError: object of type 'Document' has no len()
# d1[...].summary() # only with DocumentArray

# da_d1.chunks[0].summary() #AttributeError: 'DocumentArrayInMemory' object has no attribute 'chunks'
# da_d1[0].chunks.summary() # ok
"""

q = Document(embedding=np.array([1,2,3])) # unexpected if plural "embedding"
m = Document(embedding=np.array([0,0,0])) # unexpected if plural "embedding"
m = DocumentArray([m])
m.summary()
matches = q.match(m)
print(matches)

"""
[REFERENCE GARBAGE -- DO NOTS]
# qq = d1[0] # TypeError: 'Document' object does not support indexing
"""

qq = DocumentArray([d1])
# qq.summary()
qq = qq[0].chunks[0].chunks[0]
qq.summary()
m = DocumentArray(qq)

matches = qq.match(m)
print(matches)