import os
import subprocess
from glob import glob
from math import gcd

import Crypto.PublicKey.RSA as rsa
from Crypto.Util import number

output_path = '../outputs'
input_path = '../RSA_RW'
student = 'santiago.del.rey'


def decrypt(rsa_key, encrypted_aes_key, encrypted_file):
    file_list = [fn for fn in glob(os.path.join(input_path, '*.pem')) if not os.path.basename(fn).startswith(student)]
    for file_name in file_list:
        with open(file_name, 'rb') as file:
            someone_rsa_key = rsa.importKey(file.read())
            file.close()
        p = gcd(rsa_key.n, someone_rsa_key.n)

        if p != 1:
            q = rsa_key.n // p
            generate_key(p, q, rsa_key.e)
            decrypt_aes_key(encrypted_aes_key)
            decrypt_file(encrypted_file)
            break


def generate_key(p, q, e):
    new_rsa_key = rsa.construct((p * q, e, number.inverse(e, (p - 1) * (q - 1)), p, q))
    private_rsa_key = new_rsa_key.export_key()

    with open(os.path.join(output_path, f'{student}_privkeyRSA_RW.pem'), 'wb') as file:
        file.write(private_rsa_key)
        file.close()


def decrypt_aes_key(key_path):
    subprocess.run(['openssl', 'rsautl', '-decrypt',
                    '-in', key_path,
                    '-out', os.path.join(output_path, f'{student}_RSA_RW_decrypted.key'),
                    '-inkey', os.path.join(output_path, f'{student}_privkeyRSA_RW.pem')])


def decrypt_file(file_path):
    subprocess.run(['openssl', 'enc', '-d', '-aes-128-cbc', '-pbkdf2',
                    '-kfile', os.path.join(output_path, f'{student}_RSA_RW_decrypted.key'),
                    '-in', file_path,
                    '-out', os.path.join(output_path, f'{student}_decrypted_file.png')])


class Parte2:
    @staticmethod
    def execute():
        with open(os.path.join(input_path, f'{student}_pubkeyRSA_RW.pem'), 'rb') as file:
            my_rsa_key = rsa.importKey(file.read())
            file.close()

        print('Decryption starts')
        decrypt(my_rsa_key, os.path.join(input_path, f'{student}_RSA_RW.enc'),
                os.path.join(input_path, f'{student}_AES_RW.enc'))
        print('End')


if __name__ == '__main__':
    Parte2.execute()
