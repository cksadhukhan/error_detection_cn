import pickle
import socket
from utils import constants, error_detection

HEADER_SIZE = constants.HEADER_SIZE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), constants.PORT))

while True:
    full_message = b''
    new_message = True
    while True:
        message = client_socket.recv(16)
        if new_message:
            message_length = int(message[:HEADER_SIZE])
            new_message = False

        full_message += message

        if len(full_message) - HEADER_SIZE == message_length:
            print('Full message received')

            data = pickle.loads(full_message[HEADER_SIZE:])

            error_detection.check_lrc(data[0], constants.NO_OF_BITS)

            error_detection.check_vrc(data[1])

            error_detection.check_checksum(data[2], constants.NO_OF_BITS)

            error_detection.check_crc(data[3], constants.GENERATOR_POLYNOMIAL)

            new_message = True
            full_message = b''

        # client_socket.close()
