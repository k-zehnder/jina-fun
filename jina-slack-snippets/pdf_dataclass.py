"""
This script extracts TEXT only from PDF. It will not do anything with images.
"""

#pip install pymupdf
from typing import List, Dict
from docarray import Document, DocumentArray, dataclass
from docarray.typing import Image, Text, JSON
from jina import Flow, Executor, requests
# import fitz
import pikepdf


# pdf = fitz.open('./data/pdf/sr71_medium.pdf')
# da = DocumentArray([Document(text=page.get_text().split("\n")) for page in pdf])

# da.summary()
# all_docs = da[:5, "text"]
# for doc in all_docs:
#     print(doc)
#     print("\n\n")
# print(da[:,'text'])

############################
# docs = DocumentArray.from_files(f"./data/pdf/*.pdf", recursive=True, size=num_docs)
d1 = Document(uri="/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/cats_are_awesome.pdf")
d2 = Document(uri="/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/sample_pdf.pdf")
docs = DocumentArray([d1, d2])


@dataclass
class PDFPage:
    images: List[Image]
    texts: List[Text]

f = Flow().add(
    uses='jinahub://PDFSegmenter',
)
with f:
    resp = f.post(on='/craft', inputs=docs)
    print(resp)
    print(type(resp)) # documentarrayinmemory
    # print(len(resp)) # 2
    print(f'{[c.mime_type for c in resp[0].chunks]}')

resp.summary()
print("--\n\n\n")
resp[0].summary()

final = []
for d in resp:
    obj = PDFPage(images=[], texts=[])
    for chunk in d.chunks:
        assert d.id == chunk.parent_id
        if chunk.mime_type == "image/*":
            obj.images.append(chunk.tensor)
        else:
            # sentencizer = Executor.from_hub(
            #     "jinahub://SpacySentencizer/v0.4",
            #     install_requirements=True,
            # )
            # sentencizer.segment(doc.chunks, parameters={})
            # sentencizer.segment(chunk, parameters={})
            # print(sentencizer)

            obj.texts.append(chunk.text)
    final.append(obj)
    print(obj)
# print(final)
