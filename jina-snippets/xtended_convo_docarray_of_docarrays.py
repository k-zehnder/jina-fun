from docarray import Document, DocumentArray
import numpy as np


d1 = Document(chunks=[Document(embedding=np.array([1, 2, 3])), Document(embedding=np.array([1, 2, 3]))])
d2 = Document(chunks=[Document(embedding=np.array([1, 2, 3])), Document(embedding=np.array([1, 2, 3]))])
da = DocumentArray([d1, d2])
da.summary()

# d1.summary()
d1.chunks.match(d2.chunks)
# d1.summary()



""""
Extended convo below. Very helpful!
"""
# Is it possible to have a DocArray of DocArrays?

# Joan Fontanals (Jina AI)  3 days ago
# Document is a recursive structure, so by using chunks u can definitely have it

# Carlos Mauro Osorio Osorio  3 days ago
# oh ok. Hard to realize that by myself. I was planning to recurse on DocumentArray which would be wrong

# Carlos Mauro Osorio Osorio  3 days ago
# thanks for your help

# Carlos Mauro Osorio Osorio  3 days ago
# d1 and d2 can be matched too?

# Carlos Mauro Osorio Osorio  3 days ago
# like d1.match(d2) ?

# Carlos Mauro Osorio Osorio  3 days ago
# because i do that with documentarrays but not sure if with documents can be done

# Joan Fontanals (Jina AI)  3 days ago
# no, you need to wrap them in a DocumentArray

# Carlos Mauro Osorio Osorio  3 days ago
# :disappointed: I imagined that

# Carlos Mauro Osorio Osorio  3 days ago
# i wanna match each chunk of d1 with each chunk of d2... what is the best for wrapping d1 and d2 as documentarrays so they would be matchable? chunks convert into documents automatically?
# white_check_mark
# eyes
# raised_hands

# Joan Fontanals (Jina AI)  3 days ago
# u can do d1.chunks.match(d2.chunks)

# Carlos Mauro Osorio Osorio  3 days ago
# ooooh excellent

# Joan Fontanals (Jina AI)  3 days ago
# and then u would find the matches under each chunk matches.

# Carlos Mauro Osorio Osorio  3 days ago
# excellent! thank you for your kind answer :slightly_smiling_face:

# Joan Fontanals (Jina AI)  3 days ago
# you will slowly discover the power of DA

# Carlos Mauro Osorio Osorio  3 days ago
# that's right

# Carlos Mauro Osorio Osorio  3 days ago
# is there a way to get matches in the same order as da2 when doing da1.match(da2) ?

# Joan Fontanals (Jina AI)  3 days ago
# what do u mean?

# Carlos Mauro Osorio Osorio  3 days ago
# it is automatically organizing by score and want to avoid that

# Joan Fontanals (Jina AI)  3 days ago
# Not automatically, but u should be able to do it by using Python functionality. At the end DA behave as  Lists

# Carlos Mauro Osorio Osorio  3 days ago
# yes

# Carlos Mauro Osorio Osorio  3 days ago
# i was thinking maybe match had a parameter like .match(sort='score') or something like that, but it doesn't :disappointed:

# Carlos Mauro Osorio Osorio  3 days ago
# or sort='ascending'

# Carlos Mauro Osorio Osorio  3 days ago
# much better

# Joan Fontanals (Jina AI)  3 days ago
# u can open a ticket in the repo to consider

# Carlos Mauro Osorio Osorio  3 days ago
# good idea

# Carlos Mauro Osorio Osorio  3 days ago
# in the meanwhile, i will sort the list pythonically

# Han (Jina AI)  3 days ago
# in the meanwhile, i will sort the list pythonically
# this is the recommended way

# Han (Jina AI)  3 days ago
# take .find() for example, it returns a DA, which you can always do sort(da, key=lamnda d: d.score['cosine'].value, descending=False) , note that sort is the Python built-in function

# Carlos Mauro Osorio Osorio  3 days ago
# yes, I've been trying that
# :clap:
# 1

