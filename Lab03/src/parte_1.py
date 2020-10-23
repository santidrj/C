# %%
import hashlib
import random
import string
from time import time

from Lab03.src.rsa_key import rsa_key


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))


bits_modulo = [512, 1024, 2048, 4096]
messages = [int(hashlib.sha256(get_random_alphanumeric_string(20).encode()).hexdigest(), 16) for i in range(100)]

output = "Bits modulo,Tiempo usando TXR (s),Tiempo sin usar TXR (s)\n"

for modulo in bits_modulo:
    rsa = rsa_key(bits_modulo=modulo)

    rounds = 20
    time_to_sign = 0
    time_to_sign_slow = 0
    for i in range(rounds):
        start = time()
        for message in messages:
            rsa.sign(message)
        time_to_sign += time() - start

        start = time()
        for message in messages:
            rsa.sign_slow(message)
        time_to_sign_slow += time() - start
    time_to_sign /= rounds
    time_to_sign_slow /= rounds

    print(f'''
    modulo: {modulo}
    fast: {time_to_sign}
    slow: {time_to_sign_slow}
    ''')

    output += f"{modulo},{time_to_sign},{time_to_sign_slow}\n"

with open("/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab03/outputs/tabla_comparativa.csv", 'w') as file:
    file.write(output)
