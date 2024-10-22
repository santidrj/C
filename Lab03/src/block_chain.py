from block import block


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
