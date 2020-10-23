from Lab03.src.block import block


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
            return False, 0

        for idx, current_block in enumerate(self.list_of_blocks[1:], 1):
            if not current_block.verify_block():
                return False, idx
        return True
