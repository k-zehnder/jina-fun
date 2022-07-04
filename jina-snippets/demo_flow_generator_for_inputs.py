"""
This script just demonstrates how to use a generator as Flow input, rather than inputting a big DocumentArray to Flow all at once.
"""
from jina import Document, DocumentArray, Flow
from executors.clip import CLIPEncoder
from helpers import clear_workspace, search_by_text_print_search_results


# Don't just put documents into flow like below...
da = DocumentArray.from_files("./data/images/fashion_images_very_small/*.jpg", size=50)

# put them into the Flow like this using a generator
def my_input():
    yield from DocumentArray.from_files("data/images/fashion_images_very_small/*.jpg", size=50)

clear_workspace("./workspace")

WORKSPACE_DIR = "./workspace"
index_flow = (
    Flow(
        port=12345
    ).add(
        uses=CLIPEncoder,
        name="encoder",
        uses_with={"device" : "cpu"},
    ).add(
        uses="jinahub://PQLiteIndexer/latest",
        name="indexer",
        uses_with={
            "dim": 512,
            "metric": "cosine",
            "include_metadata": True,
        },
        workspace=WORKSPACE_DIR,
        install_requirements=True,
    )
)

WORKSPACE_DIR = "./workspace"
text_search_flow = (
    Flow(
        port=12345
    ).add(
        uses=CLIPEncoder,
        name="encoder",
        uses_with={"device": "cpu"},
        workspace=WORKSPACE_DIR
    ).add(
        uses="jinahub://PQLiteIndexer/latest",
        name="indexer",
        uses_with={
            "dim": 512,
            "metric": "cosine",
            "include_metadata": True,
        },
        workspace=WORKSPACE_DIR,
        install_requirements=True,
    )
)

# use generator to input docs into Flow instead of just passing the DA
with index_flow:
    index_flow.post(on="/index", inputs=my_input, show_progress=True)

with text_search_flow:
    while True:
        query = Document(text=input("Please enter your search term: "))
        if query.text == "":
            break
        response = text_search_flow.search(inputs=query)
        search_by_text_print_search_results(response)

print("[INFO] program finished.")