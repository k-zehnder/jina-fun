import numpy as np
import scipy.sparse
from docarray import DocumentArray

# build sparse matrix
sp_embed = np.random.random([3, 10])
sp_embed[sp_embed > 0.1] = 0
sp_embed = scipy.sparse.coo_matrix(sp_embed)
print(f"[INFO] sp_embed: {sp_embed}")
print(f"[INFO] sp_embed shape: {sp_embed.shape}")


da = DocumentArray.empty(3)

da[:, 'embedding'] = sp_embed
da.summary()

print(type(da[:, 'embedding']), da[:, 'embedding'].shape)
for d in da:
    print(type(d.embedding), d.embedding.shape)