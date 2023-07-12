#Alice's part: 
#1. Take the public key from the previous section as Alice’s public key. 
#2. Choose any 1024-bit integer s. 
#3. Compute a new message from s using the public key: x ≡ se mod n (note: this x can look random) \
#4. On behalf of Alice, send the signature s and the message x to Bob. 
#Bob's part: 
# Bob verifies the signature using Alice’s public key (by following normal RSA signature verification process): 
#1. Using the public key, Bob gets a new digest x': x' ≡ se mod n 
#2. Bob checks whether x' == x is true 3. 
#If true, s is a valid signature for message x and Bob will accept the message/signature pair (x,s)

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import encodebytes

def square_multiply(a,x,n):
    y = 1
    for i in bin(x)[2:]:
        y = (y*y)%n

        if (i == '1'):
            y = (y*a) % n

    return y

def encrypt(x,e,n):
    return square_multiply(x,e,n)

def decrypt(x,d,n):
    return square_multiply(x,d,n)

def get_byte_from_int(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def get_int_from_byte(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

key1 = open('mykey.pem.pub','r').read()
rsakey_pub = RSA.importKey(key1)
print("public key")
print(f"rsakey.n : ,{rsakey_pub.n}")
print(f"rsakey.e : {rsakey_pub.e}")

key2 = open('mykey.pem.priv','r').read()
rsakey_priv = RSA.importKey(key2)
print("private key")
print(f"rsakey.n : {rsakey_priv.n}")
print(f"rsakey.d : {rsakey_priv.d}")

def encrypt_string(message, e, n):

    encode_msg = encodebytes(message.encode())
    encode_msg_int = get_int_from_byte(encode_msg)
    encrypted_msg = encrypt(encode_msg_int, e, n)

    return encrypted_msg

#Alice
signature = SHA256.new()
signature.update(get_byte_from_int(2))
s = signature.hexdigest()
print(f"signature: {s}")

#Bob
x = encrypt_string(s, rsakey_pub.e, rsakey_pub.n)
x_prime = encrypt_string(s, rsakey_pub.e, rsakey_pub.n)
print(f"x == x_prime is {x == x_prime}")
