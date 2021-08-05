from utils import constants


def generate_lrc(list_of_frames, no_of_bits):
    lrc_val = lrc(list_of_frames, no_of_bits)

    list_of_frames2 = list_of_frames[:]
    list_of_frames2.append(lrc_val)
    return list_of_frames2


def generate_vrc(list_of_frames, no_of_bits):
    list_of_frames2 = vrc(list_of_frames)[:]

    return list_of_frames2


def generate_checksum(list_of_frames, no_of_bits):
    checksum_val = checksum(list_of_frames, no_of_bits)

    list_of_frames2 = list_of_frames[:]  # added all frames
    list_of_frames2.append(checksum_val)  # put checksum at the end of last frame

    return list_of_frames2


# Function to write the crc frames to the file
def generate_crc(list_of_frames, generator, no_of_bits):
    list_of_frames2 = crc(list_of_frames, generator,
                          no_of_bits)[:]

    return list_of_frames2


# To generate the LRC code
def lrc(list_of_frames, no_of_bits):
    lsum = 0

    for frame in list_of_frames:
        lsum = lsum ^ int(frame, 2)
    lsum = bin(lsum)[2:]

    while len(lsum) < no_of_bits:
        lsum = '0' + lsum
    return lsum


# To generate the VRC code
def vrc(list_of_frames):
    codewords = []
    for i in range(len(list_of_frames)):

        dataword = list_of_frames[i]
        if dataword.count('1') % 2 == 0:
            dataword += '0'
        else:
            dataword += '1'
        codewords.append(dataword)

    return codewords


# To find checksum of a number
def checksum(list_of_frames, no_of_bits):
    chksum = 0

    for frame in list_of_frames:
        chksum = chksum + int(frame, 2)

    csum = bin(chksum)
    csum = csum[2:]

    while len(csum) > no_of_bits:
        first = csum[0:len(csum) - no_of_bits]
        second = csum[len(csum) - no_of_bits:]
        s = int(first, 2) + int(second, 2)
        csum = bin(s)
        csum = csum[2:]

    while len(csum) < no_of_bits:
        csum = '0' + csum
    chksum = ''
    for i in range(len(csum)):
        if csum[i] == '0':
            chksum += '1'
        else:
            chksum += '0'
    return chksum


# XOR operation
def xor(a, b):
    a = int(a, 2)
    b = int(b, 2)
    a = a ^ b
    a = bin(a)[2:]
    return a


def modulo2div(dataword, generator):
    l_xor = len(generator)
    tmp = dataword[0:l_xor]

    while l_xor < len(dataword):
        if tmp[0] == '1':

            tmp = xor(generator, tmp) + dataword[l_xor]
        else:

            tmp = xor('0' * len(generator), tmp) + dataword[l_xor]
        tmp = '0' * (len(generator) - len(tmp)) + tmp

        l_xor += 1

    if tmp[0] == '1':
        tmp = xor(generator, tmp)
    else:
        tmp = xor('0' * len(generator), tmp)
    tmp = '0' * (len(generator) - len(tmp) - 1) + tmp
    checkword = tmp
    return checkword


# Return the codeword for crc
def crc(list_of_frames, generator, no_of_bits):
    codewords = []
    for i in range(len(list_of_frames)):
        dataword = list_of_frames[i]

        append_dataword = dataword + '0' * (len(generator) - 1)

        checkword = modulo2div(append_dataword, generator)
        codeword = dataword + checkword
        codewords.append(codeword)

    return codewords


# Check for error by lrc
def check_lrc(list_of_frames, no_of_bits):
    # Removing padding
    list_of_frames = [list_of_frames[i][len(constants.GENERATOR_POLYNOMIAL) - 1:]
                      for i in range(len(list_of_frames))]

    lrc_val = lrc(list_of_frames, no_of_bits)
    # if the appended value is zero
    if int(lrc_val, 2) == 0:
        print('No error in data detected by LRC')
        print('Dataword frames are')
        print(list_of_frames[0:-1])

    else:
        print('Error detected by LRC')


# Check for error by vrc


def check_vrc(list_of_frames):
    # Removing padding
    list_of_frames = [list_of_frames[i][len(constants.GENERATOR_POLYNOMIAL) - 2:]
                      for i in range(len(list_of_frames))]
    flag = True

    for i in range(len(list_of_frames)):
        if list_of_frames[i].count('1') % 2 != 0:
            print('Error detected in frame ' + str(i + 1) + ' by VRC')
            flag = False

    if flag:
        # No error extract dataword
        print("No error detected in data by VRC")
        list_of_frames = [list_of_frames[i][0:-1]
                          for i in range(len(list_of_frames))]
        print('Dataword frames are')
        print(list_of_frames)


# Check for error by checksum
def check_checksum(list_of_frames, no_of_bits):
    # Removing padding
    list_of_frames = [list_of_frames[i][len(constants.GENERATOR_POLYNOMIAL) - 1:]
                      for i in range(len(list_of_frames))]

    chksum = checksum(list_of_frames, no_of_bits)

    if int(chksum, 2) == 0:
        # In case of no error detected then dataword is printed
        print('No error in data is detected by checksum')
        print('Dataword frames are')
        print(list_of_frames[0:-1])

    else:
        print('Error detected by checksum')


# Check for error by crc
def check_crc(list_of_frames, generator):
    flag = True
    for i in range(len(list_of_frames)):
        if int(modulo2div(list_of_frames[i], constants.GENERATOR_POLYNOMIAL), 2) != 0:
            print('Error detected in frame ' + str(i + 1) + ' by CRC')
            flag = False

    if flag:
        list_of_frames = [list_of_frames[i][0:constants.NO_OF_BITS_CRC]
                          for i in range(len(list_of_frames))]
        print('Dataword frames are')
        print(list_of_frames)
        print("No error detected in data by CRC")
