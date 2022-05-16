"""
The purpose of this example is to show how to use CLIP as a service to rerank. Remember, usually in a DocumentArray .chunks can be thought of as going "deeper" while .matches can be thought of as going "wider". 90% of the time, you use .chunks as it is the "cause". You can think of .matches more like a "consequence" of some algorithm, as it is generally not built by you manually, but rather a consequence when you apply .find() or .match().

This example addresses the 10% case mentioned above, where you have a "rerank" scenario, and want to construct matches and reorder the matches as we will see below (also https://clip-as-service.jina.ai/user-guides/client/#reranking). 

The following 2 scenarios will be demonstrated.
1. given image, rank sentences
2. given sentence, rank images

pip install clip-client
pip install clip-server
"""

from clip_client import Client
from docarray import Document


d = Document(
    uri='./data/demo_data/not_a_conference.png',
    matches=[
        Document(text=f'a photo of a {p}')
        for p in (
            'control room',
            'lecture room',
            'conference room',
            'podium indoor',
            'television studio',
        )
    ],
)

# NOTE: make sure CLIP server running in background locally for this to work by doing a >>> python -m clip_server
c = Client(server='grpc://0.0.0.0:51000')
r = c.rank([d])

print(r['@m', ['text', 'scores__clip_score__value']])
