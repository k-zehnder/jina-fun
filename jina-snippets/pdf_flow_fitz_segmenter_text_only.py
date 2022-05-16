from docarray import DocumentArray, Document
from jina import Flow
import fitz

# ---------------- data
"""
THIS WILL PROPERLY SENTENCIZE AND ALLOWS YOU TO SEE WHAT PAGE EACH TEXT CAME FROM -- BUT WILL *NOT* GET THE IMAGES FROM THE PDF, IT WILL *ONLY* GET THE TEXT FROM PDF
"""
pdf = fitz.open('./data/pdf/sr71_medium.pdf')
da = DocumentArray([Document(text=page.get_text()) for page in pdf])
da.summary()

# ---------------- define flow
f = (
    Flow()
    .add(
        uses="jinahub://PDFSegmenter",
    )
    .add(
        uses="jinahub://SpacySentencizer/latest",
    )
)

# ---------------- open context to flow
with f:
    resp = f.post(on='/craft', inputs=da)
    # print(f'{[c.mime_type for c in resp[0].chunks]}')
    print(resp["@c", "mime_type"])

resp.summary()
for doc in resp:
    print(doc)
    print("\n\n")