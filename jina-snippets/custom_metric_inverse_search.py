from jina import Document, DocumentArray
import random
import numpy as np
from docarray.math.distance.numpy import cosine

# This script shows you how to "do the opposite" of da.find(query, metric="cosine", limit=5, exlude_self=True). Aka we want to get last-k instead of top-k, not caring what the magnitude of the scores are...just the last-k (least similar) documents

N, D = 4, 128
da = DocumentArray.empty(N)
da.embeddings = np.random.random([N, D])

q = np.random.random([D])
print("distance", da.find(q)[:, ["scores__cosine__value", "id"]])

def inv_cosine(x, y, *args):
    return - cosine(x, y)

print("inv_distance", da.find(q, metric=inv_cosine)[:, ["scores__inv_cosine__value", "id"]])