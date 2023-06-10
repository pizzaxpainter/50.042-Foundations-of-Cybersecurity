#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse

nokeybits=80
blocksize=64

def encrypt(block,key):
    padding = blocksize - len(block)
    if padding > 0:
        block += bytes(padding for i in range(padding))

    output = int.from_bytes(block, byteorder='big')
    return present(output, key)

def remove_padding(block):
    padding = block & 0xFF
    for i in range(padding):
        temp_block = (block >> 8 * i) & 0xFF
        if temp_block != padding:
            return block, 8
    
    block = block >> 8 * padding
    return block, 8-padding

def decrypt(block,key):
    encrypted = int.from_bytes(block, byteorder='big')
    return present_inv(encrypted, key)

def ecb(infile,outfile,key,mode):
    pass
    with open(infile,mode="rb") as fin, open(outfile, mode="wb") as fout:
            if mode.upper() == "E":
                print("Encrypting.....")
                while(True):
                    data = fin.read(blocksize)
                    if not data: break
                    output = encrypt(data,key)
                    fout.write(output.to_bytes(blocksize, byteorder = "big"))

                print("Encryption Complete")

            if mode.upper() == "D":
                output = []
                print("Decrypting.....")
                while(True):
                    data = fin.read(blocksize)
                    if not data: break
                    output.append(decrypt(data,key))
                output[-1], bits_to_write = remove_padding(output[-1])

                for bits in output[:-1]:
                    fout.write(bits.to_bytes(8,byteorder = "big"))
                fout.write(output[-1].to_bytes(bits_to_write,byteorder = "big"))

                print("Decryption Complete")
            
    fin.close()
    fout.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile



