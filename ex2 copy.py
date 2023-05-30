
import sys
import argparse
import string

def encrypt(byte, key):
    if (key >= 0 and key <= 255):
        # mod ensures the looping eg. 255 + (key = 10) = 265 so need 265%256
        return (ord(byte) + key) % 256
    else:
        print("Key error")

def decrypt(byte, key):
    if (key >= 0 and key <= 255):
        return (ord(byte) - key) % 256
    else:
        print("Key error")


def doStuff(filein, fileout, key, mode):
    if (mode != "e" and mode != "E" and mode != "d" and mode != "D"):
        print("Invalid mode. Please input 'e' for encrpyting or 'd' for decrypting.")
    
    else:
        # open file handles to both files
        fin_b = open(filein, mode="rb")  # binary read mode
        fout_b = open(fileout, mode="wb")  # binary write mode
        
        result = bytearray()
        byte = fin_b.read(1)
        while byte:
            if (mode == "e" or mode == "E"):
                result.append(encrypt(byte, key))
            elif (mode == "d" or mode == "D"):
                result.append(decrypt(byte, key))
            byte = fin_b.read(1)

        fout_b.write(result)

        # close all file streams

        fin_b.close()
        fout_b.close()

# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k", dest = "key", type = int, help = "key")
    parser.add_argument("-m", dest = "mode", help = "encrypt or decrypt")

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    # key = int(args.key)
    key = args.key
    mode = args.mode
    
    doStuff(filein, fileout, key, mode)
