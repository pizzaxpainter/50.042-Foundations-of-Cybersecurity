# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021

from copy import deepcopy
class Polynomial2:

    def __init__(self,coeffs):
        self.coeffs = coeffs

    def add(self,p2):
        output = []
        polynomial_1, polynomial_2 = deepcopy(self.coeffs), deepcopy(p2.coeffs)
        polynomial_1_len, polynomial_2_len = len(polynomial_1),len(polynomial_2)

        longer = max(polynomial_2_len,polynomial_1_len)

        for i in range(longer):
            try: output.append(polynomial_1[i] ^ polynomial_2[i])
            except IndexError:
                if polynomial_1_len < polynomial_2_len: 
                    output.append(polynomial_2[i] ^ 0)

                else : output.append(polynomial_1[i] ^ 0)

        #print(output)
        return Polynomial2(output)

    def sub(self,p2):
        return self.add(p2)

    def shift_right(self):
        return Polynomial2([0] + self.coeffs)

    def modp(self, modp):

        if len(self.coeffs) >= len(modp.coeffs):
            """
            MSB does not coincide, XOR self and modp without MSB
            --> add 
            """
            return Polynomial2(self.coeffs[:-1]).add(Polynomial2(modp.coeffs[:-1]))
        else:
            return self

    def mul(self,p2,modp=None):
        output = []

        output.append(p2)

        for i in range(1, len(self.coeffs)):
            MSB_output = output[-1]
            try:
                if MSB_output.coeffs.index(1) > -1:
                    MSB_shifted = MSB_output.shift_right()

                    if modp:
                        result = MSB_shifted.modp(modp)
                        output.append(result)
                    else:
                        MSB_shifted = MSB_output.shift_right()
                        output.append(MSB_shifted)

            # if MSB not = 1
            except ValueError:
                MSB_shifted = MSB_output.shift_right()
                output.append(MSB_shifted)

        result_sum = Polynomial2([0])

        for index, coeff in enumerate(self.coeffs):
            if coeff == 1:
                result_sum = result_sum.add(output[index])

        return result_sum

    @property
    def deg(self):
        return len(self.coeffs) - 1

    @property
    def lc(self):
        return self.coeffs[-1]

    def div(self,p2):
        q,r = Polynomial2([0]), deepcopy(self)

        b,c = p2, p2.lc
        
        if (r.deg >= p2.deg):
            s = Polynomial2([0 for i in range(r.deg - p2.deg)] + [1])
            q = s.add(q)
            r = r.sub(s.mul(b))

        return q, r

    def __str__(self):
        output = ""

        for index, coeff in enumerate(self.coeffs[::-1]):
            if (len(self.coeffs)-index-1) == 0 and coeff == 1: output += f"1"
            elif (len(self.coeffs)-index-2) == 1: output += f"x+"
            elif coeff == 1 and (len(self.coeffs)-index-1) != 1:
                    output += f"x^{len(self.coeffs)-index-1}+"

        
        return output.strip("+")

    def getInt(self):
        result = 0
        for index,coeff in enumerate(self.coeffs):
            result += coeff * (2**index)
            
        return result

class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.x = x
        self.n = n
        self.ip = ip

    def add(self,g2):
        p1 = self.getPolynomial2()
        p2 = g2.getPolynomial2()
        result = p1.add(p2)
        result = result.modp(self.ip)

        return GF2N(result.getInt(),self.n,self.ip)

    def sub(self, g2):
        return self.add(g2.p)

    def mul(self, g2):
        p1 = self.getPolynomial2()
        p2 = g2.getPolynomial2()
        result = p1.mul(p2, self.ip)
        return GF2N(result.getInt(), self.n, self.ip)

    def div(self, g2):
        p1 = self.getPolynomial2()
        p2 = g2.getPolynomial2()

        quotient, remainder = p1.div(p2)
        quotient, remainder = quotient.getInt(),remainder.getInt()
        return (GF2N(quotient, self.n, self.ip), GF2N(remainder, self.n,self.ip))

    def getPolynomial2(self):
        binary = bin(self.x)[2:]
        polynomial = Polynomial2([int(x) for x in binary][::-1])

        return polynomial

    def __str__(self):
        return str(self.getPolynomial2().getInt())

    def getInt(self):
        return self.getPolynomial2().getInt()

    def egcd(a,b):
        if a == 0: return (b, 0, 1)
        else:
            g, y, x = GF2N.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def mulInv(self):
        irreduciable_polynomial = self.ip.getInt()
        reduction_polynomial = self.getPolynomial2().getInt()

        t1, t2 = Polynomial2([0]), Polynomial2([1])

        r1,reduction_polynomial,t1 = GF2N.egcd(irreduciable_polynomial,reduction_polynomial)

        if (r1 == 1):
            return GF2N(t1, self.n, self.ip)

        if (self.x == 0):
            return GF2N(0, self.n, self.ip)

    def affineMap(self):
        rhs = [1,1,0,0,0,1,1,0]
        b_prime = self.getPolynomial2().coeffs
        result = []
        index = 0
        for bit_array in self.affinemat:
            new_array = []
            for x_i, y_i in zip(bit_array, b_prime):
                new_array.append(x_i & y_i )

            res = 0
            for bit in new_array:
                res = res ^ bit
            res = res ^ rhs[index]
            result.append(res)
            index += 1
        return GF2N(Polynomial2(result).getInt(), self.n, self.ip)

print ('\nTest 1')
print ('======')
print ('p1=x^5+x^2+x')
print ('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print ('p3= p1-p2 =',p3)

print ('\nTest 2')
print ('======')
print ('p4=x^7+x^4+x^3+x^2+x')
print ('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print ('p5=p1*p4 mod (modp)=',p5)

print ('\nTest 3')
print ('======')
print ('p6=x^12+x^7+x^2')
print ('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print ('q for p6/p7=',p8q)
print ('r for p6/p7=',p8r)

print ('\nTest 4')
print ('======')
g1=GF2N(100)
g2=GF2N(5)
print ('g1 = ',g1.getPolynomial2())
print ('g2 = ',g2.getPolynomial2())
g3=g1.add(g2)
print ('g1+g2 = ',g3)

print ('\nTest 5')
print ('======')
ip=Polynomial2([1,1,0,0,1])
print ('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print ('g4 = ',g4.getPolynomial2())
print ('g5 = ',g5.getPolynomial2())
g6=g4.mul(g5)
print ('g4 x g5 = ',g6.getPolynomial2())

print ('\nTest 6')
print ('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print ('g7 = ',g7.getPolynomial2())
print ('g8 = ',g8.getPolynomial2())
q,r=g7.div(g8)
print ('g7/g8 =')
print ('q = ',q.getPolynomial2())
print ('r = ',r.getPolynomial2())

print ('\nTest 7')
print ('======')
ip=Polynomial2([1,1,0,0,1])
print ('irreducible polynomial',ip)
g9=GF2N(0b101,4,ip)
print ('g9 = ',g9.getPolynomial2())
print(g9.mulInv())
print ('inverse of g9 =',g9.mulInv().getPolynomial2())

print ('\nTest 8')
print ('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print ('irreducible polynomial',ip)
g10=GF2N(0xc2,8,ip)
print ('g10 = 0xc2')
g11=g10.mulInv()
print ('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print ('affine map of g11 =',hex(g12.getInt()))