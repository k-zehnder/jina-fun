"""
What does this script do?
This script is practice simple text matching using example from docs with batman data. This script will allow text searching of a batman script and demonstrated how to preprocess both the data and the query so that we can search.

# more info: 
# https://docarray.jina.ai/datatypes/text/?utm_source=learning-portal

"""
from jina import Flow
from docarray import Document, DocumentArray
from helpers import print_search_results, clear_workspace


# --------- get data
d = Document(uri="./data/text/batman.txt").load_uri_to_text()
d.summary()
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())
da.summary()
da.apply(lambda d: d.embed_feature_hashing())

print("[INFO] clearing workspace.")
clear_workspace("./workspace")

# --------- preprocess data
q = (
    Document(text='embrace the chaos of the masses')
    .embed_feature_hashing()
    .match(da, limit=5, exclude_self=True, metric='jaccard', use_scipy=True)
)

# --------- handle results
print(f"[INFO] results for query: '{q.text}'")
res = q.matches[:, ('text', 'scores__jaccard')]
for r in zip(res[0], res[1]):
    print(f"> {r[1].value:.3f} - {r[0]}")
    print("\n")