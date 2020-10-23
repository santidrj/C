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
