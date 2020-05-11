#!/usr/bin/python3.7


import pickle
import string
import sys

from pathlib  import Path
from time     import sleep
from colorama import Fore, Style

from fileIO import file_lines_into_list
from Rotors import Rotor
from Wiring import Wiring


alph       = string.ascii_lowercase
ALPH       = string.ascii_uppercase
digits     = '0123456789'
spec_chars = ['\'', ';', ':', '.', '"', '?', '!', ',', ' ', '\n', '\t']

class EnigmaMachine:

    def __init__(self):
        self.rotor1, self.rotor2, self.rotor3 = Rotor(), Rotor(), Rotor()
        self.wiring = Wiring()
        self.reflector = Wiring()


    ################
    #Saving Machine#
    ################


    def pickle_machine(self):
        data = [self.rotor1, self.rotor2, self.rotor3,
                self.wiring,
                self.reflector]

        with open('data.pickle', mode='wb') as f:
            pickle.dump(data, f)


    def unpickle_machine(self):
        try:
            with open('data.pickle', mode='rb') as f:
                data = pickle.load(f)

                self.rotor1, self.rotor2, self.rotor3,
                self.wiring,
                self.reflector = data

        except IOError:
            print('Error Loading Machine')
            print('Generating New Machine...')


    #######################
    #Encryption/Decryption#
    #######################


    def get_input(self):

        answer = input(
            'Do you want to encode a file? Note: The file will be deleted in accordance with best security practices. (y/n) ')

        if answer.strip().lower()[0] == 'y':
            path = input('Provide the absolute path to the file: ')
            file_content = file_lines_into_list(path)
            Path(path).unlink()

            return file_content

        if answer.strip().lower()[0] == 'n':
            print('Enter the string you would like to encrypt/decrypt. CTRL+D ends input')
            user_input = sys.stdin.read()

            return user_input


    def map_input(self, letter, verbose=False):
        '''Maps each letter through wiring, forward rotors, reflector backward rotors, wiring
        Arguments:
            ::
        '''
        r1, r2, r3 = self.rotor1.rotor, self.rotor2.rotor, self.rotor3.rotor
        t1, t2, t3 = self.rotor1.reverse(), self.rotor2.reverse(), self.rotor3.reverse()  # reverse rotors so letter maps backwards through them
        wr = self.wiring.wiring
        rf = self.reflector.wiring

        if verbose:
            n = alph.index(letter)
            print('encryption path: {0} -> {1} -> {2} -> {3} -> {4} -> {5} -> {6} -> {7} -> {8} -> {9}'.format(
                letter,
                alph[wr[n]],
                alph[r1[wr[n]]],
                alph[r2[r1[wr[n]]]],
                alph[r3[r2[r1[wr[n]]]]],
                alph[rf[r3[r2[r1[wr[n]]]]]],
                alph[t3[rf[r3[r2[r1[wr[n]]]]]]],
                alph[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]],
                alph[t1[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]]],
                alph[wr[t1[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]]]]))

            return alph[wr[t1[t2[t3[rf[r3[r2[r1[wr[n]]]]]]]]]]

        return alph[wr[t1[t2[t3[rf[r3[r2[r1[wr[alph.index(letter)]]]]]]]]]]


    def encode(self, user_input, machine_settings = (0,0,0), decrypt=False, verbose=False, use_file=False):
        '''
        :d: decrypt (allow seting rotor positions)
        :o: open encode
        :f: output to file
        '''
        output = []

        if decrypt:
            self.rotor1.set_position(machine_settings[0])
            self.rotor2.set_position(machine_settings[1])
            self.rotor3.set_position(machine_settings[2])
        else:
           rotor_settings = self.rotor1.pos, self.rotor2.pos, self.rotor3.pos

        # user_input = self.get_input()

        for char in user_input:
            print(char)
            if char in spec_chars:
                output.append(char)
                #  do not advance rotors for special chars
                continue
            if char in digits:
                print(True)
                output.append(char)
                continue
                #  do not advance rotors for digits
            if char in ALPH:
                if verbose:
                    output.append(self.map_input(char.lower(), verbose).upper())
                else:
                    output.append(self.map_input(char.lower(),).upper())
            else:
                if verbose:
                    output.append(self.map_input(char, verbose))
                else:
                    output.append(self.map_input(char))

            self.rotor1.advance()
            self.rotor1.pos += 1
            if self.rotor1.pos == 26:
                self.rotor1.pos = 0
                self.rotor2.pos += 1
                self.rotor2.advance()
                if self.rotor2.pos == 26:
                    self.rotor2.pos = 0
                    self.rotor3.pos += 1
                    self.rotor3.advance()
                    if self.rotor3.pos == 26:
                        self.rotor3.pos = 0


        output = ''.join(output)

        if decrypt:
            return output
        else:
            return rotor_settings, output

    ##########
    #Listener#
    ##########


    def listen(self):

        answer = input('Do you wish to load the previous machine?  (y/n) ')

        if answer == 'y':
            self.unpickle_machine()
            # rotor1, rotor2, rotor3, rotor1_pos, rotor2_pos, rotor3_pos, wiring, reflector = unpickle_machine()

        while True:
            try:
                answer = input(
                    'What would you like to do? \n (1) Encrypt Message \n (2) Decrypt Message \n (q) quit \n')

                if answer == '1':
                    answer = input(
                        'Which would you like? \n (0) Secret Encryption \n (1) Open Encryption \n (2) Output to file \n')
                    if answer == '0':
                        self.encode()
                        continue
                    if answer == '1':
                        self.encode(verbose=True)
                        continue
                    if answer =='2':
                        self.encode(machine, use_file=True)

                elif answer == '2':
                    answer = input(
                        'Which would you like? \n (0) Secret Decryption \n (1) Open Decryption \n (2) Output to file \n')
                    if answer == '0':
                        self.encode(decrypt=True)
                        continue
                    if answer == '1':
                        self.encode(decrypt=True, verbose=True)
                        continue
                    if answer == '2':
                        self.encode(decrypt=True, use_file=True)

                elif answer == 'q':
                    answer = input('Do you wish to save current machine? (y/n): ').strip().lower()[0]
                    if answer == 'y':
                        self.pickle_machine()
                    print('Exiting')
                    break
                else:
                    print(Fore.YELLOW + '\n  {:*^21} \n'.format('Invalid Input') + Style.RESET_ALL)
                    sleep(1)

            except ValueError:
                print('\n  {:*^21} \n'.format('Invalid Input'))
                sleep(1)
                continue


# if __name__ == '__main__':
#     machine = EnigmaMachine()
#     machine.listen()