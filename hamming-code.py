import random
from math import log2, ceil

# https://en.wikipedia.org/wiki/Hamming_code

s = input()

# generate alphabet (0x61 - a, 0x7a - z)
alphabet = {chr(i): bin(i - 0x61)[2:].zfill(5) for i in range(0x61, 0x7b)}

data = ''.join(alphabet[item] for item in s)

# generate control bits indexes
idx = [2 ** i - 1 for i in range(ceil(log2(len(data))) + 1)]
if idx[-1] >= len(data):
    del idx[-1]

# set control bits with initial value of 0
for item in idx:
    data = data[0:item] + '0' + data[item:]

# calculate control bits
control_bits = {item: '0' for item in idx}
for item in idx:
    n = item + 1
    bits = ''.join(e for i in range(item, len(data), n + n) for e in data[i:i + n])
    r = bits.count('1') % 2

    control_bits[item] = str(r)

# set control bits with their values
for key, val in control_bits.items():
    data = data[0:key] + val + data[key + 1:]

# corrupt data manually
data_corrupted = data
corrupted_idx = random.randint(0, len(data) - 1)
data_corrupted = data_corrupted[0:corrupted_idx] + (
    '0' if data_corrupted[corrupted_idx] == '1' else '1') + data_corrupted[corrupted_idx + 1:]

# set control bits with initial value of 0
for item in idx:
    data_corrupted = data_corrupted[0:item] + '0' + data_corrupted[item + 1:]

# calculate control bits
control_bits_saved = {item: data[item] for item in idx}
control_bits = {item: '0' for item in idx}
for item in idx:
    n = item + 1
    bits = ''.join(e for i in range(item, len(data_corrupted), n + n) for e in data_corrupted[i:i + n])
    r = bits.count('1') % 2

    control_bits[item] = str(r)


def decode(dirty_data: str):
    global alphabet

    # remote control bits
    for item in idx:
        dirty_data = dirty_data[0:item] + '-' + dirty_data[item + 1:]

    dirty_data = dirty_data.replace('-', '')

    alphabet = {v: k for k, v in alphabet.items()}

    # convert bits to string
    res = ''
    current = ''
    for item in dirty_data:
        current += item
        if current in alphabet:
            res += alphabet[current]
            current = ''

    return res


if control_bits_saved != control_bits:
    # find error bit index
    error_idx = 0
    for item in control_bits.keys():
        if control_bits[item] != control_bits_saved[item]:
            error_idx += item + 1

    error_idx -= 1

    data_corrupted = data_corrupted[0:error_idx] + ('0' if data_corrupted[error_idx] == '1' else '1') + data_corrupted[
                                                                                                        error_idx + 1:]

res = decode(data_corrupted)

print(res)
