import re

def query_to_list(query):
    regex = r"([a-zA-Z]+|\(|\))"
    return re.findall(regex, query)


def query_to_postfix(query):
    prec = {}
    prec['('] = 0
    prec[')'] = 0
    prec['not'] = 3
    prec['and'] = 2
    prec['or'] = 1
    
    operator_stack = []
    postfix_list = []
    token_list = query_to_list(query)
    for token in token_list:
        if token not in prec:
            postfix_list.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            topToken = operator_stack.pop()
            while topToken != '(':
                postfix_list.append(topToken)
                topToken = operator_stack.pop()
        else:
            while len(operator_stack) > 0 and (prec[operator_stack[-1]] >= prec[token]):
                  postfix_list.append(operator_stack.pop())
            operator_stack.append(token)

    while len(operator_stack) > 0:
        postfix_list.append(operator_stack.pop())
    return postfix_list
