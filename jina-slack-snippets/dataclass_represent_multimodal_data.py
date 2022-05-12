from docarray import dataclass, Document
from docarray.typing import Image, Text, JSON
import numpy as np


@dataclass
class Person:
    name: str # primitive type  -> tag
    age: int # primitive type  -> tag
    avatar: Image # docarray type -> sibling
    

if __name__ == '__main__':
    p1 = Person(
        name="kevin",
        age=30,
        avatar="https://avatars.githubusercontent.com/u/51463990?v=4"
    )
    print(p1)
    print(p1.name)
    
    d = Document(p1)
    d.summary()


# NOTE: REMINDER! doc.chunks ...chunks are sub-documents!
"""
Person(name='kevin', age=30, avatar='https://avatars.githubusercontent.com/u/51463990?v=4')
kevin

📄 Document: ff2d284e31457e090cb7d40652c5ce2c
╭─────────────────────┬────────────────────────────────────────────────────────╮
│ Attribute           │ Value                                                  │
├─────────────────────┼────────────────────────────────────────────────────────┤
│ tags                │ {'name': 'kevin', 'age': 30}                           │
╰─────────────────────┴────────────────────────────────────────────────────────╯
└── 💠 Chunks
    └── 📄 Document: a01a96f19968e703101e802c9fb780b9
        ╭──────────────┬───────────────────────────────────────────────────────────────╮
        │ Attribute    │ Value                                                         │
        ├──────────────┼───────────────────────────────────────────────────────────────┤
        │ parent_id    │ ff2d284e31457e090cb7d40652c5ce2c                              │
        │ granularity  │ 1                                                             │
        │ tensor       │ <class 'numpy.ndarray'> in shape (460, 460, 3), dtype: uint8  │
        │ uri          │ https://avatars.githubusercontent.com/u/51463990?v=4          │
        │ modality     │ image                                                         │

"""