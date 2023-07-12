from Crypto.PublicKey import RSA

key = open('mykey.pem.pub','r').read() 
rsakey = RSA.importKey(key)
# public key
print(rsakey.n) 
print(rsakey.e) 
# private key 
print(rsakey.n) 
print(rsakey.d)

#Define a function to encrypt a message using the following formula: m ≡ xe mod n Note: Use square and multiply algorithm to do the exponentiation!

def encrypt(m, e, n):
    return square_multiply(m, e, n)

#Decryption Use the private key mykey.pem.priv, same way as how you imported and used the public key. Define a function to decrypt a message using the following formula: m ≡ xd mod n Note: Use square and multiply algorithm to do the exponentiation!

priv_key = open('mykey.pem.priv','r').read()
rsakey = RSA.importKey(priv_key)
# public key
print(rsakey.n)
print(rsakey.e)
# private key
print(rsakey.n)
print(rsakey.d)

def decrypt(c, d, n):
    return square_multiply(c, d, n)

#Create a signature the plaintext message.txt using the private key. Rather than exponentiation of the actual message, signature using RSA is usually applied to the hash of the message. First, hash the plaintext using SHA-256 (use Crypto.Hash.SHA256), then exponentiate the digest using the following equation. s ≡ xd mod n Verify the signature using the public key. The resulting exponentiation must be the same as the hash value of the plaintext. x' ≡ se mod n

from Crypto.Hash import SHA256

def sign(m, d, n):
    h = SHA256.new(m).digest()
    return square_multiply(h, d, n)
    
def verify(m, s, e, n):
    h = SHA256.new(m).digest()
    return square_multiply(s, e, n) == h

