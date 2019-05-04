from Retrieval import Retrieval

model = Retrieval('corpus/my-corpus.txt')
query = 'warga or pemerintah'
print(model.retrieve(query))
