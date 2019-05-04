import numpy as np
import re
from Document import Document
import QueryProcessing as qproc


class Retrieval:
    def __init__(self, corpus):
        self.read_file_and_make_docs(corpus)
        self.create_incidence_matrix()

    def read_file_and_make_docs(self, filename):
        corpus = open(filename, encoding='utf-8')
        corpus = corpus.read()

        regex = r"<TITLE>([^<]+)<.+>\s+<.+>([^<]+)"
        matches = re.finditer(regex, corpus)

        self.docs = [Document(match.group(1), match.group(2)) for match in matches]


    def get_all_terms(self):
        stopwords = open('stopword/stopword-list.txt', encoding='utf-8')
        stopwords = stopwords.read()
        
        regex = r"(.+)\n"
        matches = re.finditer(regex, stopwords)

        stopwords = [match.group(1) for match in matches]
        print(len(stopwords))
        
        word_all_documents = []
        
        for doc in self.docs:
            word_all_documents += doc.get_words()

        word_all_documents = np.array(word_all_documents)
        terms = np.unique(word_all_documents)
        print(len(terms))
        return np.setdiff1d(terms, stopwords)


    def create_incidence_matrix(self):
        terms = self.get_all_terms()
        inc_mat = [[i for i, doc in enumerate(self.docs) if term in doc.words] for term in terms]

        self.inc_mat = dict(zip(terms, inc_mat))


    def retrieve_term(self, term):
        return self.inc_mat[term]


    def postfix_eval(self, postfix_expr):
        print(postfix_expr)
        operand_stack = []
        operator = ['and', 'or', 'not']
        for token in postfix_expr:
            if token not in operator:
                operand_stack.append(self.retrieve_term(token))
            elif token == 'not':
                operand_stack.append(negate(operand_stack.pop()))
            else:
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = self.operate(token, operand1, operand2)
                operand_stack.append(result)
        
        return operand_stack.pop()


    def operate(self, op, res1, res2):
        if op == "and":
            return np.intersect1d(res1, res2)
        else:
            return np.unique(np.concatenate((res1, res2)))


    def negate(self, docs, res):
        idx = [i for i, d in enumerate(docs)]
        return np.setdiff1d(idx, res)


    def retrieve(self, query):
        return self.postfix_eval(qproc.query_to_postfix(query))
