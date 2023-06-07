import os

from modules.utils import huffman_algo
from modules.utils.buffer import Buffer


def init_matrix(chain_len):
    matrix = {}

    for i in range(1, chain_len+1):
        matrix[i] = {}

    return matrix


def init_buffer_map(chain_len):
    buffer_map = {}

    for i in range(1, chain_len+1):
        buffer_map[i] = Buffer(i)

    return buffer_map


def analyze_directory(path,  matrix, buffer_map):
    for dir_path, dir_names, filenames in os.walk(path):
        for filename in filenames:
            analyze_file(os.path.join(dir_path, filename), matrix, buffer_map)


def analyze_file(path, matrix, buffer_map):
    with open(path, "rb") as file:
        eof_pos = file.seek(0, 2)
        file.seek(0, 0)

        while file.tell() < eof_pos:
            byte = int.from_bytes(file.read(1), 'little')

            for chain_len in buffer_map.keys():
                chain_buffer = buffer_map[chain_len]

                if not chain_buffer.is_full():
                    chain_buffer.enqueue(byte)

                if chain_buffer.is_full():
                    inner_matrix = matrix[chain_len]

                    chain_history = tuple(chain_buffer.get_slice(chain_len-1))
                    chain_element = chain_buffer.get_last()

                    if chain_history not in inner_matrix.keys():
                        inner_matrix[chain_history] = {}

                    if chain_element in inner_matrix[chain_history].keys():
                        inner_matrix[chain_history][chain_element] += 1
                    else:
                        inner_matrix[chain_history][chain_element] = 1

                    chain_buffer.dequeue()


def write_matrix(path, matrix):
    with open(path, 'w', encoding="utf-8") as file:
        for chain_len in matrix.keys():
            inner_matrix = matrix[chain_len]

            for chain_history in inner_matrix.keys():
                str_chain_history = [str(elem) for elem in chain_history]
                str_chain_history = ','.join(str_chain_history)

                for chain_element in inner_matrix[chain_history].keys():
                    code = inner_matrix[chain_history][chain_element]
                    file.write(f'{str_chain_history}:{chain_element}:{code}\n')


def create_matrix(input_dir_path, chain_len, matrix_path):
    matrix = init_matrix(chain_len)
    buffer_map = init_buffer_map(chain_len)

    analyze_directory(input_dir_path, matrix, buffer_map)
    huffman_algo.run(matrix)
    write_matrix(matrix_path, matrix)

    return matrix
