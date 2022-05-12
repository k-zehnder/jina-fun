from docarray import Document, DocumentArray, dataclass
from docarray.typing import Text, Image, JSON
import numpy as np
import torchvision

"""
*[Embedding]*
Embedding is a 1, D representation of a Document and plays an important role in machine learning. The embedding information is not the data itself, but an abstract representation of data as a list of numbers.
"""
d1 = Document(embedding=np.array([1,2,3]))
da1 = DocumentArray([d1])
# da1.summary()


"""
*[Fill embedding via neural network]*
Usually embedding is not set manually like this, but rather embed() is used to fill the emebdding attribute (e.g., q.embed(model))
"""
d1 = (Document(uri='./data/images/fashion_images_very_small/1163.jpg')
     .load_uri_to_image_tensor()
     .set_image_tensor_normalization()
     .set_image_tensor_channel_axis(-1, 0))
# d1.summary()

model = torchvision.models.resnet50(pretrained=True)

d1.embed(model)
d1.summary()
print(d1.embedding)
print(d1.embedding[10])

res = d1.match(da1)
print(res)
res.summary()
