from Lab03.src.rsa_public_key import rsa_public_key


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
