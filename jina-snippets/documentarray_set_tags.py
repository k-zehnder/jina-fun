from docarray import Document, DocumentArray

da = DocumentArray(
    [Document(id=1), Document(id=2), Document(id=3)]
)

da[:, 'mime_type'] = ['image/jpg'] * 3
print(da[0].mime_type)
da[:, 'tags__company_name'] = ['jina'] * 3
print(da[0].tags)
da[:, 'tags'] = [{'company_name': 'jina'}] * 3

print(da[1].tags)