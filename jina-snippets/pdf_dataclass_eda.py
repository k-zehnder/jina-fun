from typing import List, Dict
from docarray import Document, DocumentArray, dataclass
from docarray.typing import Image, Text, JSON
from jina import Flow, Executor, requests
import random
import numpy as np


# -------------- Construct DocumentArray
d1 = Document(uri="/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/cats_are_awesome.pdf")
d2 = Document(uri="/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/somatosensory.pdf")
docs = DocumentArray([d1, d2])

@dataclass
class PDFPage:
    images: List[Image] # docarray type --> sibling doc
    texts: List[Text] # docarray type --> sibling doc
    tags: dict # primitive python type --> tag on parent


# -------------- Build Flow
# e = Executor.from_hub("jinahub+docker://PDFSegmenter")
# resp = e.craft(docs)
f = Flow().add(
    uses='jinahub://PDFSegmenter',
)
with f:
    resp = f.post(on='/craft', inputs=docs) # returns -> documentarray with 2 documents (1 document in documentarray per pdf)
    # print(f'{[c.mime_type for c in resp[0].chunks]}')
    assert isinstance(resp, DocumentArray)
    print(resp)
    print(type(resp)) # documentarrayinmemory
    print(len(resp)) # 2
    for idx, doc in enumerate(resp):
        for chunk in doc.chunks:
            print(f">pdf #: {idx} - mime_type: {chunk.mime_type}")

resp.summary()
print("--\n\n\n")
resp[0].summary()
resp[1].summary()

# -------------- Build dataclass objects from response
final = []
for d in resp:
    assert isinstance(d, Document)
    dc = PDFPage(
            images=[], 
            texts=[], 
            tags={
                "doc0_uri" : d.uri, 
                "channel_id" : np.random.randint(1, 100)
            })
    for chunk in d.chunks:
        assert chunk.parent_id == d.id
        if chunk.mime_type == "image/*":
            dc.images.append(chunk.tensor)
        else:
            dc.texts.append(chunk.text)
    final.append(dc)
    # print(dc)
print(final)

# -------------- Inspect dataclass objects
for dc in final:
    # print(dc)
    print("\n\n")
    print(f"imgs len {len(dc.images)}")
    print(f"txt len {len(dc.texts)}")
    print(f"doc0 tags: {dc.tags}")
    # print(f"doc0 tags: {dc.}")
    print("\n\n")

