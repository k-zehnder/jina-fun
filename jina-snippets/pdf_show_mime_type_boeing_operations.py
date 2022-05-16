from docarray import DocumentArray, Document
from jina import Flow


da = DocumentArray([Document(uri='./data/pdf/747-400_operations_manual.pdf')])

f = Flow().add(
    uses='jinahub://PDFSegmenter',
)
with f:
    resp = f.post(on='/craft', inputs=da, show_progress=True)
    print(f'{[c.mime_type for c in resp[0].chunks]}')

# show how to get summary documentarray returned as response results
resp.summary()

# how to show all the photos available in the pdf
for doc in resp[:5]:
    for c in doc.chunks:
        if c.mime_type == "text/plain":
            # print(c.text)
            continue
        elif c.mime_type == "image/*":
            # print(c.tensor)
            show = DocumentArray([Document(tensor=c.tensor)])
            show.plot_image_sprites()
            # press 'p' to toggle through photos