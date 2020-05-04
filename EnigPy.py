#!/usr/bin/python3

'''
Enigma Machine Emulator

Allows user to generate/load an enigma machine for the encryption/decryption of plain text messages.
Machine is saved in plain text files in directory script is run from. 

Author: Aaron Zolotor
'''

from random import sample
from copy import deepcopy
from time import sleep
import pickle
import pathlib
import string
from colorama import Fore, Style

from ListMethods import *
from fileIO import * 

####################
# Global Variables #
####################
# alphabet list whose indicies are used to exchange letters with numbers for encryption/decryption
alph = string.ascii_lowercase
ALPH = string.ascii_uppercase
spec_chars = ['\'',';',':','.','"','?','!',',', ' ']

wiring = []
reflector = []
rotor1, rotor1_pos, rotor2, rotor2_pos, rotor3, rotor3_pos = [], 0, [], 0, [], 0

######################
# Machine Generation #
######################
# A default machine and code to generate a random machine and report its settings


def generate_reflector():
    '''
    Generates list of corresponding pairs. i.e. l[0]=1, l[1]=0
        Arguments:
                none
    Returns:
        :rf: machine reflector list
    '''

    indices = [x for x in range(0, 26, 1)]
    rf = [0 for x in range(0, 26, 1)]

    while len(indices) > 0:
        smp = sample(indices, 2)
        for elt in smp:
            indices.remove(elt)
            rf[smp[0]] = smp[1]
            rf[smp[1]] = smp[0]
    return rf


def generate_wiring():
    '''
    Generates list of corresponding pairs. i.e. l[0]=1, l[1]=0
    Returns:
            :wr: machine wiring list
    '''
    wr = [0 for x in range(0, 26, 1)]
    indices = [x for x in range(0, 26, 1)]
    while len(indices) > 0:
        smp = sample(indices, 2)
        for elt in smp:
            indices.remove(elt)
            wr[smp[0]] = smp[1]
            wr[smp[1]] = smp[0]


    return wr


def generate_rotors():
    '''
    Generates three list containing distinct elements between 0 and 25
    Arguments:
        none
        Return:
                :r1: machine rotor1 list
                :r2: machine rotor2 list
                :r3: machine rotor3 list
    '''
    # num_of_rotors = input('How many rotors would you like? (Enigma machines use 3)')
    r1 = sample(range(0, 26), 26)  # Generates a list of unique values between 0-25
    r2 = sample(range(0, 26), 26)
    r3 = sample(range(0, 26), 26)

    return r1, r2, r3


def set_wires(al):
    '''Allows user to wire pairs of letters together manually
    Arguments:
                :al: list containing alphabet
        Returns:
                                :wr: mach1425 Lincoln Hwy, DeKalb, IL 60115ine wiring list
    '''
    print('Remember each letter must be wired to a unique place and the letters must be mapped in pairs. \n i.e. a -> c => c -> a')
    # deepcopy of alphabet list so we may strip letters out of it leaving the original as an index reference
    tempAl = deepcopy(al)
    wr = [None for x in range(0, 26, 1)]

    while len(tempAl) > 0:
        letter = tempAl[0]
        toBeMapped = al.index(letter)
        mappedTo   = None

        while mappedTo is None:
            try:
                x = input(f'Where would you like to map {letter}? ').strip().lower()
                mappedTo = al.index(x)
            except ValueError as error:
                print(ValueError)
                print('Please choose a legal value...')

        while True:
            # loop to ensure user chooses legal values
            # ensures letter is not mapped to itself
            if x not in alph:
                print('You must enter a letter')
                x = input('Where would you like to wire {0}: '.format(letter))
                mappedTo = al.index(x)
                continue

            if x == letter:
                print('You may not assign a letter to itself.')
                x = input('Where would you like to wire {0}: '.format(letter))
                mappedTo = al.index(x)
                continue

            # ensures unique input
            if mappedTo in wr:
                print('This letter has already been mapped. Please choose another.')
                x = input('Where would you like to wire {0}: '.format(letter))
                mappedTo = al.index(x)
                continue

            else:
                break
            #!Consider replacing this with a try/catch block!#

        # Mapping the indices of the corresponding letter to one another
        wr[toBeMapped] = mappedTo
        wr[mappedTo] = toBeMapped
        # removing the mapped letters
        tempAl.remove(letter)
        tempAl.remove(x)
        print('The remaining letters are ' + str(tempAl))

    return wr


