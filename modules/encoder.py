from modules.frequency_matrix.matrix_creator import create_matrix
from modules.utils.dir_traverse import traverse_directory
from modules.utils.buffer import Buffer


def encode_file_mc(input_path, output_path, matrix, input_buffer):
    with open(input_path, "rb") as input_file, open(output_path, "wb") as output_file:
        output_buffer = ''

        eof_pos = input_file.seek(0, 2)
        input_file.seek(0, 0)

        adj_len = 0
        output_file.write(adj_len.to_bytes(1, 'little'))

        while input_file.tell() < eof_pos:
            byte = int.from_bytes(input_file.read(1), 'little')
            input_buffer.enqueue(byte)

            chain_history = tuple(input_buffer.get_slice(input_buffer.length-1))
            chain_element = input_buffer.get_last()
            output_buffer += matrix[input_buffer.length][chain_history][chain_element]

            while len(output_buffer) >= 8:
                output_file.write(int(output_buffer[:8], 2).to_bytes(1, 'little'))
                output_buffer = output_buffer[8:]

            if input_buffer.is_full():
                input_buffer.dequeue()

        if output_buffer:
            adj_len = 8 - len(output_buffer)
            output_buffer += '0' * adj_len
            output_file.write(int(output_buffer, 2).to_bytes(1, 'little'))

    with open(output_path, "rb+") as output_file:
        output_file.write(adj_len.to_bytes(1, 'little'))


def encode_file_classical(input_path, output_path, vector):
    with open(input_path, "rb") as input_file, open(output_path, "wb") as output_file:
        buffer = ''
        eof_pos = input_file.seek(0, 2)
        input_file.seek(0, 0)

        adj_len = 0
        output_file.write(adj_len.to_bytes(1, 'little'))

        while input_file.tell() < eof_pos:
            byte = int.from_bytes(input_file.read(1), 'little')
            buffer += vector[byte]

            while len(buffer) >= 8:
                output_file.write(int(buffer[:8], 2).to_bytes(1, 'little'))
                buffer = buffer[8:]

        if buffer:
            adj_len = 8 - len(buffer)
            buffer += '0' * adj_len
            output_file.write(int(buffer, 2).to_bytes(1, 'little'))

    with open(output_path, "rb+") as output_file:
        output_file.write(adj_len.to_bytes(1, 'little'))

    return byte


def run(input_path, enc_path_mc, enc_path_classical, matrix_path, chain_len):
    matrix = create_matrix(input_path, chain_len, matrix_path)

    print("\nСжатие при помощи (больше - лучше):")

    buffer = Buffer(chain_len)
    src_size, dest_size = traverse_directory(input_path, enc_path_mc, matrix, encode_file_mc, buffer)
    print(f"\tХаффмана на Марковских цепях - {100 - dest_size / src_size * 100} %")

    vector = matrix[1][()]
    src_size, dest_size = traverse_directory(input_path, enc_path_classical, vector, encode_file_classical)
    print(f"\tХаффмана классического - {100 - dest_size / src_size * 100} %")
