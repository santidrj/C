from glob import glob

from parte_1 import *

if __name__ == '__main__':
    file_list = [fn for fn in glob(os.path.join('../BlockChain-20201022', '*.block'))]
    for idx, file_name in enumerate(file_list):
        with open(file_name, 'rb') as file:
            blk = pickle.load(file)
            file.close()

        print(file_name, ' ', blk.verify())

    with open('../BlockChain-20201022/claveRSA', 'rb') as file:
        RSA = pickle.load(file)
        file.close()

    message = 12321351234123412352346234
    signature = RSA.sign(message)
    print(f'Clave RSA {rsa_public_key(RSA).verify(message, signature)}')
