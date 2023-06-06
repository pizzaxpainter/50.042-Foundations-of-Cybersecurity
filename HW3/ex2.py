import hashlib
import itertools
import string
from timeit import default_timer as timer

start = timer()
def iterate(text, dictionary):
    ls = []
    for i in text:
        ls.append(dictionary.get(i))
    return ls

ls_lower = list(string.ascii_lowercase)
ls_digits = list(string.digits)
ls_chars = ls_lower + ls_digits
iter_set = list(itertools.product(ls_chars, repeat = 20))

dict_h_pt = {}
plaintext_ls = []
hashed_ls = []
for strings in iter_set:
    plaintext = ''.join(strings)
    # plaintext_ls.append(plaintext)

    hashed = ''.join(hashlib.md5(plaintext.encode()).hexdigest())
    # hashed_ls.append(hashed)

    dict_h_pt[hashed] = plaintext

import hashlib

plaintext = "Rainbows"

result = hashlib.md5(plaintext.encode())

print(result.hexdigest())
    
