#Encrypt an integer (e.g. 100) using the public key from previous part, e.g. y 2. 
#Choose a multiplier s equal to 2 and calculate: ys ≡ se mod n 3. 
#Multiply the two numbers: m ≡ y × ys mod n 4. 
#Decrypt using the private key from the previous part.
from Crypto.PublicKey import RSA

def square_multiply(a,x,n):
    y = 1
    for i in bin(x)[2:]:
        y = (y*y)%n

        if (i == '1'):
            y = (y*a) % n

    return y

# public key
def encrypt(x,e,n):
    return square_multiply(x,e,n)

def decrypt(x,d,n):
    return square_multiply(x,d,n)


# public key
key1 = open('mykey.pem.pub','r').read()
rsakey_pub = RSA.importKey(key1)
print("public key")
print(f"rsakey.n : ,{rsakey_pub.n}")
print(f"rsakey.e : {rsakey_pub.e}")

# private key
key2 = open('mykey.pem.priv','r').read()
rsakey_priv = RSA.importKey(key2)
print("private key")
print(f"rsakey.n : {rsakey_priv.n}")
print(f"rsakey.d : {rsakey_priv.d}")

print("encrypting:  100")
y = encrypt(100, rsakey_pub.e, rsakey_pub.n)
y_s = encrypt(2, rsakey_pub.e, rsakey_pub.n)
msg = y * y_s

msg_decrypted = decrypt(m, rsakey_priv.d, rsakey_priv.n)
print(f"result:\n{y}\n")
print(f"modified to:\n{msg}\n")
print(f"decrypted:  {msg_decrypted}")



