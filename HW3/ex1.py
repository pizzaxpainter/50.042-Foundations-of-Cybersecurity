import hashlib

plaintext = "Rainbows"

result = hashlib.md5(plaintext.encode())

print(result.hexdigest())