def generate_machine(al, s=False):

    if s:
        print()
        print('Generating Rotors')
        r1, r2, r3 = generate_rotors()
        print('Generating Reflector')
        rf = generate_reflector()
        print('Setting Wires')
        wr = set_wires(al)
        print()
    else:
        print()
        print('Generating Rotors')
        r1, r2, r3 = generate_rotors()
        print('Generating Reflector')
        rf = generate_reflector()
        print('Generating Wiring')
        wr = generate_wiring()
        print()

    return r1, r2, r3, wr, rf

################
#Getter Methods#
################


def get_rotors(r1, r2, r3, al=alph, r1pos=rotor1_pos, r2pos=rotor2_pos, r3pos=rotor3_pos):
    print('The wiring of rotor1 in position {0} is:'.format(r1pos))
    for i in range(26):
        print('({0} -> {1})'.format(al[i], al[r1[i]]), end=' ')
        print()

    print('The wiring of rotor2 in position {0} is:'.format(r2pos))
    for i in range(26):
        print('({0} -> {1})'.format(al[i], al[r2[i]]), end=' ')
        print()

    print('The wiring of rotor3 in position {0} is:'.format(r3pos))
    for i in range(26):
        print('({0} -> {1})'.format(al[i], al[r3[i]]), end=' ')
        print()


def get_wires(al=alph, wr=wiring):

    print('The frontboard wiring is:')

    for i in range(26):
        print('({0} -> {1})'.format(al[i], al[wr[i]]), end=' ')

    print()


def get_reflector(al=alph, rf=reflector):

    print('The reflector wiring is:')

    for i in range(26):
        print('({0} -> {1})'.format(al[i], al[rf[i]]), end=' ')

    print()

##################
# Saving Machine #
##################


def save_reflector(rf):
    with open('reflector.txt', mode='w') as f:
        for num in rf:
            f.write(str(num)+'\n')


def save_rotors(r1, r2, r3, r1pos, r2pos, r3pos):
    with open('rotors.txt', mode='w') as f:
        f.write(str(r1pos)+'\n')
        for num in r1:
            f.write(str(num)+'\n')

        f.write(str(r2pos)+'\n')
        for num in r2:
            f.write(str(num)+'\n')

        f.write(str(r3pos)+'\n')
        for num in r3:
            f.write(str(num)+'\n')


def save_wiring(wr):
    with open('wiring.txt', mode='w') as f:
        for num in wr:
            f.write(str(num)+'\n')


def save_machine(r1, r2, r3, r1pos, r2pos, r3pos, wr, rf, v=None):
    ''' v=True for verbose mode
    '''
    if v is not None:
        print('Saving rotors...')
        save_rotors(r1, r2, r3, r1pos, r2pos, r3pos)
        print('Saving wiring...')
        save_wiring(wr)
        print('Saving reflector')
        save_reflector(rf)
        print('Machine Successfully saved')
    else:
        save_rotors(r1, r2, r3, r1pos, r2pos, r3pos)
        save_wiring(wr)
        save_reflector(rf)


###################
#Importing Machine#
###################


def import_rotors():
    '''Imports saved state of rotors from rotors.txt
            Arguments:
            :r1:
            :r2:
            :r3:
            :r1pos:
            :r2pos:
            :r3pos:
    '''
    r1, r2, r3, r1pos, r2pos, r3pos = [], [], [], 0, 0, 0
    with open('rotors.txt.', mode='r') as f:
        r1pos = int(f.readline())
        for i in range(26):
            r1.append(int(f.readline()))

        r2pos = int(f.readline())
        for i in range(26):
            r2.append(int(f.readline()))

        r3pos = int(f.readline())
        for i in range(26):
            r3.append(int(f.readline()))

    return r1, r2, r3, r1pos, r2pos, r3pos


def import_reflector():
    '''Imports save state of reflector from reflector.txt
            Arguments:
            :rf:
    '''
    rf = []
    with open('reflector.txt.', mode='r') as f:
        for i in range(26):
            rf.append(int(f.readline()))

    return rf


