from modules.frequency_matrix.matrix_reader import read_matrix
from modules.utils.dir_traverse import traverse_directory
from modules.utils.buffer import Buffer


def tree_search(tree, buffer, input_file, eof_pos):
    node, buffer = tree.find_code(buffer)
    output_byte = node.data

    while output_byte is None:
        if input_file.tell() < eof_pos:
            input_byte = str(bin(int.from_bytes(input_file.read(1), 'little')))[2:]
            buffer += '0' * (8 - len(input_byte)) + input_byte

        node, buffer = node.find_code(buffer)
        output_byte = node.data

    return output_byte, buffer


def decode_file_mc(input_path, output_path, matrix, output_buffer):
    with open(input_path, "rb") as input_file, open(output_path, "wb") as output_file:
        eof_pos = input_file.seek(0, 2)
        input_file.seek(0, 0)

        adj_len = int.from_bytes(input_file.read(1), 'little')

        input_byte = str(bin(int.from_bytes(input_file.read(1), 'little')))[2:]
        input_buffer = '0' * (8 - len(input_byte)) + input_byte

        while input_file.tell() < eof_pos:
            chain_len = output_buffer.length + 1
            chain_history = tuple(output_buffer.get_slice(output_buffer.length))

            output_byte, input_buffer = tree_search(matrix[chain_len][chain_history], input_buffer, input_file, eof_pos)
            output_file.write(output_byte.to_bytes(1, 'little'))

            if output_buffer.is_full():
                output_buffer.dequeue()

            output_buffer.enqueue(output_byte)

        input_buffer = input_buffer[:len(input_buffer) - adj_len]
        while input_buffer:
            chain_len = output_buffer.length + 1
            chain_history = tuple(output_buffer.get_slice(output_buffer.length))

            output_byte, input_buffer = tree_search(matrix[chain_len][chain_history], input_buffer, input_file, eof_pos)
            output_file.write(output_byte.to_bytes(1, 'little'))

            if output_buffer.is_full():
                output_buffer.dequeue()

            output_buffer.enqueue(output_byte)


def decode_file_classical(input_path, output_path, vector):
    with open(input_path, "rb") as input_file, open(output_path, "wb") as output_file:
        eof_pos = input_file.seek(0, 2)
        input_file.seek(0, 0)

        adj_len = int.from_bytes(input_file.read(1), 'little')

        input_byte = str(bin(int.from_bytes(input_file.read(1), 'little')))[2:]
        input_buffer = '0' * (8 - len(input_byte)) + input_byte

        while input_file.tell() < eof_pos:
            output_byte, input_buffer = tree_search(vector, input_buffer, input_file, eof_pos)
            output_file.write(output_byte.to_bytes(1, 'little'))

        input_buffer = input_buffer[:len(input_buffer) - adj_len]
        while input_buffer:
            output_byte, input_buffer = tree_search(vector, input_buffer, input_file, eof_pos)
            output_file.write(output_byte.to_bytes(1, 'little'))


def run(input_path_mc, output_path_mc, input_path_classical, output_path_classical, matrix_path):
    matrix, chain_len = read_matrix(matrix_path)

    buffer = Buffer(chain_len-1)
    traverse_directory(input_path_mc, output_path_mc, matrix, decode_file_mc, buffer)

    vector = matrix[1][()]
    traverse_directory(input_path_classical, output_path_classical, vector, decode_file_classical)
