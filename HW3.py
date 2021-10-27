# Name: Jacob Gregie
# FSUID: JCG19
# Due Date: November 5th 2021
# The program in this file is the individual work of Jacob Gregie

import random
from datetime import datetime
import binascii


def encrypt(plaintext, key):

    temp_string = plaintext[0:8]
    string_block = ""
    for x in temp_string:
        string_block += str(ord(x))
    int_block = int(string_block)
    
    print(string_block)
    print(int_block)







'''

    # convert plaintext to binary
    bin = ''.join(format(ord(i), '08b') for i in plaintext)
    print (bin)

    ciphertext = ""
    while bin:
        # pad the binary plaintext with 0's
        if len(bin) < 64:
            while len(bin) != 64:
                bin += '0'
        
        # acquire the next 64 bit block of the binary plaintext
        block = bin[0:64]
        print (block)

        # run DES function for each block
        #ciphertext += DES(block, key)

        # remove the first 64 bits from the binary plaintext for the next loop
        bin = bin[64:]'''

def decrypt(ciphertext, key):
    print("hey")

def DES(num, key):

    # Initial Permutation
    pt = permute(pt, initial_perm, 64)
     
    # Splitting
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
        #  Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, exp_d, 48)
         
        # XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])
 
        # S-boxex: substituting the value from s-box table by calculating row and column
        sbox_str = ""
        for j in range(0, 8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)
             
        # Straight D-box: After substituting rearranging the bits 
        sbox_str = permute(sbox_str, per, 32)
         
        # XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result
         
        # Swapper
        if(i != 15):
            left, right = right, left
     
    # Combination
    combine = left + right
     
    # Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text






initial_perm = [58,	50,	42,	34,	26,	18,	10,	2,
                60,	52,	44,	36,	28,	20,	12,	4,
                62,	54,	46,	38,	30,	22,	14,	6,
                64,	56,	48,	40,	32,	24,	16,	8,
                57,	49,	41,	33,	25,	17,	9 ,	1,
                59,	51,	43,	35,	27,	19,	11,	3,
                61,	53,	45,	37,	29,	21,	13,	5,
                63,	55,	47,	39,	31,	23,	15,	7]

final_perm = [40,	8,	48,	16,	56,	24,	64,	32,
              39,	7,	47,	15,	55,	23,	63,	31,
              38,	6,	46,	14,	54,	22,	62,	30,
              37,	5,	45,	13,	53,	21,	61,	29,
              36,	4,	44,	12,	52,	20,	60,	28,
              35,	3,	43,	11,	51,	19,	59,	27,
              34,	2,	42,	10,	50,	18,	58,	26,
              33,	1,	41,	9 ,	49,	17,	57,	25]

exp_d = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5 ,
         6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1 ]

per = [ 16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25 ]

pc2 = [14,	17,	11,	24,	1 ,	5 ,
       3 ,	28,	15,	6 ,	21,	10,
       23,	19,	12,	4 ,	26,	8 ,
       16,	7 ,	27,	20,	13,	2 ,
       41,	52,	31,	37,	47,	55,
       30,	40,	51,	45,	33,	48,
       44,	49,	39,	56,	34,	53,
       46,	42,	50,	36,	29,	32]

sbox = [14, 4 , 13, 1 , 2 , 15, 11, 8 , 3 , 10, 6 , 12, 5 , 9 , 0 , 7 ,
        0 , 15, 7 , 4 , 14, 2 , 13, 1 , 10, 6 , 12, 11, 9 , 5 , 3 , 8 ,
        4 , 1 , 14, 8 , 13, 6 , 2 , 11, 15, 12, 9 , 7 , 3 , 10, 5 , 0 ,
        15, 12, 8 , 2 , 4 , 9 , 1 , 7 , 5 , 11, 3 , 14, 10, 0 , 6 , 13]

# seed random with current time
random.seed(datetime.now())

print ("Enter a string:")
plaintext = input()
while (plaintext.lower() != "exit"):

    # get random 56 bit key
    key = (random.getrandbits(56))
    key = bin(key)[2:]

    # randomly pad the key with 0's or 1's until it's 56 bits
    # sometimes getrandbits will not give 56 bits
    while (len(key) < 56):
        key += str(random.randint(0, 1))

    # encrypt
    ciphertext = encrypt(plaintext, key)
    #print ("Ciphertext = " + ciphertext)
        
    print ("Enter a string:")
    plaintext = input()

print("bye")