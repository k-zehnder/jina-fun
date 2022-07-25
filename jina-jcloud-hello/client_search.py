from jina import Client, Document, DocumentArray
import numpy as np


c = Client(host='https://433038414c.wolf.jina.ai')

qx_da = DocumentArray([Document(text="what is the topic of this weeks podcast?")])

r = c.post(on="/search", inputs=qx_da, show_progress=True)
r[0].summary()

message = f"Your results for query: {qx_da[0].text}"
print(f"[INFO] {message}")

for match in r[0].matches[:5]:
    score = match.scores["cosine"].value
    print(f"> {score:.4f}: {match.text[:250]}")
