import hashlib
import os
from pydoc import plain
import random
import string
import itertools
import time

def hash(plaintext):
    result1 = hashlib.md5(plaintext.encode())
    result = result1.hexdigest()
    return result

def saltedhash(plaintext, salt):
    saltedplaintext = plaintext + salt
    salted_hash = hash(saltedplaintext)

    return salted_hash, saltedplaintext

start_time = time.time()

def iterate(content):
    salt_pt_ls = []
    saltedhash_ls = []
    for i in content:
        salt = random.SystemRandom().choice(string.ascii_lowercase)
        salt_hash_result, salt_pt = saltedhash(i, salt)
        saltedhash_ls.append(salt_hash_result)
        salt_pt_ls.append(salt_pt)
    return saltedhash_ls, salt_pt_ls

end_time = time.time()
elapsed_time = end_time - start_time
print(f"{elapsed_time} seconds")

if __name__ == "__main__":
    fin = open('ex2_hash.txt', "r")  # read mode
    fout = open('salted6.txt', "w")  # write mode
    fout2 = open('plain6.txt', "w")
    text = fin.read()
    content = text.splitlines()

    salt_hashes, salt_pt = iterate(content)
    salt_hashes = '\n'.join(salt_hashes)
    finalsalt_hashes = ''.join(salt_hashes)
    salt_pt = '\n'.join(salt_pt)
    finalsalt_pt = ''.join(salt_pt)

    fout.write(finalsalt_hashes)
    fout2.write(finalsalt_pt)
    fin.close()
    fout.close()
    fout2.close()
 