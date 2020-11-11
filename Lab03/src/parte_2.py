import Crypto.PublicKey.RSA as rsa

if __name__ == '__main__':
    with open('../RSA_pseudo/santiago.del.rey_pubkeyRSA_pseudo.pem',
              'rb') as file:
        KEY = rsa.importKey(file.read())

    print(f'e = {KEY.e}')
    print(f'n = {KEY.n}')
