from utils import constants, error_detection

no_of_errors = 0


# Function to introduce error
def inject_error(list_of_frames, frame_no, list_of_bit):
    list_of_frames2 = list_of_frames[:]
    frame = list_of_frames2[frame_no]
    new = list(frame)

    for i in range(len(list_of_bit)):

        if new[list_of_bit[i]] == '0':
            new[list_of_bit[i]] = '1'
        elif new[list_of_bit[i]] == '1':
            new[list_of_bit[i]] = '0'
    list_of_frames2[frame_no] = ''.join(new)

    return list_of_frames2


def generate_error_injected_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list):
    global no_of_errors

    lrc_with_error = generate_error_injected_lrc_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list)

    vrc_with_error = generate_error_injected_vrc_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list)

    checksum_with_error = generate_error_injected_chksum_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list)

    crc_with_error = generate_error_injected_crc_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list)

    return lrc_with_error, vrc_with_error, checksum_with_error, crc_with_error


# Function to write the lrc frames to file
def generate_error_injected_lrc_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list):
    lrc_val = error_detection.lrc(list_of_frames, no_of_bits)

    list_of_frames2 = list_of_frames[:]
    list_of_frames2.append(lrc_val)

    for i in range(len(error_list_frames)):
        list_of_frames2 = inject_error(list_of_frames2, error_list_frames[i], error_bit_list[i])

    lrc_list = []

    for item in list_of_frames2:
        item = '0' * (len(constants.GENERATOR_POLYNOMIAL) - 1) + item
        lrc_list.append(item)

    return lrc_list


# Function to insert error by vrc to file
def generate_error_injected_vrc_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list):
    list_of_frames2 = error_detection.vrc(list_of_frames)[:]

    # Inserting error
    for i in range(len(error_list_frames)):
        list_of_frames2 = inject_error(list_of_frames2, error_list_frames[i], error_bit_list[i])
    vrc_list = []

    for item in list_of_frames2:
        item = '0' * (len(constants.GENERATOR_POLYNOMIAL) - 2) + item
        vrc_list.append(item)

    return vrc_list


# Function to insert error toggling the checksum frames to file
def generate_error_injected_chksum_codeword(list_of_frames, no_of_bits, error_list_frames, error_bit_list):
    chksum = error_detection.checksum(list_of_frames, no_of_bits)

    list_of_frames2 = list_of_frames[:]
    list_of_frames2.append(chksum)

    # Inserting error
    for i in range(len(error_list_frames)):
        list_of_frames2 = inject_error(list_of_frames2, error_list_frames[i], error_bit_list[i])
    chksum_list = []

    for item in list_of_frames2:
        item = item = '0' * (len(constants.GENERATOR_POLYNOMIAL) - 1) + item
        chksum_list.append(item)
    return chksum_list


# Function to insert error toggling the CRC frames to file
def generate_error_injected_crc_codeword(list_of_frames, generator, error_list_frames, error_bit_list):
    list_of_frames2 = error_detection.crc(list_of_frames,
                                          constants.GENERATOR_POLYNOMIAL, constants.NO_OF_BITS_CRC)[:]

    # Inserting error
    for i in range(len(error_list_frames)):
        list_of_frames2 = inject_error(list_of_frames2, error_list_frames[i], error_bit_list[i])

    crc_list = []

    for item in list_of_frames2:
        crc_list.append(item)

    return crc_list
