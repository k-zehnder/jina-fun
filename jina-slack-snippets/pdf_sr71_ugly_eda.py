from docarray import DocumentArray, Document
from jina import Flow


# da = DocumentArray([Document(uri="./data/pdf/sr71.pdf")])
# da = DocumentArray([Document(uri='./data/pdf/sr71_crowood_aviation.pdf')])
da = DocumentArray([Document(uri='./data/pdf/sr71_medium.pdf')])


f = Flow().add(
    uses='jinahub://PDFSegmenter',
)
with f:
    resp = f.post(on='/craft', inputs=da, show_progress=True)
    print(f'{[c.mime_type for c in resp[0].chunks]}')

# show how to get summary documentarray returned as response results
resp.summary()
print(len(resp["@c"]))

chunk_count = 0
chunk_text = 0
chunk_image = 0

# chunks are ordered by type...so images first then text chunks thats why can index from end of the list to get the text only chunks
# for c in resp["@c[-45:]"]:
for c in resp["@c"]:
    chunk_count += 1
    if c.mime_type == "text/plain":
        chunk_text += 1
        print(c.text[:500])
        print("--\n\n")
    # elif c.mime_type == "image/*":
        # chunk_image += 1
        # print(c.tensor)
        # show = DocumentArray([Document(tensor=c.tensor)])
        # show.plot_image_sprites()
        # press 'p' to toggle through photos

print(f"program complete: {chunk_count}")
print(f"chunk text count: {chunk_text}")
print(f"chunk image count: {chunk_image}")

# show how to access documents
# some_texts = resp["@c[:5]", ["id", "text"]] # returns 2-D list not documentarray
# print(some_texts)
# remember: can't do below because resp is a 2-d list, not a documentarray
# for doc in some_texts:
    # print(doc.text)

# how to loop through and print id and corresponding text for that id
# for s in zip(some_texts[0], some_texts[1]):
#     print(s)
#     print("\n")
# some_texts.summary() # cant do this, returns 2-D list not documentarray


# how to show all the photos (or text, or both) by changing logic in code block below to show whats available in the pdf
# count = 0
# doc_count = 0
# for doc in resp[:5]:
#     count += 1
#     for c in doc.chunks:
#         if c.mime_type == "text/plain":
#             # print(c.text)
#             continue
#         elif c.mime_type == "image/*":
#             # print(c.tensor)
#             show = DocumentArray([Document(tensor=c.tensor)])
#             # show.plot_image_sprites()
#             count += 1
#             # press 'p' to toggle through photos

# print(f"program complete: {count}")

all_chunks = ['image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'image/*', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain', 'text/plain']
print(len(all_chunks))