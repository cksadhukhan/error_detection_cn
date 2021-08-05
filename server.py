import socket
import pickle
from utils import constants
from utils import helpers, error_inject

HEADER_SIZE = constants.HEADER_SIZE

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), constants.PORT))

server_socket.listen(5)

print('Waiting for client...')

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection has been established")

    list_of_frames = helpers.readfile(constants.INPUT_FILE, constants.NO_OF_BITS)

    code_words = list(helpers.dataword_to_codeword(
        list_of_frames, constants.GENERATOR_POLYNOMIAL, constants.NO_OF_BITS))

    print('LRC code word')
    print(code_words[0])
    print('VRC code word')
    print(code_words[1])
    print('Checksum code word')
    print(code_words[2])
    print('CRC code word')
    print(code_words[3])

    choice = helpers.show_options()

    if choice == 1:
        error_injected_code_words = list(
            error_inject.generate_error_injected_codeword(list_of_frames, constants.NO_OF_BITS,
                                                          [0], [[0, 2, 3]]))
    elif choice == 2:
        error_injected_code_words = list(
            error_inject.generate_error_injected_codeword(list_of_frames, constants.NO_OF_BITS,
                                                          [0], [[0, 3, 5]]))
    elif choice == 3:
        error_injected_code_words = list(
            error_inject.generate_error_injected_codeword(list_of_frames, constants.NO_OF_BITS,
                                                          [1], [[0, 3, 5]]))
    else:
        print('Wrong choice !')

    message = pickle.dumps(error_injected_code_words)

    message = bytes(f'{len(message):<{HEADER_SIZE}}', "utf-8") + message

    client_socket.send(message)

    condition = input(
        '\nWant to select another choice ?\n  Press Y for Yes and any other key to escape : ')
    print('\n')
    if condition != 'Y' or condition != 'y':
        print('Existing ....')
        server_socket.close()
        quit()

    # server_socket.close()