"""
The output of this file is pretty useful to understand whats happening so I'm going to save it. Really cool how you can "visually inspect" a DocumentArray like this.

(venv) (base) plusplusaviator@sp4:~/Desktop/python/jina-fun$ pdf_dataclass_eda.py
╭───── 🎉 Flow is ready to serve! ─────╮
│  🔗  Protocol                GRPC    │
│  🏠     Local       0.0.0.0:59422    │
│  🔒   Private    10.0.0.227:59422    │
│  🌍    Public  24.4.218.237:59422    │
╰──────────────────────────────────────╯
<DocumentArray (length=2) at 139629448443264>
<class 'docarray.array.memory.DocumentArrayInMemory'>
2
>pdf #: 0 - mime_type: image/*
>pdf #: 0 - mime_type: image/*
>pdf #: 0 - mime_type: text/plain
>pdf #: 1 - mime_type: image/*
>pdf #: 1 - mime_type: text/plain
>pdf #: 1 - mime_type: text/plain
>pdf #: 1 - mime_type: text/plain
>pdf #: 1 - mime_type: text/plain
╭────────────────── Documents Summary ──────────────────╮
│                                                       │
│   Length                    2                         │
│   Homogenous Documents      True                      │
│   Has nested Documents in   ('chunks',)               │
│   Common Attributes         ('id', 'mime_type',       │
│                             'uri', 'chunks')          │
│   Multimodal dataclass      False                     │
│                                                       │
╰───────────────────────────────────────────────────────╯
╭───────────────── Attributes Summary ──────────────────╮
│                                                       │
│                            #Unique      Has empty     │
│   Attribute   Data type    values       value         │
│  ───────────────────────────────────────────────────  │
│   chunks      ('ChunkAr…   2            False         │
│   id          ('str',)     2            False         │
│   mime_type   ('str',)     1            False         │
│   uri         ('str',)     2            False         │
│                                                       │
╰───────────────────────────────────────────────────────╯
--



📄 Document: 030292b765907c75a184a908eac7d41f
╭───────────┬────────────────────────────────────────────
│ Attribute │ Value                                      
├───────────┼────────────────────────────────────────────
│ mime_type │ application/pdf                            
│ uri       │ /home/plusplusaviator/Desktop/python/jina-f
╰───────────┴────────────────────────────────────────────
└── 💠 Chunks
    ├── 📄 Document: 80665cf88aba95125f6de928120501bd
    │   ╭─────────────┬──────────────────────────────────
    │   │ Attribute   │ Value                            
    │   ├─────────────┼──────────────────────────────────
    │   │ parent_id   │ 030292b765907c75a184a908eac7d41f 
    │   │ granularity │ 1                                
    │   │ tensor      │ <class 'numpy.ndarray'> in shape 
    │   │             │ float32                          
    │   │ mime_type   │ image/*                          
    │   ╰─────────────┴──────────────────────────────────
    ├── 📄 Document: 33c7264d18433219ad7aaefc038288cc
    │   ╭─────────────┬──────────────────────────────────
    │   │ Attribute   │ Value                            
    │   ├─────────────┼──────────────────────────────────
    │   │ parent_id   │ 030292b765907c75a184a908eac7d41f 
    │   │ granularity │ 1                                
    │   │ tensor      │ <class 'numpy.ndarray'> in shape 
    │   │             │ float32                          
    │   │ mime_type   │ image/*                          
    │   ╰─────────────┴──────────────────────────────────
    └── 📄 Document: a28c13252ffe9ab94e20c24957621d70
        ╭──────────────────┬─────────────────────────────
        │ Attribute        │ Value                       
        ├──────────────────┼─────────────────────────────
        │ parent_id        │ 030292b765907c75a184a908eac7
        │ granularity      │ 1                           
        │ mime_type        │ text/plain                  
        │ text             │ A cat poem                  
        │                  │ I love cats, I love every ki
        │                  │ I just wanna hug all of them
        │                  │ I'm thi... (length: 188)    
        ╰──────────────────┴─────────────────────────────
📄 Document: 6e59ed0b2e762881faae06ebc8c823a5
╭───────────┬────────────────────────────────────────────
│ Attribute │ Value                                      
├───────────┼────────────────────────────────────────────
│ mime_type │ application/pdf                            
│ uri       │ /home/plusplusaviator/Desktop/python/jina-f
╰───────────┴────────────────────────────────────────────
└── 💠 Chunks
    ├── 📄 Document: a89b326a27868b0f937ab07c410e0b01
    │   ╭─────────────┬──────────────────────────────────
    │   │ Attribute   │ Value                            
    │   ├─────────────┼──────────────────────────────────
    │   │ parent_id   │ 6e59ed0b2e762881faae06ebc8c823a5 
    │   │ granularity │ 1                                
    │   │ tensor      │ <class 'numpy.ndarray'> in shape 
    │   │ mime_type   │ image/*                          
    │   ╰─────────────┴──────────────────────────────────
    ├── 📄 Document: c4642947abf0f6e8f43c461cfe3051b1
    │   ╭─────────────┬──────────────────────────────────
    │   │ Attribute   │ Value                            
    │   ├─────────────┼──────────────────────────────────
    │   │ parent_id   │ 6e59ed0b2e762881faae06ebc8c823a5 
    │   │ granularity │ 1                                
    │   │ mime_type   │ text/plain                       
    │   │ text        │ Anatomy of the Somatosensory Syst
    │   │             │ 1                                
    │   │             │ F  W                             
    │   │             │ ROM IKIBOOKS                     
    │   │             │ Our somatosensory system consists
    │   ╰─────────────┴──────────────────────────────────
    ├── 📄 Document: abccd1b7c54baf23a2979bc2f75feb08
    │   ╭──────────────────┬─────────────────────────────
    │   │ Attribute        │ Value                       
    │   ├──────────────────┼─────────────────────────────
    │   │ parent_id        │ 6e59ed0b2e762881faae06ebc8c8
    │   │ granularity      │ 1                           
    │   │ mime_type        │ text/plain                  
    │   │ text             │ From Wikibooks              
    │   │                  │ Figure 2: Mammalian muscle  
    │   │                  │ spindle showing typical posi
    │   │                  │ in a muscle (left), neuro...
    │   ╰──────────────────┴─────────────────────────────
    ├── 📄 Document: b27a9bcfc4b0004ad582e01a740a42ff
    │   ╭────────────────┬───────────────────────────────
    │   │ Attribute      │ Value                         
    │   ├────────────────┼───────────────────────────────
    │   │ parent_id      │ 6e59ed0b2e762881faae06ebc8c823
    │   │ granularity    │ 1                             
    │   │ mime_type      │ text/plain                    
    │   │ text           │ Anatomy of the Somatosensory S
    │   │                │ Rapidly adapting Slowly adapti
    │   │                │ Surface receptor / Hair recept
    │   ╰────────────────┴───────────────────────────────
    └── 📄 Document: 1a4929128f587e1a2029876b76d399ee
        ╭─────────────────────┬──────────────────────────
        │ Attribute           │ Value                    
        ├─────────────────────┼──────────────────────────
        │ parent_id           │ 6e59ed0b2e762881faae06ebc
        │ granularity         │ 1                        
        │ mime_type           │ text/plain               
        │ text                │ From Wikibooks           
        │                     │ Force                    
        │                     │ control Force (Golgi tend
        │                     │ signal Inter- Force feedb
        │                     │ neurons                  
        │                     │ Externa... (length: 1622)
        ╰─────────────────────┴──────────────────────────
[PDFPage(images=[array([[[255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.],
        ...,
        [255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.]],

       [[255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.],
        ...,
        [255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.]],

       [[255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.],
        ...,
        [255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.]],

       ...,

       [[  8.,   9.,  14.],
        [  7.,   8.,  13.],
        [  6.,   7.,  11.],
        ...,
        [193., 177., 164.],
        [195., 179., 166.],
        [196., 180., 167.]],

       [[  8.,   9.,  14.],
        [  7.,   8.,  13.],
        [  6.,   7.,  11.],
        ...,
        [194., 178., 165.],
        [197., 181., 168.],
        [197., 181., 168.]],

       [[  8.,   9.,  14.],
        [  7.,   8.,  13.],
        [  6.,   7.,  11.],
        ...,
        [196., 180., 167.],
        [198., 182., 169.],
        [199., 183., 170.]]], dtype=float32), array([[[ 12.,  27., 142.],
        [  3.,  18., 133.],
        [  0.,  15., 130.],
        ...,
        [ 10.,  28., 136.],
        [ 12.,  30., 138.],
        [ 13.,  31., 139.]],

       [[ 12.,  27., 142.],
        [  5.,  20., 135.],
        [  2.,  17., 132.],
        ...,
        [  4.,  22., 130.],
        [  3.,  21., 129.],
        [  3.,  21., 129.]],

       [[  2.,  17., 132.],
        [  2.,  17., 132.],
        [  4.,  19., 134.],
        ...,
        [  0.,  21., 130.],
        [  0.,  21., 130.],
        [  1.,  22., 131.]],

       ...,

       [[  2.,  13., 128.],
        [  2.,  13., 128.],
        [  0.,  13., 127.],
        ...,
        [  0.,  15., 130.],
        [  1.,  16., 131.],
        [  4.,  19., 134.]],

       [[  3.,  12., 129.],
        [  6.,  15., 132.],
        [  8.,  17., 134.],
        ...,
        [  3.,  16., 131.],
        [  8.,  21., 136.],
        [ 12.,  25., 140.]],

       [[  3.,  12., 129.],
        [  6.,  15., 132.],
        [  8.,  17., 134.],
        ...,
        [  3.,  16., 131.],
        [  8.,  21., 136.],
        [ 12.,  25., 140.]]], dtype=float32)], texts=["A cat poem\nI love cats, I love every kind of cat,\nI just wanna hug all of them, but I can't,\nI'm thinking about cats again\nI think about how cute they are\nAnd their whiskers and their nose"], tags={'doc0_uri': '/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/cats_are_awesome.pdf', 'channel_id': 47}), PDFPage(images=[array([[[243., 243., 243.],
        [243., 243., 243.],
        [243., 243., 243.],
        ...,
        [  8.,   8.,   8.],
        [  6.,   6.,   6.],
        [  0.,   0.,   0.]],

       [[254., 254., 254.],
        [254., 254., 254.],
        [254., 254., 254.],
        ...,
        [  0.,   0.,   0.],
        [ 10.,  10.,  10.],
        [  1.,   1.,   1.]],

       [[255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.],
        ...,
        [157., 157., 157.],
        [128., 128., 128.],
        [  0.,   0.,   0.]],

       ...,

       [[255., 255., 255.],
        [255., 255., 255.],
        [255., 255., 255.],
        ...,
        [255., 255., 255.],
        [210., 210., 210.],
        [ 17.,  17.,  17.]],

       [[202., 202., 202.],
        [202., 202., 202.],
        [202., 202., 202.],
        ...,
        [207., 207., 207.],
        [171., 171., 171.],
        [  0.,   0.,   0.]],

       [[  0.,   0.,   0.],
        [  0.,   0.,   0.],
        [  0.,   0.,   0.],
        ...,
        [  0.,   0.,   0.],
        [  0.,   0.,   0.],
        [  0.,   0.,   0.]]], dtype=float32)], texts=['Anatomy of the Somatosensory System\n1\nF  W\nROM IKIBOOKS\nOur somatosensory system consists of sensors in the skin\nThis is a sample document to\nand sensors in our muscles, tendons, and joints. The re-\nshowcase page-based formatting. It\nceptors in the skin, the so called cutaneous receptors, tell\ncontains a chapter from aWikibook\nus about temperature (thermoreceptors), pressure and sur-\ncalledSensory Systems. None of the\nface texture (mechano receptors), and pain (nociceptors).\ncontent has been changed in this\nThe receptors in muscles and joints provide information\narticle, but some content has been\nabout muscle length, muscle tension, and joint angles.\nremoved.\nCutaneous receptors\nSensory information from Meissner corpuscles and rapidly\nadapting afferents leads to adjustment of grip force when\nobjects are lifted. These afferents respond with a brief\nburst of action potentials when objects move a small dis-\ntance during the early stages of lifting. In response to\nHairy skin Glabrous skin\nFigure 1: Receptors in the hu-\nman skin: Mechanoreceptors can\nbe free receptors or encapsulated.\nPapillary Ridges\nExamples for free receptors are\nthe hair receptors at the roots of\nEpidermis\nFree nerve Septa hairs. Encapsulated receptors are\nMerkel’s\nending\nreceptor\nthe Pacinian corpuscles and the\nreceptors in the glabrous (hair-\nless) skin: Meissner corpuscles,\nMeissne r’s\nSebaceous Ruffini corpuscles and Merkel’s\ncorpuscle\nDermis\ngland\ndisks.\nRuffini’s\n corpuscle\nHair receptor\nPacinian\ncorpuscle\n1\nThe following description is based on lecture notes from Laszlo Zaborszky, from Rutgers University.\n1', 'From Wikibooks\nFigure 2: Mammalian muscle\nspindle showing typical position\nin a muscle (left), neuronal con-\nnections in spinal cord (middle)\nand expanded schematic (right).\nThe spindle is a stretch receptor\nwith its own motor supply con-\nsisting of several intrafusal mus-\ncle fibres. The sensory endings of\na primary (group Ia) afferent and\na secondary (group II) afferent\ncoil around the non-contractile\ncentral portions of the intrafusal\nfibres.\nrapidly adapting afferent activity, muscle force increases\nreflexively until the gripped object no longer moves. Such\na rapid response to a tactile stimulus is a clear indication\nof the role played by somatosensory neurons in motor ac-\ntivity.\nThe slowly adapting Merkel’s receptors are responsible\nfor form and texture perception. As would be expected for\nreceptors mediating form perception, Merkel’s receptors\nare present at high density in the digits and around the\nmouth (50/mm² of skin surface), at lower density in oth-\ner glabrous surfaces, and at very low density in hairy skin.\nThis innervations density shrinks progressively with the\npassage of time so that by the age of 50, the density in hu-\nman digits is reduced to 10/mm². Unlike rapidly adapting\naxons, slowly adapting fibers respond not only to the ini-\ntial indentation of skin, but also to sustained indentation\nup to several seconds in duration.\nActivation of the rapidly adapting Pacinian corpuscles\ngives a feeling of vibration, while the slowly adapting\nRuffini corpuscles respond to the lataral movement or\nstretching of skin.\nNociceptors\nNociceptors have free nerve endings. Functionally, skin\nnociceptors are either high-threshold mechanoreceptors\n2', 'Anatomy of the Somatosensory System\nRapidly adapting Slowly adapting\nSurface receptor / Hair receptor, Meissner’s corpuscle: De- Merkel’s receptor: Used for spa-\nsmall receptive tect an insect or a very fine vibration. tial details, e.g. a round surface\nfield Used for recognizing texture. edge or “an X” in brail.\nDeep receptor / Ruffini’s corpuscle: “A skin\nPacinian corpuscle: “A diffuse vibra-\nlarge receptive stretch”. Used for joint position\ntion” e.g. tapping with a pencil.\nfield in fingers.\nTable 1\nor polymodal receptors. Polymodal receptors respond not\nonly to intense mechanical stimuli, but also to heat and\nto noxious chemicals. These receptors respond to minute\npunctures of the epithelium, with a response magnitude\nthat depends on the degree of tissue deformation. They al-\nso respond to temperatures in the range of 40–60°C, and\nchange their response rates as a linear function of warm-\ning (in contrast with the saturating responses displayed by\nnon-noxious thermoreceptors at high temperatures).\nPain signals can be separated into individual compo-\nNotice how figure captions and\nnents, corresponding to different types of nerve fibers\nsidenotes are shown in the outside\nused for transmitting these signals. The rapidly transmit-\nmargin (on the left or right, depending\nted signal, which often has high spatial resolution, is\non whether the page is left or right).\ncalled first pain or cutaneous pricking pain. It is well local-\nAlso, figures are floated to the top/\nized and easily tolerated. The much slower, highly affec-\nbottom of the page. Wide content, like\ntive component is called second pain or burning pain; it is\nthe table and Figure 3, intrude into the\npoorly localized and poorly tolerated. The third or deep\noutside margins.\npain, arising from viscera, musculature and joints, is also\npoorly localized, can be chronic and is often associated\nwith referred pain.\nMuscle Spindles\nScattered throughout virtually every striated muscle in the\nbody are long, thin, stretch receptors called muscle spin-\ndles. They are quite simple in principle, consisting of a few\nsmall muscle fibers with a capsule surrounding the middle\nthird of the fibers. These fibers are called intrafusal fibers,\nin contrast to the ordinary extrafusal fibers. The ends of the\nintrafusal fibers are attached to extrafusal fibers, so when-\never the muscle is stretched, the intrafusal fibers are also\n3', 'From Wikibooks\nForce\ncontrol Force (Golgi tendon organ)\nsignal Inter- Force feedback\nneurons\nExternal\nforces\nMuscle\nDriving\nlength\nsignal\nTendon Muscle force\nMuscle Load\norgans\nLength (secondary muscle-spindel afferents)\nLength error (primary muscle-spindel afferents)\nLength &\nVelocity (primary muscle-spindel afferents)\nvelocity\nfeedback\nLength Spindles\ncontrol\nsignal\nGamma bias\nFigure 3: Feedback loops for proprioceptive signals for the perception and control of limb move-\nments. Arrows indicate excitatory connections; filled circles inhibitory connections.\nstretched. The central region of each intrafusal fiber has\nfew myofilaments and is non-contractile, but it does have\none or more sensory endings applied to it. When the mus-\ncle is stretched, the central part of the intrafusal fiber is\nstretched and each sensory ending fires impulses.\nMuscle spindles also receive a motor innervation. The\nFor more examples of how to use\nlarge motor neurons that supply extrafusal muscle fibers\nHTML and CSS for paper-based\nare called alpha motor neurons, while the smaller ones sup-\npublishing, seecss4.pub.\nplying the contractile portions of intrafusal fibers are\ncalled gamma neurons. Gamma motor neurons can regu-\nlate the sensitivity of the muscle spindle so that this sensi-\ntivity can be maintained at any given muscle length.\nJoint receptors\nThe joint receptors are low-threshold mechanoreceptors\nand have been divided into four groups. They signal differ-\nent characteristics of joint function (position, movements,\ndirection and speed of movements). The free receptors or\ntype 4 joint receptors are nociceptors.\n4'], tags={'doc0_uri': '/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/somatosensory.pdf', 'channel_id': 16})]



imgs len 2
txt len 1
doc0 tags: {'doc0_uri': '/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/cats_are_awesome.pdf', 'channel_id': 47}






imgs len 1
txt len 4
doc0 tags: {'doc0_uri': '/home/plusplusaviator/Desktop/python/jina-fun/jina-slack-snippets/data/pdf/somatosensory.pdf', 'channel_id': 16}
"""