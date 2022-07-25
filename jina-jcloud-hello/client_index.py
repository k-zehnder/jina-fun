from jina import Client, Document, DocumentArray
import numpy as np


c = Client(host='https://433038414c.wolf.jina.ai')

# print(c.post("/index", DocumentArray(Document="Mary had a little lamb doc 1"), show_progress=True))

# print(c.post("/index", DocumentArray(Document="This is such cool tech bro! doc 2"), show_progress=True))

# da = DocumentArray([Document(text="Mary had a little lamb doc 1"), Document(text="This is such cool tech bro! doc 2")])

#TODO: put episode number in tag so when you get results you can see which episode they are coming from along with their cosine SIMILARITY score ==> cosine distance = 1 - cosine_similarity

d = Document(uri="https://www.grc.com/sn/sn-880.txt").load_uri_to_text()
da = DocumentArray(Document(text=s.strip()) for s in d.text.split("\n") if s.strip())

r = c.post(on="/index", inputs=da, show_progress=True)
r[0].summary()

print("\n==================================\n")

d = Document(uri="https://www.grc.com/sn/sn-879.txt").load_uri_to_text()
da = DocumentArray(Document(text=s.strip()) for s in d.text.split("\n") if s.strip())

r = c.post(on="/index", inputs=da, show_progress=True)
r[0].summary()
