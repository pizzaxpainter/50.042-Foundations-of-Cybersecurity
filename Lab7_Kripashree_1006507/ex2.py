from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import encodebytes,decodebytes

def square_multiply(a,x,n):
    y = 1
    for i in bin(x)[2:]:
        y = (y*y)%n

        if (i == '1'):
            y = (y*a) % n

    return y
    
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


def encrypt(x,e,n):
    return square_multiply(x,e,n)

def decrypt(x,d,n):
    return square_multiply(x,d,n)

def get_byte_from_int(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def get_int_from_byte(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

message = open('message.txt', 'r').read()

def encrypt_string(message, e, n):

    encode_message = encodebytes(message.encode())
    encode_message_int = get_int_from_byte(encode_message)
    encrypted_message = encrypt(encode_message_int, e, n)

    return encrypted_message


def decrypt_string(encoded_int, d, n):

    decrypted_int = decrypt(encoded_int, d, n)
    output = decodebytes(get_byte_from_int(decrypted_int))

    return output.decode()


#encoded_message = encrypt_string(message, rsakey_pub.e,rsakey_pub.n)
#decrypted_message = decrypt_string(encoded_message,rsakey_priv.d, rsakey_priv.n)

print(f"\nmessage: {message}")
# print(f"message_encoded_int_encrypted: {message_encoded_int_encrypted}\n")
# print(f"message_encoded_decrypted: {message_encoded_decrypted}\n")

# sign and verify
h = SHA256.new()
h.update(b'Hello')
print(f"hash: {h.hexdigest()}")

sha256_signed = encrypt_string(h.hexdigest(), rsakey_priv.d, rsakey_priv.n)
sha256_verify = decrypt_string(sha256_signed, rsakey_pub.e, rsakey_pub.n)

print(f"verified hash: {sha256_verify}")
print("verifiying : h.hexdigest() == sha256_verify")
print("verification result is ",h.hexdigest() == sha256_verify)