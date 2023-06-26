# 50.042 FCS Lab 6 template
# Year 2021

import random
def square_multiply(a,x,n):
    y = 1
    n_b = str(bin(x)).lstrip('0b')
    for i in range(len(n_b)):
        y = (y * y) % n
        if n_b[i] == '1':
            y = (a * y) % n 
    return y

def miller_rabin(n, a):
    
    n = n-1
    k = 0
    q = n
    while q%2 == 0:
        k += 1
        q = q//2
    d = n
    # print(f'The value of d is {d}')
    # print(f'The value of r is {r}')
    for i in range(a):
        a = random.randint(2, n-2) 
        x = square_multiply(a, d, n) # (a ** d) % n
        if x == 1 or x == n-1:
            continue
        state = 0
        for j in range(k-1):
            x = square_multiply(x, 2, n) # (x ** 2) % n
            if x == n-1:
                state = 1
                break
        if state == 1:
            continue
        return 'Probably not prime'
    return 'Probably prime'

def gen_prime_nbits(n):
    odd_num = 2 * random.randint(1, 2**(n - 1) - 1) + 1
    while miller_rabin(odd_num, 2) == 'Probably not prime':
        odd_num = 2 * random.randint(1, 2**(n - 1) - 1) + 1
    return odd_num

if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
