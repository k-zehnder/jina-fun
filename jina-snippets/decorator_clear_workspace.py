"""
This script is just for practice with decorators but also could be used in a Jina project to clear workspace before running Flow like is common in early stages in project.
"""


# ---------------------------------- Imports ----------------------------------
import os
import shutil
import pathlib
from jina import Flow
from docarray import Document, DocumentArray
from helpers import clear_workspace
from functools import wraps


def remove_workspace():
    current_dir = pathlib.Path(__file__).parent.resolve()
    if os.path.exists(os.path.join(current_dir, "workspace")):
        print("[INFO] removing existing workspace...")
        shutil.rmtree(os.path.join(current_dir, "workspace"))

def clear_workspace(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        remove_workspace()
        result = func(*args, **kwargs)
        print("decorator used.")
        return result
    return wrapped


# --------------------------------- Get data ----------------------------------
# data = "https://www.gutenberg.org/files/1342/1342-0.txt"
data = "https://www.py4e.com/code3/romeo-full.txt"
d = Document(uri=data).load_uri_to_text()
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())
da.apply(lambda d: d.embed_feature_hashing())
da.summary()

# ------------------------------ Perform maching ------------------------------
@clear_workspace
def match():
    q = (
        Document(text='embrace the chaos of the masses')
        .embed_feature_hashing()
        .match(da, limit=5, exclude_self=True, metric='jaccard', use_scipy=True)
    )
    return q

q = match()


# ------------------------------ Handle results -------------------------------
print(f"[INFO] results for query: '{q.text}'")
for m in q.matches:
    print(f"> {m.scores['jaccard'].value:.3f} - {m.text}")