#Encrypt mydata.txt using your public key 
#2. Decrypt mydata.txt using your private key. 
#3. Sign the text mydata.txt using your private key. Verify to check that it the signature is valid. 
#Write a script ex5.py to do the following:
#1. Redo the protocol attack with the new RSA. 
#2. Report if the attack works#

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256

def generate_RSA():
    private = RSA.generate(1024)
    public = private.publickey()
    with open('priv.pem', 'wb') as f1:
        f1.write(private.exportKey('PEM'))
    with open('pub.pem', 'wb') as f2:
        f2.write(public.exportKey('PEM'))

generate_RSA()

def encrypt_RSA(public_key_file, message):
    key = open(public_key_file, 'r')
    rsakey_pub = RSA.importKey(key.read())
    cipher = PKCS1_OAEP.new(rsakey_pub)
    ciphertext = cipher.encrypt(bytes(message, 'utf8'))

    return ciphertext

def decrypt_RSA(private_key_file, ciphertext):
    key = open(private_key_file, 'r')
    rsakey_priv = RSA.importKey(key.read())
    cipher = PKCS1_OAEP.new(rsakey_priv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()


data = open('mydata.txt','r').read()
print(f"data: {data}\n")
cipher = encrypt_RSA('pub.pem', data)
print(f"cipher: {cipher}\n")
plaintext = decrypt_RSA('priv.pem', cipher)
print(f"data decrypted: {plaintext}\n")


def sign_data(private_key_file, data):
    key = RSA.importKey(open(private_key_file).read())
    h = SHA256.new()
    h.update(data)
    sig = PKCS1_PSS.new(key)
    signature = sig.sign(h)

    return signature


def verify_sign(public_key_file, sign, data):
    key = RSA.importKey(open(public_key_file).read())
    h = SHA256.new()
    h.update(data)
    verifier = PKCS1_PSS.new(key)
    return verifier.verify(h, sign)

print("encrypted with public key (cipher) : ", cipher)

try:
    data_decrypted = decrypt_RSA('priv.pem', data)
    print(f"decrypted:\n{data_decrypted}\n")
except ValueError:
    print("unable to decrypt, attack FAILED")