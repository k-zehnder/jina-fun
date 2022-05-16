from docarray import dataclass, Document, DocumentArray
from docarray.typing import Image, Text, JSON


@dataclass
class WAPOArticle:
    title: Text
    image: Image
    metas: JSON


if __name__ == "__main__":
    a = WAPOArticle(
        title="Sonic buys smoothies.",
        image="./data/demo_data/not_a_conference.png",
        metas={
            "key1" : "value1",
            "key2" : "value2"
        },
    )

    b = WAPOArticle(
        title="Cool show!",
        image="./data/demo_data/not_a_conference.png",
        metas = {}
    )

    d1 = Document(a)
    # d1.summary()

    d2 = Document(b)
    # d2.summary()

    # d_array = Document(d1, d2)
    d_array = DocumentArray([d1, d2])
    print(d_array)
    d_array.summary()
    # d_array[...].summary() # flatten with elipsis

    res = d_array.find({'parent_id': {'$eq': d1.parent_id}}) # returns DocumentArray
    print(res)

    # print(d_array[0]) # index a DocumentArray by offset, ID
    print(d_array[0].chunks[2].tags.get("key1"))
    print(d_array["@c"][2].summary())