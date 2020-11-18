import csv
import hashlib
import os
import pickle
import random
import string
from pathlib import Path
from time import time

from block_chain import block_chain
from rsa_key import rsa_key
from transaction import transaction

output_folder = "../outputs"


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for _ in range(length)))


messages = [int(hashlib.sha256(get_random_alphanumeric_string(20).encode()).hexdigest(), 16) for _ in range(100)]


def create_comp_table():
    print("Iniciando la comparación entre la firma con TXR y sin TXR.")

    rounds = 10
    bits_modulo = [512, 1024, 2048, 4096]
    output = [["Bits modulo", "Tiempo usando TXR (s)", "Tiempo sin usar TXR (s)"]]
    for modulo in bits_modulo:
        rsa = rsa_key(bits_modulo=modulo)

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

        output.append([modulo, f'{time_to_sign:.4f}', f'{time_to_sign_slow:.4f}'])

    Path(output_folder).mkdir(exist_ok=True)
    output_path = os.path.join(output_folder, "tabla_comparativa.csv")
    with open(output_path, 'w', newline='') as file:
        csv_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerows(output)

    print(f"Se ha creado el fichero {output_path}")


def generate_block_chain(output, limit=100, num_blocks=100):
    rsa = rsa_key()
    transactions = map(lambda i: transaction(messages[i], rsa), range(100))
    blockchain = block_chain(next(transactions))

    for i in range(1, limit):
        blockchain.add_block(next(transactions))
        print(f'Block {i} created')

    if limit < num_blocks:
        for i in range(limit, num_blocks):
            blockchain.add_wrong_block(next(transactions))
            print(f'Invalid block {i} created')

    Path(output_folder).mkdir(exist_ok=True)
    output_path = os.path.join(output_folder, output)
    with open(output_path, 'wb') as output_file:
        pickle.dump(blockchain, output_file)

    valid, idx = blockchain.verify()
    if valid:
        print(f"Se ha creado el fichero {output_path}.\nEl Blockchain es válido.")
    else:
        print(f"Se ha creado el fichero {output_path}.\n"
              f"El Blockchain es válido hasta el bloque {idx} de {num_blocks}.")


def create_valid_block_chain():
    print("Iniciando la creación de una cadena válida de 100 bloques.")
    generate_block_chain("valid_block_chain.block")


def create_invalid_block_chain():
    print("Iniciando la creación de una cadena inválida de 100 bloques.")
    generate_block_chain("invalid_block_chain.block", limit=39)


class Parte1:
    @staticmethod
    def execute():
        print("Por favor introduzca una de las siguientes opciones:")
        while True:
            option = input("""\t(1) Crear una tabla comparatiba de la firma digital usando el TXR y sin usarlo
    (2) Crear un blockchain válido de 100 bloques
    (3) Crear un blockchain inválido de 100 bloques
    (4) Realizar todas las tareas anteriores y salir del programa
    (5) Salir del programa
    """)
            if '4' == option:
                create_comp_table()
                create_valid_block_chain()
                create_invalid_block_chain()
                quit()
            elif '5' == option:
                quit()
            elif '1' == option:
                create_comp_table()
            elif '2' == option:
                create_valid_block_chain()
            elif '3' == option:
                create_invalid_block_chain()
            else:
                print("La opción introducida no es válida, pruebe de nuevo.")


if __name__ == '__main__':
    Parte1.execute()
