import hashlib
import itertools
import sys
import time

def reverse_hashes():

    with open('hash5.txt', 'r') as hash_file:
        hashes = [line.strip() for line in hash_file.readlines()]
        
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
    password_length = 5

    # Generate all possible combinations of characters
    combinations = itertools.product(charset, repeat=password_length)

    start_time = time.time()

    for password in combinations:
        password_str = ''.join(password)

        # Calculate the hash of the generated password
        hashed_password = hashlib.md5(password_str.encode()).hexdigest()

        if hashed_password in hashes:
            print(f"Hash found: {hashed_password} corresponds to password: {password_str}")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Total computation time: {elapsed_time} seconds")

if __name__ == '__main__':
    reverse_hashes()







 #f = open('hash5.txt', 'r')
    #hashtext = f.read()
    #f.close()


    
