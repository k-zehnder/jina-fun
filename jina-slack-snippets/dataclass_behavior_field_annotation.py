from docarray import dataclass, Document, DocumentArray
from docarray.typing import Image, Text, JSON
import torchvision


# re: https://docarray.jina.ai/fundamentals/dataclass/construct/?utm_source=docarray
# re: https://github.com/jina-ai/docarray/issues/268


@dataclass
class WPArticle:
    author: str # primitive type  -> tag
    column: str # primitive type -> tag
    banner: Image # docarray type -> sibling
    headline: Text # docarray type -> sibling

@dataclass
class WAPOArticle:
    title: Text # docarray type -> sibling
    image: Image # docarray type -> sibling
    metas: JSON # docarray type -> sibling


if __name__ == "__main__":
    a = WPArticle(
        banner='./data/images/fashion_images_very_small/1163.jpg',
        headline='Everything to know about flying with pets, from picking your seats to keeping your animal calm',
        author= 'Nathan Diller',
        column= 'By the Way - A Post Travel Destination'
    )
    z = Document(a)
    z.summary()
    
    # for practice: access the "banner" attribute/image chunk of the WPArticle, load uri to image tensor and, normalize, set channel axis, and then use neural network to embed image contents to vector embeddings
    model = torchvision.models.resnet50(pretrained=True)
    c = z.chunks[0].load_uri_to_image_tensor().set_image_tensor_normalization().set_image_tensor_channel_axis(-1, 0)
    c.embed(model)
    print(c)
    
    z.summary()

    a = WAPOArticle(
        title="Sonic buys smoothies.",
        image="./data/images/fashion_images_very_small/1163.jpg",
        metas={
            "key1" : "value1",
            "key2" : "value2"
        },
    )
    z = Document(a)
    z.summary()