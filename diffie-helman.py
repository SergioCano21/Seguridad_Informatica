import hashlib
import random

# Numero primo de RFC3526 de 1536 bits - MODOP Group
p = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF", 16)
g = 2

# Inicio
print("\n", "*******************************")
print("\n", "Variables publicas compartidas")
print("\n", "Numero primo compartido publicamente RFC3526: ", p)
print("\n", "Numero base compartido publicamente: ", g)

# Generación de numeros secretos de Alice y Bob
secreto_alice = random.getrandbits(256) #a
secreto_bob = random.getrandbits(256) #b

secreto_eve= random.getrandbits(256) #e

print("\n", "Numero secreto Alice: ", secreto_alice)
print("\n", "Numero secreto Bob: ", secreto_bob)
print("\n", "Numero secreto Eve: ", secreto_eve)

# Alice manda mensaje a Eve -> A = g^a mod p
A = pow(g, secreto_alice, p)
print("\n", "Mensaje de Alice interceptado por Eve: ", A)

# Bob manda mensaje a Eve -> B = g^b mod p
B = pow(g, secreto_bob, p)
print("\n", "Mensaje de Bob interceptado por Eve: ", B)

E = pow(g, secreto_eve, p)
print("\n", "Mensaje de Eve a Alice y Bob: ", E)

#Alice calcula la llave secreta compartida -> s1 = E^a mod p
s1 = pow(E, secreto_alice, p)
print("\n", "Llave secreta compartida 1: ", s1)

#Eve calcula la llave secreta compartida con Alice -> s2 = A^a mod p
s2 = pow(A, secreto_eve, p)
print("\n", "Llave secreta compartida 2: ", s2)

#Bob calcula la llave secreta compartida -> s3 = E^a mod p
s3 = pow(E, secreto_bob, p)
print("\n", "Llave secreta compartida 3: ", s3)

#Eve calcula la llave secreta compartida con Bob -> s4 = B^a mod p
s4 = pow(B, secreto_eve, p)
print("\n", "Llave secreta compartida 4: ", s4)

# Comparar las llaves secretas
h1 = hashlib.sha512(int.to_bytes(s1, length=1024, byteorder='big')).hexdigest()
h2 = hashlib.sha512(int.to_bytes(s2, length=1024, byteorder='big')).hexdigest()
h3 = hashlib.sha512(int.to_bytes(s3, length=1024, byteorder='big')).hexdigest()
h4 = hashlib.sha512(int.to_bytes(s4, length=1024, byteorder='big')).hexdigest()

print("--------------------------------------")
print("Intercambio de llaves Alice - Eve")
print("\n", "h1: ", h1)
print("\n", "h2: ", h2)

if(h1 == h2):
    print("\n", "TRUE")
else:
    print("\n", "FALSE")

print("--------------------------------------")
print("Intercambio de llaves Eve - Bob")
print("\n", "h3: ", h3)
print("\n", "h4: ", h4)

if(h3 == h4):
    print("\n", "TRUE")
else:
    print("\n", "FALSE")