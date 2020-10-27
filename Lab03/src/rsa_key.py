import math

import sympy


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
        self.privateExponent = sympy.mod_inverse(self.publicExponent, (self.primeP - 1) * (self.primeQ - 1)) % \
                               (self.primeP - 1) * (self.primeQ - 1)
        self.privateExponentModulusPhiP = self.privateExponent % (self.primeP - 1)
        self.privateExponentModulusPhiQ = self.privateExponent % (self.primeQ - 1)
        self.inverseQModulusP = sympy.mod_inverse(self.primeQ, self.primeP)
        self.Q = self.inverseQModulusP * self.primeQ

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

        return (c_1 * self.Q + c_2 * (1 - self.Q)) % self.modulus

    def sign_slow(self, message):
        """
        Retorna un enter que és la signatura de "message" feta amb la clau RSA sense fer servir el TXR.
        """
        return pow(message, self.privateExponent, self.modulus)
