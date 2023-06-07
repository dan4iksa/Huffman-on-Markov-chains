class Node:
    def __init__(self, frequency, chain_element=None, left=None, right=None):
        self.frequency = frequency
        self.chain_element = chain_element
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

    def get_codes(self, codes_map):
        self.dfs("", codes_map)

    def dfs(self, code, codes_map):
        if self.left is None and self.right is None:
            if not code:
                code = '1'
            codes_map[self.chain_element] = code

        if self.left is not None:
            self.left.dfs(code + '0', codes_map)
        if self.right is not None:
            self.right.dfs(code + '1', codes_map)


def get_codes(node, code, codes_map):
    if node is None:
        return

    if node.left is None and node.right is None:
        codes_map[node.chain_element] = code

    get_codes(node.left, code+'0', codes_map)
    get_codes(node.right, code+'1', codes_map)


def huffman_algo(frequency_map):
    nodes = [Node(frequency=frequency_map[chain_element], chain_element=chain_element)
             for chain_element in frequency_map.keys()]

    while len(nodes) > 1:
        nodes.sort(reverse=True)

        left_node = nodes[-1]
        right_node = nodes[-2]
        nodes = nodes[:-2]

        nodes.append(Node(frequency=left_node.frequency+right_node.frequency, left=left_node, right=right_node))

    nodes[0].get_codes(frequency_map)


def run(matrix):
    for chain_len in matrix.keys():
        inner_matrix = matrix[chain_len]

        for chain_history in inner_matrix.keys():
            huffman_algo(inner_matrix[chain_history])
