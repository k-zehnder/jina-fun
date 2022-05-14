import numpy as np
from docarray import DocumentArray, Document


N, D = 100, 3

documents = DocumentArray(
    storage='sqlite', 
    config={
        'connection': 'jina-slack-snippets/persisted_data/sqlite_index'
    })

with documents:
    # documents.extend([
    #     Document(embedding=np.random.random(D), tags={'channel_id': str(i)}) for i in range(N)
    # ])
    documents.extend([Document(embedding=np.random.random(D), tags={"channel_id" : str(i)}) for i in range(D)])
# print(help(result.find))


# find d in da by random embedding (nearest neighbor)
result = documents.find(np.random.random(3))
print(type(result)) # da
print(result)
result.summary()
assert len(result) != 0
d = Document(text="i dont have matches set yet")
assert len(d.scores.items()) == 0 # show that a random new d will not start with any scores attribute set. this will be set when we find, and thats why result above has a scores attribute set as a "consequence" of being found nearest neighbor wise
assert len(result[0].scores) != 0 # checks to make sure first d in da has ".score" attribute now set as a "consequence" of being "found" by documents.find()

result = documents.find(Document(embedding=np.array([0,0,0]), tags={"channel_id" : "0"}), limit=2, metric="cosine")
print(type(result)) # NOTE: list
print(result)
result[0].summary()
print(result[0].embeddings)

# intentionally search for d that doesnt exist in D to understand this behavior
result = documents.find({'modality': {'$eq': 'D'}})
print(type(result)) # da
assert len(result) == 0 # expecting not to find this d
print(result)
result.summary()

# find d in da by specific tag number
some_doc = Document(channel_id=str(10005))
documents.extend([some_doc])
result = documents.find({"tags__channel_id" : {"$eq" : "10005"}})
print(type(result))
assert len(result) != 0
print(result)
result.summary()
result[0].summary()

# # same as above just selecting for equality for different value
result = documents.find({"tags__channel_id" : {"$eq" : "42"}})
assert len(result) == 0
print(type(result))
print(result)
result.summary()
