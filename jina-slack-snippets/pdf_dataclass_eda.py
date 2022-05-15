from typing import List, Dict
from docarray import Document, DocumentArray, dataclass
from docarray.typing import Image, Text, JSON
from jina import Flow, Executor, requests
import cv2


d1 = Document(uri="/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/cats_are_awesome.pdf")
d2 = Document(uri="/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/somatosensory.pdf")
docs = DocumentArray([d1, d2])


@dataclass
class PDFPage:
    images: List[Image]
    texts: List[Text]
    tags: dict # primitive python type --> tag on parent

f = Flow().add(
    uses='jinahub://PDFSegmenter',
)
with f:
    resp = f.post(on='/craft', inputs=docs) # returns -> documentarray with 2 documents (1 document in documentarray per pdf)
    print(resp)
    print(type(resp)) # documentarrayinmemory
    print(len(resp)) # 2
    for idx, doc in enumerate(resp):
        for chunk in doc.chunks:
            print(f">pdf #: {idx} - mime_type: {chunk.mime_type}")
    # print(f'{[c.mime_type for c in resp[0].chunks]}')


resp.summary()
print("--\n\n\n")
resp[0].summary()
resp[1].summary()

final = []
count = 0
for d in resp:
    obj = PDFPage(images=[], texts=[], tags={"doc0_uri" : d.uri})
    for chunk in d.chunks:
        assert chunk.parent_id == d.id
        if chunk.mime_type == "image/*":
            obj.images.append(chunk.tensor)
            # cv2.imshow("window", chunk.tensor)
            # cv2.waitKey()
        else:
            obj.texts.append(chunk.text)
        count += 1
    final.append(obj)
    # print(obj)
print(final)

for dc in final:
    # print(dc)
    print("\n\n")
    print(f"imgs len {len(dc.images)}")
    print(f"txt len {len(dc.texts)}")
    print(f"doc0 tags: {dc.tags}")
    # print(f"doc0 tags: {dc.}")
    print("\n\n")