def import_wiring():
    '''Imports save state of wiring from wiring.txt
            returns:
            :wr:
    '''
    wr = []
    with open('wiring.txt.', mode='r') as f:
        for i in range(26):
            wr.append(int(f.readline()))

        return wr


def import_machine():
    '''A call of the three import functions
            Arugments:
            :r1:
            :r2:
            :r3:
            :r1pos:
            :r2pos:
            :r3pos:
            :rf:
            :wr:
    '''
    r1, r2, r3, r1pos, r2pos, r3pos = import_rotors()
    rf = import_reflector()
    wr = import_wiring()
    print(rf, wr, r1pos, r2pos, r3pos, r1, r2, r3, sep='\n')
    return r1, r2, r3, r1pos, r2pos, r3pos, rf, wr


######################
#Machine Manipulation#
######################


def reverse_rotors(r1, r2, r3):
    '''Changes the direction of the rotor. e.g. if 1 -> 4, then 4 -> 1
    Arguments:
    :r1: List of integers of length 26
    :r2: List of integers of length 26
    :r3: List of integers of length 26
    '''
    r1 = exchange_index_pos(r1)
    r2 = exchange_index_pos(r2)
    r3 = exchange_index_pos(r3)

    return r1, r2, r3


def set_rotor_position(r1, r2, r3, r1pos, r2pos, r3pos):
    '''Used to set/reset rotor position so messages may be decoded. Finds minimum number of rotations (forwards or backwards) such that we get to desired position and cycle forward backwards said number of times
    Arguments:
    :r1:
    :r2:
    :r2:
    :r1pos:
    :r1pos:
    :r1pos:
    '''
    pos1 = int(input('What position would you like for rotor 1? (0-25): '))
    pos2 = int(input('What position would you like for rotor 2? (0-25): '))
    pos3 = int(input('What position would you like for rotor 3? (0-25): '))

    if pos1 < r1pos:
        r1 = reverse_cycle_list(r1, r1pos-pos1)
        r1pos = pos1

    if pos1 > r1pos:
        r1 = cycle_list(r1, pos1-r1pos)
        r1pos = pos1

    if pos2 < r2pos:
        r2 = reverse_cycle_list(r2, r2pos-pos2)
        r2pos = pos2

    if pos2 > r2pos:
        r2 = cycle_list(r2, pos2-r2pos)
        r2pos = pos2

    if pos3 < r3pos:
        r3 = reverse_cycle_list(r3, r3pos-pos3)
        r3pos = pos3

    if pos3 > r3pos:
        r3 = cycle_list(r3, pos3-r3pos)
        r3pos = pos3

    return r1, r2, r3, r1pos, r2pos, r3pos

#######################
#Encryption/Decryption#
#######################


def get_input():

    answer = input('Do you want to encode a file? Note: The file will be deleted in accordance with best security practices. (y/n) ')

    if answer.strip().lower()[0] == 'y':
        path = input('Provide the absolute path to the file: ')
        file_content = file_lines_into_list(path)
        Path(path).unlink()

        return file_content

    if answer.strip().lower()[0] == 'n':
        print('Enter the string you would like to encrypt/decrypt. Enter a blank line when you\'re done.')
        sentinel = ''
        user_input =  list(iter(input, sentinel))

        return user_input


def map_input(letter, r1, r2, r3, wr, rf, al, o=False):
    '''Maps each letter through wiring, forward rotors, reflector backward rotors, wiring
    Arguments:
    :letter: character
    :r1: list of length 26
    :r2: list of length 26
    :r3: list of length 26
    :wr: list of length 26
    :rf: list of length 26
    '''
    t1, t2, t3 = reverse_rotors(r1, r2, r3)  # reverse rotors so letter maps backwards through them

    if o:
        n = al.index(letter)
        print('encryption path: {0} -> {1} -> {2} -> {3} -> {4} -> {5} -> {6} -> {7} -> {8} -> {9}'.format(
            letter,
            al[wr[n]],
            al[r1[wr[n]]],
            al[r2[r1[wr[n]]]],
            al[r3[r2[r1[wr[n]]]]],
            al[rf[r3[r2[r1[wr[n]]]]]],
            al[t3[rf[r3[r2[r1[wr[n]]]]]]],
            al[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]],
            al[t1[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]]],
            al[wr[t1[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]]]]))

        return al[wr[t1[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]]]]

    return al[wr[t1[t2[t3[rf[r3[r2[r1[wr[al.index(letter)]]]]]]]]]]
    return al[wr[t1[t2[t3[rf[r3[r2[r1[wr[al.index(letter)]]]]]]]]]]


