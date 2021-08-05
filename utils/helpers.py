# from error_detection import generate_lrc, generate_vrc, generate_checksum, generate_crc
from utils import error_detection


def readfile(filename, no_of_bits):
    f = open(filename, 'r')
    data = f.read()

    list_of_frames = [data[i:i + no_of_bits] for i in range(0, len(data), no_of_bits)]
    return list_of_frames


def dataword_to_codeword(list_of_frames, generator, no_of_bits):
    lrc_codeword = error_detection.generate_lrc(list_of_frames, no_of_bits)

    vrc_codeword = error_detection.generate_vrc(list_of_frames, no_of_bits)

    checksum_codeword = error_detection.generate_checksum(list_of_frames, no_of_bits)

    crc_codeword = error_detection.generate_crc(list_of_frames, generator, no_of_bits)

    return lrc_codeword, vrc_codeword, checksum_codeword, crc_codeword


def show_options():
    print('''Please choose from below options :
        1. Error is detected by all four schemes.
        2. Error detected by checksum but not by CRC
        3. Error detected by VRC but not by CRC''')

    choice = int(input('Enter your choice : '))
    return choice
