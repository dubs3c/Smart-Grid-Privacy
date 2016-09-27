#!/usr/bin/python env

## An implementation of an additivelly homomorphic 
## ECC El-Gamal scheme, used in Privex.

from petlib.ec import EcGroup
import pytest

class Crypto():

    def __init__(self):
        self._logh = None

    def setup(self):
        """Generates the Cryptosystem Parameters."""
        G = EcGroup(nid=713)
        g = G.hash_to_point(b"g")
        h = G.hash_to_point(b"h")
        o = G.order()
        return (G, g, h, o)

    def params_gen(nid=713):
        """Generates the AHEG for an EC group nid"""
        G = EcGroup(nid)
        g = G.generator()
        o = G.order()
        return (G, g, o)

    def key_gen(self, params):
       """ Generate a private / public key pair """
       (G, g, h, o) = params
       
       priv = o.random() 
       pub = priv * g
       return (priv, pub)

    def encrypt(self, params, pub, m):
        """ Encrypt a message under the public key """
        if not -100 < m <= 100:
            raise Exception("Message value to low or high.")
        (G, g, h, o) = params
        
        priv = o.random()
        a = priv * g
        b = priv * pub + m * h
        c = (a,b)
        return c

    def enc(self, params, pub, counter):
        """Encrypts the values of a small counter"""
        assert -2**8 < counter < 2**8
        G, g, o = params

        k = o.random()
        a = k * g
        b = k * pub + counter * g
        return (a, b)

    def enc_side(self, params, pub, counter):
        """Encrypts the values of a small counter"""
        assert -2**8 < counter < 2**8
        G, g, o = params

        k = o.random()
        a = k * g
        b = k * pub + counter * g
        return (a, b, k)

    def add(self, params, pub, c1, c2):
        """ Given two ciphertexts compute the ciphertext of the 
            sum of their plaintexts.
        """
        assert self.isCiphertext(params, c1)
        assert self.isCiphertext(params, c2)
       
        #zero element encrypted
        new_enc = self.encrypt(params, pub, 0)
        #check whether this new element is in fact 
        assert self.isCiphertext(params, new_enc)
        
        #assign variables to input ciphers
        (a0,b0)=c1
        (a1,b1)=c2
        #new generated 0 element cipher used for verification
        (a2,b2)=new_enc
        #compute initial addition of ciphers c1 + c2
        c3 = (a0+a1,b0+b1)
        #assign value to the new cipher
        (a3,b3) = c3
        #add zero element cipher encrypted with public key (pub)
        c3 = (a3+a2,b3+b2)
        return c3

    def mul(self, c1, val):
        """Multiplies an encrypted counter by a public value"""
        a1, b1 = c1
        return (val*a1, val*b1)

    def randomize(self, params, pub, c1):
        """Rerandomize an encrypted counter"""
        zero = self.enc(params, pub, 0)
        return self.add(c1, zero)

    def make_table(self, params):
        """Make a decryption table"""
        _, g, o = params
        table = {}
        for i in range(-1000, 1000):
            table[i * g] = i
        return table

    def dec(self, params, table, priv, c1):
        """Decrypt an encrypted counter"""
        _, g, o = params
        a, b = c1
        plain = b + (-priv * a)
        return table[plain]

    def decrypt(params, priv, ciphertext):
        """ Decrypt a message using the private key """
        assert isCiphertext(params, ciphertext)
        (a , b) = ciphertext
        a = priv * a
        hm = b-a    

        return logh(params, hm)

    def generate_keys(self, params):
        """ Generate private and public keys """
        return self.key_gen(params)

    def groupKey(self, params, pubKeys=[]):
        """ Generate a group public key from a list of public keys """
        (G, g, h, o) = params
        #let pub be equal to the first public key in the list
        pub = pubKeys[0]
        #scan through the rest of the list and add public keys
        for key in pubKeys[1:]:
            pub = pub+key
        return pub

    def isCiphertext(self, params, ciphertext):
        """ Check a ciphertext """
        (G, g, h, o) = params
        ret = len(ciphertext) == 2
        a, b = ciphertext
        ret &= G.check_point(a)
        ret &= G.check_point(b)
        return ret

    def partialDecrypt(self, params, priv, ciphertext, final=False):
        """ Given a ciphertext and a private key, perform partial decryption. 
            If final is True, then return the plaintext. """
        assert self.isCiphertext(params, ciphertext)
        (a,b) = ciphertext
        a1 = priv*a
        b1 = b-a1
        if final:
            return self.logh(params, b1)
        else:
            return a, b1


    def logh(self, params, hm):
        """ Compute a discrete log, for small number only """
        #global _logh
        (G, g, h, o) = params

        # Initialize the map of logh
        if self._logh == None:
            self._logh = {}
            for m in range (-1000, 1000):
                self._logh[(m * h)] = m

        if hm not in self._logh:
            raise Exception("No decryption found.")

        return self._logh[hm]

    def test_AHEG():
        params = params_gen()
        (pub, priv) = key_gen(params)
        table = make_table(params)

        # Check encryption and decryption
        one = enc(params, pub, 1)
        assert dec(params, table, priv, one) == 1

        dict = {"one": enc(params, pub, 1),
                "two": enc(params, pub, 2),
                "three": enc(params, pub, 3),
                "four": enc(params, pub, 4),
                "five": enc(params, pub, 5)}


        test = ""
        for key, value in dict.iteritems():
            if test:
                #print "Test: %s\nvalue: %s" % (test, value)
                test = add(test ,value)
                #print "Result is: %s\n" % (str(test))
            else:
                test = value

        # Check addition
        tmp = add(one, one)
        two = randomize(params, pub, test)
        print(two)
        print(priv)
        assert dec(params, table, priv, two) == 15

        # # Check multiplication
        # tmp1 = mul(two, 3)
        # four = randomize(params, pub, tmp1)
        # assert dec(params, table, priv, four) == 6
