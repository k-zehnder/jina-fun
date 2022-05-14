import kaggle
from docarray import Document, DocumentArray


d1 = Document(text="hello")
d2 = Document(text="there")

# da = DocumentArray([d1, d2])

da = DocumentArray()
da.extend([d1])
da.extend([d2])

da.summary()

