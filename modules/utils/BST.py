class Node:
    def __init__(self):
        self.data = None
        self.left_child = None
        self.right_child = None

    def insert(self, index, code, byte):
        if index == len(code):
            self.data = byte
        else:
            if code[index] == '0':
                if not self.left_child:
                    self.left_child = Node()
                self.left_child.insert(index + 1, code, byte)
            else:
                if not self.right_child:
                    self.right_child = Node()
                self.right_child.insert(index + 1, code, byte)

    def find_code(self, byte):
        node = self
        i = 0
        while True:
            if not node.left_child and not node.right_child or i == len(byte):
                return node, byte[i:]

            node = node.left_child if byte[i] == '0' else node.right_child
            i += 1
