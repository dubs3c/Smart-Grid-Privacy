#!/usr/bin/env python

from src.crypto import Crypto
import base64
from petlib import pack
from petlib.ec import EcGroup
import sys

def do_sum(pub, c1, c2):
	crypto = Crypto()
	params = crypto.setup()

	pub = pack.decode(base64.b64decode(pub))
	c1 = pack.decode(base64.b64decode(c1))
	c2 = pack.decode(base64.b64decode(c2))

	ciphertext = crypto.add(params, pub, c1, c2)
	b64_enc = base64.b64encode(pack.encode(ciphertext))
	return b64_enc


def main():
	crypto = Crypto()
	params = crypto.setup()

	msgs = [13,37] #50
	print("Messages to encrypt and calculate sum: {} + {} = {}".format(msgs[0],msgs[1],msgs[0]+msgs[1]))
	(priv,pub) = crypto.key_gen(params)

	cis =  []
	for msg in msgs:
	    cis.append(crypto.encrypt(params, pub, msg))

	pub_encoded = base64.b64encode(pack.encode(pub))
	c1_encoded = base64.b64encode(pack.encode(cis[0]))
	c2_encoded = base64.b64encode(pack.encode(cis[1]))

	print("Public key encoded: {}".format(pub_encoded))
	print("Ciphertext 1 encoded: {}".format(c1_encoded))
	print("Ciphertext 2 encoded: {}".format(c2_encoded))

	# ciphertext = crypto.add(params, pub, cis[0], cis[1])
	# b64_enc = base64.b64encode(pack.encode(ciphertext))
	# print("Encrypted result of {} + {}: {}").format(msgs[0],msgs[1],ciphertext)
	# print("Encoded version: {}".format(b64_enc))
	result = raw_input("Enter encrypted sum: ")
	decoed_ciphertext = pack.decode(base64.b64decode(result))
	dec = crypto.decrypt(params, priv, decoed_ciphertext)
	assert dec == msgs[0] + msgs[1]

	print("Plaintext: {}").format(dec)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		pub = sys.argv[1]
		c1 = sys.argv[2]
		c2 = sys.argv[3]
		result = do_sum(pub, c1, c2)
		print("Result: " + str(result))
	else:
		main()