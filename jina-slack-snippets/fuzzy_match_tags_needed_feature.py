from docarray import dataclass, Document, DocumentArray
import numpy as np


# Q6: https://docs.google.com/document/d/1BpVwRSGwuUuC57UWCzIxKXOSs2VhrDg-MYNV3-LSxC8/edit

# User question: 
# [user] I am currently using .split_by_tag to search by tags. Is there a way to search tags semantically? Or at least a way to change the behaviour of that method to do fuzzy matching of tags?
# [user] I create documents that contain other documents, each one of them being a sentence of the higher level document
# [H] could you elaborate on that,
# for example, my tags look like the following
# for example, by fuzzy matching i mean, my input is ... and i want to retrieve ...

da = DocumentArray()
da.append(Document(text="Hello. This is a sentence one. This is another sentence two.", person="person1"))
# da.summary()

da[0].chunks.append(Document(text=da[0].text.split(".")[-3], person="Apple Inc."))
da[0].chunks.append(Document(text=da[0].text.split(".")[-2], person="David"))
da.summary()
da[...].summary()

print(da[0].text)
print(da[0].chunks[0].text)

print(da["@c", "text"])

# [user] I know I can retrieve text semantically, but is there a possibility to search tags semantically? If not semantically, fuzzy matching of strings (strings are not equal but similar, like Levenshtein distance)

# [D]
# This does not exist yet but we will consider your comment. Elastic backend allows you to find by string and substring but no fuzzy matching exist at the moment. If you index the tag organization and one doc has 'apple inc' and another doc has 'apple' it will find both docs using in find 'apple'. But if you type 'aple' none of them will be retrieved (edited) 

r = da.find({"tags__person" : {"$eq" : "person1"}})
print(r)
r.summary()




