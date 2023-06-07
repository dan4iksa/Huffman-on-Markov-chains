from modules.utils.BST import Node


def read_matrix_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        matrix = {}

        for line in file:
            (chain_history, chain_element, code) = line.strip().split(':')
            if chain_history:
                chain_history = map(int, chain_history.split(','))
            chain_history = tuple(chain_history)
            chain_len = len(chain_history)+1
            chain_element = int(chain_element)

            if chain_len not in matrix.keys():
                matrix[chain_len] = {}

            inner_matrix = matrix[chain_len]
            if chain_history not in inner_matrix.keys():
                inner_matrix[chain_history] = {chain_element: code}
            else:
                inner_matrix[chain_history][chain_element] = code

        return matrix
            
            
def codes_to_tree(matrix):
    max_chain_len = 0

    for chain_len in matrix.keys():
        inner_matrix = matrix[chain_len]

        if chain_len > max_chain_len:
            max_chain_len = chain_len

        for chain_history in inner_matrix.keys():
            tree = Node()

            for chain_element in inner_matrix[chain_history].keys():
                tree.insert(0, inner_matrix[chain_history][chain_element], chain_element)

            inner_matrix[chain_history] = tree

    return max_chain_len


def read_matrix(path):
    matrix = read_matrix_file(path)
    chain_len = codes_to_tree(matrix)

    return matrix, chain_len
