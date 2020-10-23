import sympy
from Crypto import Random
from Crypto.Util import number


class rsa_key:
    def __init__(self, bits_modulo=2048, e=2 ** 16 + 1):
        """
        Genera una clau RSA (de 2048 bits i amb exponent públic 2**16+1 per defecte).
        """
        self.publicExponent = e
        self.primeP = number.getPrime(bits_modulo, Random.get_random_bytes)
        self.primeQ = number.getPrime(bits_modulo, Random.get_random_bytes)
        self.modulus = self.primeP * self.primeQ
        self.privateExponent = sympy.mod_inverse(self.publicExponent, (self.primeP - 1) * (self.primeQ - 1))
        self.privateExponentModulusPhiP = sympy.mod_inverse(self.publicExponent, (self.primeP - 1))
        self.privateExponentModulusPhiQ = sympy.mod_inverse(self.publicExponent, (self.primeQ - 1))
        self.inverseQModulusP = sympy.mod_inverse(self.primeQ, self.primeP)

    def sign(self, message):
        """
        Retorna un enter que és la signatura de "message" feta amb la clau RSA fent servir el TXR.
        """
        d_1 = self.privateExponent % (self.primeP - 1)
        d_2 = self.privateExponent % (self.primeQ - 1)
        p_1 = sympy.mod_inverse(self.primeP, self.primeQ)
        q_1 = sympy.mod_inverse(self.primeQ, self.primeP)

        c_1 = pow(message, d_1, self.primeP)
        c_2 = pow(message, d_2, self.primeQ)

        return (c_1 * q_1 * self.primeQ + c_2 * p_1 * self.primeP) % self.modulus

    def sign_slow(self, message):
        """
        Retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR.
        """
        return pow(message, self.privateExponent, self.modulus)
