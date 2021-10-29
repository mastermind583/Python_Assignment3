# Name: Jacob Gregie
# FSUID: JCG19
# Due Date: November 5th 2021
# The program in this file is the individual work of Jacob Gregie

import random
from datetime import datetime
import struct

def encrypt(plaintext, rk_list):
    cipher_text = "" 
    while plaintext:
        # Get the next 8 characters of the plaintext
        char_block = plaintext[0:8]
        plaintext = plaintext[8:]

        # Convert each character to binary, pads with 0's when necessary
        str_block = ""
        for i in char_block:
            temp = bin(ord(i))[2:]
            while len(temp) < 8:
                temp = '0' + temp
            str_block += temp

        while len(str_block) < 64:
            str_block += '0'

        # convert to an int and run the DES function
        int_block = int(str_block, 2)
        result = DES(int_block, rk_list)

        # Turn the result of the DES into each ascii value and concatenate onto string
        byte_string = struct.pack('>Q', result)
        for b in byte_string:      
            cipher_text += chr(b)

    return cipher_text

# With how this program is set up, decrypt does the exact same thing as encrypt
#   because the list of round keys is reversed
def decrypt(ciphertext, rev_rk_list):
    plain_text = "" 
    while ciphertext:
        char_block = ciphertext[0:8]
        ciphertext = ciphertext[8:]

        str_block = ""
        for i in char_block:
            temp = bin(ord(i))[2:]
            while len(temp) < 8:
                temp = '0' + temp
            str_block += temp
        while len(str_block) < 64:
            str_block += '0'

        int_block = int(str_block, 2)

        result = DES(int_block, rev_rk_list)

        # Turn integer into each ascii value and concatenate onto
        byte_string = struct.pack('>Q', result)
        for b in byte_string:
            plain_text += chr(b)

    return plain_text

def DES(num, rk_list):

    # Initial Permutation
    permutation = permute(num, initial_perm, 64, 64)
    
    # Splitting the number into 32 bit halves
    left = permutation >> 32 & 0b11111111111111111111111111111111
    right = permutation & 0b11111111111111111111111111111111
    
    for i in range(0, 16):
        # Apply an expansion permutation to the right half of the number to expand it to 48 bits
        right_expanded = permute(right, expansion_d, 48, 56)

        # XOR with the round key
        xor_int = right_expanded ^ rk_list[i]

        # Use an S-box (given on slide 17 of the DES slides) to shrink it back down to 32 bits.
        sbox_int = 0
        for j in range(0, 8):
            # 1st bit
            bit_position = j * 6 + 1
            row = 2* (xor_int >> (48 - bit_position) & 1)

            # 6th bit
            bit_position = j * 6 + 6
            row += (xor_int >> (48 - bit_position) & 1)

            # 2-4th bits
            bit_position = j * 6 + 2
            col = (i >> (48 - bit_position) & 0b111)

            # get the value of the substitution from the sbox
            val = sbox[16*row+col]

            # set each 4 bit block of the result to the substitution value
            sbox_int |= (val << (j*4))
             
        # Use an intermediary permutation 
        num = permute(sbox_int, perm, 32, 32)
         
        # XOR with the left half to get the right half for the next round
        result = left ^ num
        left = result
         
        # Swap left and right half
        if(i != 15):
            left, right = right, left
     
    # Combination
    num = (left << 32 | right)

    # Final permutation: final rearranging of bits to get cipher text
    test = permute(num, final_perm, 64, 64)
    return test

# Helper function that permutes the number using the passed in table
#  n is the number of elements in the array, bits is the number of bits that number starts with
def permute(number, table, n, bits):
    permutation = 0
    for i in range(0, n):
        # set each bit of the permutation integer if the corresponding bit of number
        #    acquired from the table is 1
        if (number >> (bits - table[i]) & 1 == 1):
            permutation |= 1 << i 
            
    return permutation

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

expansion_d = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5 ,
               6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
               12, 13, 12, 13, 14, 15, 16, 17,
               16, 17, 18, 19, 20, 21, 20, 21,
               22, 23, 24, 25, 24, 25, 26, 27,
               28, 29, 28, 29, 30, 31, 32, 1 ]

perm = [16,	7 ,	20,	21,	29,	12,	28,	17,
        1 ,	15,	23,	26,	5 ,	18,	31,	10,
        2 ,	8 ,	24,	14,	32,	27,	3 ,	9 ,
        19,	13,	30,	6 ,	22,	11,	4 ,	25]

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

print("DES Implementation:")
plaintext = input("Enter text to encrypt (\"Exit\" to quit): ")
while (plaintext.lower() != "exit"):
    # get random 56 bit key
    key = (random.getrandbits(56))

    # make a list of all 16 round keys
    rk_list = []
    for i in range(0, 16):    
        # cyclic shift left of the bits in the key
        shifted_key = (key << (i+1)) % (1 << 56) | (key >> (56 - (i+1)))
        
        # Compress the key to 48 bits using PC-2 and add it to the list
        new_key = permute(shifted_key, pc2, 48, 56)
        rk_list.append(new_key)

    # encrypt
    ciphertext = encrypt(plaintext, rk_list)

    # make a temporary ciphertext string to make the encryption appear nicer in the console
    temp_cipher = ""
    for x in ciphertext:
        if (32 <= ord(x) <= 126):
            temp_cipher += x
        else:
            temp_cipher += '.'

    print ("Encrypted text: " + temp_cipher)

    # reverse round key list and decrypt
    rev_rk_list = rk_list[::-1]
    plaintext = decrypt(ciphertext, rev_rk_list)
    print ("Decrypted text: " + plaintext)
       
    # ask for next string
    plaintext = input("\nNext text (\"Exit\" to quit): ")