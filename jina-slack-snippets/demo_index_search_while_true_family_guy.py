"""
# In this example we do the following:
# 1. Use "from_csv" to load Documents and resolve fields
# 2. Index Document
# 3. Perform Search

4-16-22 KZ
"""

from jina import Flow
from docarray import Document, DocumentArray
from helpers import print_search_results, clear_workspace


docs = DocumentArray.from_csv("./data/csv/family_guy_dialog.csv", field_resolver={"dialog": "text"})

clear_workspace("./workspace")

flow = (
    Flow(
        port=12345
    ).add(
        uses="jinahub://CLIPTextEncoder/latest",
        name="encoder",
        uses_with={"device": "cpu"},
    ).add(
        uses="jinahub://SimpleIndexer/latest",
        name="indexer",
        install_requirements=True
    )
)

with flow:
    flow.index(inputs=docs, show_progress=True)
    while True:
        query = Document(text=input("Please enter your search term: "))
        if query.text == "":
            break
        response = flow.search(inputs=query)
        print_search_results(response)

print("[INFO] program finished.")