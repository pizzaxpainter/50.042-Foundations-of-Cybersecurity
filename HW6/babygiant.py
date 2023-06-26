# 50.042 FCS Lab 6 template
# Year 2023

import math
import primes


def baby_step(alpha, beta, p, fname='baby_step.txt'):
    pass
    g = p - 1 # since All elements of the eld except 0 form a multiplicative group with the group operation ×
    # Calculate m
    m = math.floor(math.sqrt(g))
    baby_step_result = {}
    with open(fname, 'w') as fout:
        for xb in range(m):
            result = (primes.square_multiply(alpha, xb, p) * beta)%p
            # result = (pow(alpha, xb, p) * beta)%p
            fout.write(str(result) + '\n')
            baby_step_result[xb] = result
    return baby_step_result

def giant_step(alpha, p, fname):
    pass
    g = p - 1
    m = math.floor(math.sqrt(g))
    giant_step_result = {}
    with open(fname, 'w') as fout:
        for xg in range(m):
            result = primes.square_multiply(alpha, xg * m, p)
            # result = pow(alpha, xg * m, p)# alpha ** (xg * m)
            fout.write(str(result) + '\n')
            giant_step_result[xg] = result
    return giant_step_result


def baby_giant(alpha, beta, p):
    pass
    g = p - 1
    m = math.floor(math.sqrt(g))
    baby_step_result = baby_step(alpha, beta, p)
    giant_step_result = giant_step(alpha, p)
    for xb, baby_value in baby_step_result.items():
        for xg, giant_value in giant_step_result.items():
            if baby_value == giant_value:
                xb_final = xb
                xg_final = xg
    try:
        result = xg_final * m - xb_final
        return result
    except:
        return "none found"


if __name__ == "__main__":

    test 1
    My private key is:  264
    Test other private key is:  7265
    
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key :", sharedkey)
