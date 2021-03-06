from __future__ import print_function
import os
import fractions
import sys
import key_gen
import algorithm
import math

args = ['-k', '-e', '-d']

def print_usage():
    print("Usage: [" + sys.argv[0] + "] [-option]")
    print("[-k] [# bits in the modulus N (power of two)] : generate a key of "
            "the form (N = pq, e [public], d [private])")
    print("[-e] [N = pq] [e (public)] [filename to read from]")
    print("[-d] [N = pq] [d (priate)] [filename to read from]")
    print("Encrypted/decrypted bytes sent to stdout")

def print_key(N, e, d, bit_len):
    print("="*40)
    print("N = p*q (where p,q are each " + str(bit_len / 2) + " bit-" +
        "primes) and N is " + str(bit_len) + " bits: ")
    # convert X into its hex form, take away the 0x and 'L' character at the end
    N_str = str(hex(N))[2:]
    if N_str[-1:] == 'L':
        N_str = N_str[:-1]
    print(N_str)
    print("Encryption exponent (public): ")
    print(str(hex(e))[2:])
    print("Decryption exponent (private): ")
    d_str = str(hex(d))[2:]
    if d_str[-1:] == 'L':
        d_str = d_str[:-1]
    print(d_str)
    print("="*40)

def is_power_of_two(n):
    # n is of the form 10000...0 and n-1 is of the form 1111...1
    return (n & (n - 1) == 0) and (n != 0)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in args:
        print_usage()

    elif sys.argv[1] == '-k':
        if len(sys.argv) != 3:
            print_usage()
        elif not is_power_of_two(int(sys.argv[2])) or int(sys.argv[2]) < pow(2,7):
            print("Modulus bit length must be power of two, 2^k with k > 6")
        else:
            bit_len = int(sys.argv[2])
            # bit_len / (# bits in a byte * 2 (each key half the total length))
            N, e, d = key_gen.key_gen(bit_len / 16)
            print_key(N, e, d, bit_len)
    elif sys.argv[1] == '-e':
        if len(sys.argv) != 5:
            print_usage()
        else:
            N = int(sys.argv[2], base=16)
            e = int(sys.argv[3], base=16)
            filename = sys.argv[4]
            algorithm.encrypt(N, e, filename)
    elif sys.argv[1] == '-d':
        if len(sys.argv) != 5:
            print_usage()
        else:
            N = int(sys.argv[2], base=16)
            d = int(sys.argv[3], base=16)
            filename = sys.argv[4]
            algorithm.decrypt(N, d, filename)

if __name__ == "__main__":
    main()
