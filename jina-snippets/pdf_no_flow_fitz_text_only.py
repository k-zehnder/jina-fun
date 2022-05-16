"""
This script extracts TEXT only from PDF. It will not do anything with images.
"""

from docarray import Document, DocumentArray
import fitz


pdf = fitz.open('jina-slack-snippets/data/pdf/sr71_medium.pdf')
da = DocumentArray([Document(text=page.get_text().split("\n")) for page in pdf])

da.summary()
all_docs = da[:5, "text"]
for doc in all_docs:
    print(doc)
    print("\n\n")
print(da[:,'text'])