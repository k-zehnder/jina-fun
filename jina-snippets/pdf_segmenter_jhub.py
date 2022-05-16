from docarray import DocumentArray, Document
from jina import Flow
import fitz

# ---------------- data
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
# ---------------- deal with results
for doc in resp:
    print(doc.mime_type)
    if doc.mime_type == "text/plain":
        print(doc.text)
    elif doc.mime_type == "image/*":
        print(doc.tensor)


"""
[RANDOM REFERENCE GARBAGE CODE]
# show how to 'manually' index
# below results assume "catsareawesome.pdf" is input
# resp.summary()
# resp[0].chunks[0].summary() # image here
# resp[0].chunks[1].summary() # image here
# resp[0].chunks[2].summary() # text here

# show how to index by nested structure
# print(resp["@c"]) # chunks

# show how to use element selector and attribute selector
# print(resp[:, "id"])
# print(resp[0:2, "parent_id"])
# print(resp["@c", "mime_type"]) 
# print(resp["@c", ["id", "mime_type"]])

# show how to plot images in the pdf
resp.summary()
da1 = DocumentArray([Document(resp[0].chunks[0])]) # image containing chunk
da1.plot_image_sprites()

# show how to print text in the pdf
da2 = resp[0].chunks[1] # text containing chunk
print(da2.text)

# conditionally print text/image depending on mime_type
for doc in resp:
    for c in doc.chunks:
        if c.mime_type == "text/plain":
            print(c.text)
            print("\n\n")
        else:
            print(doc.tensor)

# show how to find documents in a documentarray based on some condition
# res = da.find({"mime_type" : {"$eq" : "text/plain"}})
# res = resp.find({"parent_id" : {"$eq" : resp[0].chunks[1].parent_id}})
# print(f"res: {res}")
# res.summary()
"""