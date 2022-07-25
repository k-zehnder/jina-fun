from jina import Flow, Document, DocumentArray


flow = (
    Flow(port=8080, protocol='http')
    .add(
        name='encoder', 
        uses='jinahub://CLIPEncoder', # jinahub+docker for dc
        install_requirements=True
    ).add(
        name='indexer',
        uses='jinahub://SimpleIndexer',
        install_requirements=True
    )
)

da = DocumentArray([Document(text="Mary had a little lamb doc 1"), Document(text="This is such cool tech bro! doc 2")])

with flow:
    r = flow.post(on="/index", inputs=da, show_progress=True)
    r[0].summary()
    
    
qx_da = DocumentArray([Document(text="I'm the query baby!")])

with flow:
    r = flow.post(on="/search", inputs=qx_da, show_progress=True)
    r[0].summary()