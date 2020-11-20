import csv
import hashlib
import math
import os
import pickle
import random
import string
from pathlib import Path
from random import randint
from time import time

import sympy

output_folder = "./outputs"


class rsa_key:
    def __init__(self, bits_modulo=2048, e=2 ** 16 + 1):
        """
        Genera una clau RSA (de 2048 bits i amb exponent públic 2**16+1 per defecte).
        """
        self.publicExponent = e
        self.primeP = sympy.randprime(pow(2, (bits_modulo - 1)), pow(2, bits_modulo))
        self.primeQ = sympy.randprime(pow(2, (bits_modulo - 1)), pow(2, bits_modulo))

        while not self.p_and_q_coprimes_with_e() and self.primeP == self.primeQ:
            self.primeP = sympy.randprime(pow(2, (bits_modulo - 1)), pow(2, bits_modulo))
            self.primeQ = sympy.randprime(pow(2, (bits_modulo - 1)), pow(2, bits_modulo))

        self.modulus = self.primeP * self.primeQ
        self.privateExponent = sympy.mod_inverse(self.publicExponent, (self.primeP - 1) * (self.primeQ - 1))
        self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1)
        self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)
        self.inverseQModulusP = sympy.mod_inverse(self.primeQ, self.primeP)

    def p_and_q_coprimes_with_e(self):
        """
        Retorna el booleà True si p y q són coprimers amb e.
        Altrament retorna el booleà False.
        """
        return math.gcd(self.publicExponent, self.primeP) == 1 and math.gcd(self.publicExponent, self.primeQ) == 1

    def sign(self, message):
        """
        Retorna un enter que és la signatura de "message" feta amb la clau RSA fent servir el TXR.
        """
        c_1 = pow(message, self.privateExponentModulusPhiP, self.primeP)
        c_2 = pow(message, self.privateExponentModulusPhiQ, self.primeQ)

        return (c_1 * self.inverseQModulusP * self.primeQ + c_2 * (
                1 - self.inverseQModulusP * self.primeQ)) % self.modulus

    def sign_slow(self, message):
        """
        Retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR.
        """
        return pow(message, self.privateExponent, self.modulus)


class rsa_public_key:
    def __init__(self, rsa_key):
        """
        Genera la clau pública RSA asociada a la clau RSA "rsa_key".
        """
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus

    def verify(self, message, signature):
        """
        Retorna el booleà True si "signature" es correspon amb una signatura de "message" feta amb la clau RSA associada a la clau pública RSA.
        En qualsevol altre cas retorna el booleà False.
        """
        return pow(signature, self.publicExponent, self.modulus) == message


class transaction:
    def __init__(self, message, rsa_key):
        """
        Genera una transacció signant "message" amb la clau "rsa_key".
        """
        self.public_key = rsa_public_key(rsa_key)
        self.message = message
        self.signature = rsa_key.sign(message)

    def verify(self):
        """
        Retorna el booleà True si "signature" es correspon amb una
        signatura de "message" feta amb la clau pública "public_key".
        En qualsevol altre cas retorna el booleà False.
        """
        return self.public_key.verify(self.message, self.signature)


D = 16


