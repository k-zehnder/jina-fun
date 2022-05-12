
# ---------------------------------- Imports ----------------------------------
from jina import Flow
from docarray import Document, DocumentArray

# --------------------------------- Get data ----------------------------------
data = "https://www.py4e.com/code3/romeo-full.txt"
d = Document(uri=data).load_uri_to_text()
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())
da.apply(lambda d: d.embed_feature_hashing())
da.summary()

# ------------------------------ Perform maching ------------------------------
q = (
    Document(text='embrace the chaos of the masses')
    .embed_feature_hashing()
    .match(da, limit=5, exclude_self=True, metric='jaccard', use_scipy=True)
)

# ------------------------------ Handle results -------------------------------
print(f"[INFO] results for query: '{q.text}'")
for m in q.matches:
    print(f"> {m.scores['jaccard'].value:.3f} - {m.text}")