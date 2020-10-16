import subprocess
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

ascii_chars = ''.join([chr(i) for i in range(256)])


def gen_key():
    for first_chr in ascii_chars:
        for second_chr in ascii_chars:
            yield f"{first_chr * 8}{second_chr * 8}"


def read_file(path):
    with open(path, 'rb') as file:
        return file.read()


def write_file(path, data):
    with open(path, 'wb') as file:
        file.write(data)


if __name__ == "__main__":
    key_generator = gen_key()
    i = 0
    iteration = 0

    while True:
        print(iteration)
        iteration += 1
        try:
            H = sha256(next(key_generator).encode()).digest()
            k = H[:16]
            iv = H[16:]

            enc = read_file(
                "/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/2020_09_25_10_31_48_santiago.del.rey"
                ".puerta_trasera.enc")
            aes = AES.new(k, AES.MODE_CBC, iv)
            dec = unpad(aes.decrypt(enc), AES.block_size)
        except ValueError:
            pass
        except StopIteration:
            break
        else:
            write_file("/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/initial_decript", dec)

            file_type = subprocess.run(
                ['file', '-b', '/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/initial_decript'],
                stdout=subprocess.PIPE)

            if 'data' not in file_type.stdout.decode('utf-8') and 'DOS' not in file_type.stdout.decode('utf-8') \
                    and 'PGP' not in file_type.stdout.decode('utf-8') \
                    and 'font file' not in file_type.stdout.decode('utf-8'):
                write_file(f"/home/santiago/MEGAsync/7o_Cuatrimestre/C/Lab/Lab02/outputs/decripted{i}", dec)
                i += 1
