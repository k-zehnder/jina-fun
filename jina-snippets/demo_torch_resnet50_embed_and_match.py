from docarray import Document, DocumentArray
import numpy as np
import torchvision

"""
*[Embedding]*
Embedding is a 1, D representation of a Document and plays an important role in machine learning. The embedding information is not the data itself, but an abstract representation of data as a list of numbers.
"""
d1 = Document(embedding=np.array([1,2,3]))
da1 = DocumentArray([d1])
da1.summary()
print("[INFO] da1 summary...")


"""
*[Fill embedding via neural network]*
Usually embedding is not set manually like this, but rather embed() is used to fill the emebdding attribute (e.g., q.embed(model))
"""
d1 = (Document(uri="./data/images/fashion_images_very_small/1163.jpg")
     .load_uri_to_image_tensor()
     .set_image_tensor_normalization()
     .set_image_tensor_channel_axis(-1, 0))

# define model
model = torchvision.models.resnet50(pretrained=True)

# embed
d1.embed(model, to_numpy=True)
print("[INFO] d1 summary (before match)...")
d1.summary()

# construct
rnd_da = DocumentArray(Document(embedding=np.random.random(len(d1.embedding))) for _ in range(10))

# match
d1.match(rnd_da, exclude_self=True, limit=3)
print("[INFO] d1 summary (after match)...")
d1.summary()