class block:
    def __init__(self):
        """
        Crea un bloc (no necesàriament vàlid).
        """
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None
        self.seed = None

    def genesis(self, transaction):
        """
        Genera el primer bloc d'una cadena amb la transacció "transaction" que es caracteritza per:
            - previous_block_hash = 0
            - ser vàlid
        """
        self.previous_block_hash = 0
        self.transaction = transaction
        self.generate_hash()
        return self

    def next_block(self, transaction):
        """
        Genera el següent bloc vàlid amb la transacció "transaction".
        """
        new_block = block()
        new_block.transaction = transaction
        new_block.previous_block_hash = self.block_hash
        new_block.generate_hash()
        return new_block

    def next_wrong_block(self, transaction):
        """
        Genera el següent bloc invàlid amb la transacció "transaction".
        """
        new_block = block()
        new_block.transaction = transaction
        new_block.previous_block_hash = self.block_hash
        new_block.generate_hash(wrong=True)
        return new_block

    def verify_block(self):
        """
        Verifica si un bloc és válid:
            - Comprova que el hash del bloc anterior cumpleix a les condicions exigides.
            - Comprova que la transacció del bloc és válida.
            - Comprova que el hash del bloc cumpleix les condicions exigides.
        Si totes les comprovacions són correctes retorna el booleà True.
        En qualsevol altre cas retorna el booleà False.
        """
        first_verification = self.previous_block_hash < 2 ** (256 - D)
        second_verification = self.transaction.verify()
        third_verification = self.block_hash < 2 ** (256 - D)
        fourth_verification = self.verify_hash()
        return first_verification and second_verification and third_verification and fourth_verification

    def verify_hash(self):
        entrada = str(self.previous_block_hash)
        entrada = entrada + str(self.transaction.public_key.publicExponent)
        entrada = entrada + str(self.transaction.public_key.modulus)
        entrada = entrada + str(self.transaction.message)
        entrada = entrada + str(self.transaction.signature)
        entrada = entrada + str(self.seed)
        h = int(hashlib.sha256(entrada.encode()).hexdigest(), 16)
        return h == self.block_hash

    def generate_hash(self, wrong=False):
        """
        Assigna un seed al bloc i genera el seu hash (correcte per defecte).
        """
        entrada = str(self.previous_block_hash)
        entrada = entrada + str(self.transaction.public_key.publicExponent)
        entrada = entrada + str(self.transaction.public_key.modulus)
        entrada = entrada + str(self.transaction.message)
        entrada = entrada + str(self.transaction.signature)

        if wrong:
            while True:
                self.seed = randint(0, 2 ** 256)
                entrada_final = entrada + str(self.seed)
                h = int(hashlib.sha256(entrada_final.encode()).hexdigest(), 16)
                if h >= 2 ** (256 - D):
                    break
        else:
            while True:
                self.seed = randint(0, 2 ** 256)
                entrada_final = entrada + str(self.seed)
                h = int(hashlib.sha256(entrada_final.encode()).hexdigest(), 16)
                if h < 2 ** (256 - D):
                    break
        self.block_hash = h

    def is_genesis(self):
        """
        Verifica si un bloc es "genesis":
            - Comprova que el hash del bloc anterior és 0.
            - Comprova que el bloc és vàlid
        Si totes les comprovacions són correctes retorna el booleà True.
        En qualsevol altre cas retorna el booleà False.
        """
        return self.previous_block_hash == 0 and self.verify_block()

    def generate_preliminar_hash(self):
        self.seed = randint(0, 2 ** 256)
        entrada = str(self.previous_block_hash)
        entrada = entrada + str(self.transaction.public_key.publicExponent)
        entrada = entrada + str(self.transaction.public_key.modulus)
        entrada = entrada + str(self.transaction.message)
        entrada = entrada + str(self.transaction.signature)
        entrada = entrada + str(self.seed)
        return int(hashlib.sha256(entrada.encode()).hexdigest(), 16)


class block_chain:
    def __init__(self, transaction):
        """
        Genera una cadena de blocs que és una llista de blocs,
        el primer bloc és un bloc "genesis" generat amb la transacció "transaction".
        """
        self.list_of_blocks = [block().genesis(transaction)]

    def add_block(self, transaction):
        """
        Afegeix a la llista de blocs un now bloc vàlid generat amb la transacció "transaction".
        """
        next_block = self.list_of_blocks[-1].next_block(transaction)
        self.list_of_blocks.append(next_block)
        return self

    def add_wrong_block(self, transaction):
        """
        Afegeix a la llista de blocs un now bloc invàlid generat amb la transacció "transaction".
        """
        next_block = self.list_of_blocks[-1].next_wrong_block(transaction)
        self.list_of_blocks.append(next_block)
        return self

    def verify(self):
        """
        Verifica si la cadena de blocs és vàlida:
            - Comprova que tots els blocs són vàlids.
            - Comprova que el primer bloc és un bloc "genesis".
            - Comprova que per cada bloc de la cadena el següent és el correcte.

        Si totes les comprovacions són correctes retorna el booleà True.
        En qualsevol altre cas retorna el booleá False i fins a quin bloc la cadena és vàlida.
        """
        if not self.list_of_blocks[0].is_genesis():
            return [False, -1]

        for idx, current_block in enumerate(self.list_of_blocks[1:], 1):
            if current_block.previous_block_hash != self.list_of_blocks[idx - 1].block_hash:
                return [False, idx - 1]

            if not current_block.verify_block():
                return [False, idx - 1]
        return [True, len(self.list_of_blocks) - 1]


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for _ in range(length)))


messages = [int(hashlib.sha256(get_random_alphanumeric_string(20).encode()).hexdigest(), 16) for _ in range(100)]


def create_comp_table():
    print("Iniciando la comparación entre la firma con TXR y sin TXR.")

    rounds = 10
    bits_modulo = [512, 1024, 2048, 4096]
    output = [["Bits módulo", "Tiempo usando TXR (s)", "Tiempo sin usar TXR (s)"]]
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
    print(f'Block 0 created')

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
        while True:
            print("\nPor favor introduzca una de las siguientes opciones:")
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
