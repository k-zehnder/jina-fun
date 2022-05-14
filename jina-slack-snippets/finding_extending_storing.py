import numpy as np
from docarray import DocumentArray, Document


# num docs, dims
N, D = 100, 3

documents = DocumentArray(
    storage='sqlite', 
    config={
        'connection': 'jina-slack-snippets/persisted_data/sqlite_index'
    })

with documents:
    documents.extend([Document(embedding=np.random.random(D), tags={"channel_id" : str(i)}) for i in range(N)])

# print(help(result.find))

# find d in da by random embedding (nearest neighbor)
result = documents.find(np.random.random(3))
assert isinstance(result, DocumentArray)
print(result)
result.summary()
assert len(result) != 0 # should return da with matches
d = Document(text="i dont have matches set yet")
assert len(d.scores.items()) == 0 # show that a random new d will not start with any scores attribute set. this will be set when we find, and thats why result above has a scores attribute set as a "consequence" of being found nearest neighbor wise
assert len(result[0].scores) != 0 # checks to make sure first d in da has ".score" attribute now set as a "consequence" of being "found" by documents.find()

"""
Reminder: below returns list NOT documentarray
"""
result = documents.find(Document(embedding=np.array([0,0,0]), tags={"channel_id" : "0"}), limit=2, metric="cosine")
assert len(result) != 0 # expecting 2 nearest neighbor matches 
assert isinstance(result, list) # NOTE: returns list of documentarray objects
assert len(result[0][0].scores) != 0 # element 1 in returned list of documentarrays should have a score because its the consequence of being "found"
print(result)
result[0].summary()
print(result[0].embeddings)

# intentionally search for d that doesnt exist in da to understand this behavior
result = documents.find({'modality': {'$eq': 'D'}})
assert isinstance(result, DocumentArray)
assert len(result) == 0 # expecting not to find this d
print(result)
result.summary()

# selecting for equality of tags called "channel_id"
result = documents.find({"tags__channel_id" : {"$eq" : "42"}})
assert isinstance(result, DocumentArray)
assert len(result) != 0
print(result)
result.summary()


# finding again by embedding random --> e.g. [0.17649021 0.93252586 0.89824643]
result = documents.find(np.random.random(D))
assert len(result) != 0
assert isinstance(result, DocumentArray)
print(type(result)) # NOTE: list
print(result)
result[0].summary()
print(result[0].embedding) # singular