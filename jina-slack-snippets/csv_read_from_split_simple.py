# This file demonstrates what a DocArray looks like when you read in from a csv and how to use the tags attribute to get the columns for each row.

from docarray import Document, DocumentArray

docs = DocumentArray.from_csv("jina-slack-snippets/data/csv/anime.csv")
docs.summary()
docs[0].summary()

# this is how you select specific columns
print(docs[0].tags.get("Favorites"))
print(docs[0].tags.get("Rating"))

# One can split a DocumentArray into multiple DocumentArrays according to the tag value (stored in tags) of each Document. It returns a Python dict where Documents with the same tag value are grouped together in a new DocumentArray, with their orders preserved from the original DocumentArray.
rv = docs.split_by_tag(tag='Favorites') 
print(rv.items())

# How to use DocumentArray attribute selector
print("\n\n")
print(docs[:2, "tags"])