def encode(r1, r2, r3, r1pos, r2pos, r3pos, wr, rf, al, d=False, o=False,f=False):
    '''
    :d: decrypt (allow seting rotor positions)
    :o: open encode
    :f: output to file
    '''
    output = []

    if d:
        r1, r2, r3, r1pos, r2pos, r3pos = set_rotor_position(r1, r2, r3, r1pos, r2pos, r3pos)
    else:
        print('rotor settings are {0}, {1}, {2} \n Please write these down so you can decode the message.'.format(
            r1pos, r2pos, r3pos))

    user_input = get_input()


    for line in user_input:
        for letter in line:
            if letter in spec_chars:  # handle special chars
                output.append(letter)
                continue
            if letter in ALPH:
                if o:
                    output.append(map_input(letter.lower(), r1, r2, r3, wr, rf, al, o).upper())
                else:
                    output.append(map_input(letter.lower(), r1, r2, r3, wr, rf, al).upper())
            else:
                if o:
                    output.append(map_input(letter, r1, r2, r3, wr, rf, al, o))
                else:
                    output.append(map_input(letter, r1, r2, r3, wr, rf, al))

            r1 = cycle_list(r1)
            r1pos += 1
            if r1pos == 26:
                r1pos = 0
                r2pos += 1
                r2 = cycle_list(r2)
                if r2pos == 26:
                    r2pos = 0
                    r3pos += 1
                    r3 = cycle_list(r3)
                    if r3pos == 26:
                        r3pos = 0

        output.append('\n')

    output = ''.join(output)

    if f:
        Path(input('Enter the path for output: ')).write_text(output)
    else:
        print(Fore.GREEN + output +Style.RESET_ALL)
    return r1, r2, r3, r1pos, r2pos, r3pos


##############################################################################################################################################################
if __name__ == '__main__':

    answer = input('Do you wish to load the previous machine?  (y/n) ')

    if answer == 'y':
        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, reflector, wiring = import_machine()
        #rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector = unpickle_machine()
    else:
        answer = input('Do you wish to set the wiring? (y/n) ')
        if answer == 'y':
            rotor1, rotor2, rotor3, wiring, reflector = generate_machine(alph, True)
        else:
            rotor1, rotor2, rotor3, wiring, reflector = generate_machine(alph)

    while True:
        try:
            answer = input(
                'What would you like to do? \n (1) Encrypt Message \n (2) Decrypt Message \n (q) quit \n')

            if answer == '1':
                answer = input(
                    'Which would you like? \n (0) Secret Encryption \n (1) Open Encryption \n (2) Output to file \n')
                if answer == '0':
                    rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos = encode(
                        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector, alph)
                    continue
                if answer == '1':
                    rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos = encode(
                        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector, alph, o=True)
                    continue
                if answer =='2':
                    rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos = encode(
                        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector, alph, f=True)

            elif answer == '2':
                answer = input(
                    'Which would you like? \n (0) Secret Decryption \n (1) Open Decryption \n (2) Output to file \n')
                if answer == '0':
                    rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos = encode(
                        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector, alph, d=True)
                    continue
                if answer == '1':
                    rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos = encode(
                        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector, alph, d=True, o=True)
                    continue
                if answer == '2':
                    rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos = encode(
                        rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector, alph, d=True, f=True)

            elif answer == 'q':
                answer = input('Do you wish to save current machine? (y/n): ').strip().lower()[0]
                if answer == 'y':
                    save_machine(rotor1, rotor2, rotor3, rotor1_pos,
                                  rotor2_pos, rotor3_pos, wiring, reflector)
                    #pickle_machine(rotor1, rotor2, rotor3, rotor1_pos,
                                   #rotor2_pos, rotor3_pos, wiring, reflector)
                print('Exiting')
                break
            else:
                print('\n \t invalid input, please select a valid option \n')
                sleep(1)

        except ValueError:
            print('\n \t invalid input \n')
            sleep(1)
            continue