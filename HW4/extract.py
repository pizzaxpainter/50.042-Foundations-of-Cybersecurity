#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse

def getInfo(headerfile):
    with open(headerfile, 'rb') as fheader:
        header_bytes = fheader.read()
    return header_bytes

def extract(infile,outfile,headerfile):
    output = []
    valid = True
    bit_mapper = {}
    frequency = -1
    with open(headerfile, 'r') as fheader:
        header = fheader.read()
    header_length = len(getInfo(headerfile))
    with open(infile, 'br') as fin:
        header_throw = fin.read(header_length + 1)
        while valid:
            # Read in 8 bytes
            byte_in = fin.read(8)
            if byte_in == b"":
                valid = False
            else:
                if byte_in in bit_mapper.keys():
                    bit_mapper[byte_in] += 1
                else:
                    bit_mapper[byte_in] = 1
                output.append(byte_in)
    # Base the 1s on the max frequency and the 0s on the other 
    # Note: If the above 2 produce the wrong result, swap them (code this if result is bad)
    for k, v in bit_mapper.items():
        if v > frequency:
            key_highest_freq = k
            frequency = v
    with open(outfile, 'w') as fout: 
        # Write the header first 
        fout.write(header + '\n')
        for encrypted in output:
            if encrypted == key_highest_freq:
                fout.write('0' * 8)
            else:
                fout.write('1' * 8 )
    return True

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)

    success=extract(infile,outfile,headerfile)