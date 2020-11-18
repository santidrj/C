import os
import pickle
from glob import glob

if __name__ == '__main__':
    file_list = [fn for fn in glob(os.path.join('../BlockChain-20201022', '*.block'))]
    for idx, file_name in enumerate(file_list):
        with open(file_name, 'rb') as file:
            blk = pickle.load(file)
            file.close()

        print(file_name, ' ', blk.verify())
