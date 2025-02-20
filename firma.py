import Crypto.Util.number as num
import hashlib
import Crypto.Random as rand

e = 65537
print(f"Numero 4 de Fermat 2^16+1 e: {e}\n")

pA = num.getPrime(1024, randfunc=rand.get_random_bytes)
qA = num.getPrime(1024, randfunc=rand.get_random_bytes)

nA = pA * qA
print(f"RSA Alice: {nA}\n")

# pB = num.getPrime(1024, randfunc=rand.get_random_bytes)
# qB = num.getPrime(1024, randfunc=rand.get_random_bytes)

# nB = pB * qB
# print(f"RSA Bob: {nB}\n")

phiA = (pA - 1)*(qA - 1)
dA = num.inverse(e, phiA)
print(f"Llave privada Alice: {dA}\n")

# phiB = (pB - 1)*(qB - 1)
# dB = num.inverse(e, phiB)
# print(f"Llave privada Bob: {dB}\n")

message = "Hola Mundo!"
print(f"Mensaje: {message}\n")

hM = int.from_bytes(hashlib.sha256(message.encode('utf-8')).digest(), byteorder='big')
print(f"Hash hM: {hM}\n")

sA = pow(hM, dA, nA)
print(f"Firma: {sA}\n")

hM1 = pow(sA, e, nA)
print(f"Hash hM': {hM == hM1}\n")