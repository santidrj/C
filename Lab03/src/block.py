import hashlib
from random import randint

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
        return first_verification and second_verification and third_verification

    def generate_hash(self, wrong=False):
        """
        Assigna un seed al bloc i genera el seu hash (correcte per defecte).
        """
        if wrong:
            while True:
                h = self.generate_preliminar_hash()
                if h >= 2 ** (256 - D):
                    break
        else:
            while True:
                h = self.generate_preliminar_hash()
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
