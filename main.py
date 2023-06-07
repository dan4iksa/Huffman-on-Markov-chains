from modules import encoder, decoder

MATRIX_PATH = 'matrix.txt'
INPUT_DIR = 'test1'
ENC_DIR_MC = 'ENC_Markov'
ENC_DIR_CLASSICAL = 'ENC_Classical'
DEC_DIR_MC = 'DEC_Markov'
DEC_DIR_CLASSICAL = 'DEC_Classical'
CHAIN_LEN = 3


def run():
    choice = input("Кодировать (0) или декодировать (1) ? ")
    while choice != '0' and choice != '1':
        print("Неверная опция!")
        choice = input("Кодировать (0) или декодировать (1) ? ")

    matrix_path = MATRIX_PATH

    if choice == '0':
        chain_len = input("Длина цепи Маркова (по умолчанию - 3) ? ")
        while chain_len and (not chain_len.isnumeric() or int(chain_len) < 2):
            print("Неверная длина!")
            chain_len = input("Длина цепи Маркова (по умолчанию - 3) ? ")

        if not chain_len:
            chain_len = CHAIN_LEN
        else:
            chain_len = int(chain_len)

        input_path = INPUT_DIR
        output_path_mc = ENC_DIR_MC
        output_path_classical = ENC_DIR_CLASSICAL

        encoder.run(input_path, output_path_mc, output_path_classical, matrix_path, chain_len)
    else:
        input_path_mc = ENC_DIR_MC
        output_path_mc = DEC_DIR_MC
        input_path_classical = ENC_DIR_CLASSICAL
        output_path_classical = DEC_DIR_CLASSICAL

        decoder.run(input_path_mc, output_path_mc, input_path_classical, output_path_classical, matrix_path)


if __name__ == '__main__':
    run()
