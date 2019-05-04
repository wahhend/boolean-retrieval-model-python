from Retrieval import Retrieval

model = Retrieval('corpus/vacation-corpus.txt')
query = 'not (air and terjun) or (air and terjun)'
print(model.retrieve(query))
