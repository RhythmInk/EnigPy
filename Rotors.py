from random import sample

from ListMethods import cycle_list, reverse_cycle_list, exchange_index_pos

class Rotor:


    def __init__(self):
        self.rotor = sample(range(0, 26), 26)
        self.pos = 0


    def advance(self):

        self.rotor = cycle_list(self.rotor)


    def reverse(self):
        '''Changes the direction of the rotor. e.g. if 1 -> 4, then 4 -> 1. Returns the rotor objects so as not to destroy the original rotor configuration
        '''
        rev_rotor = exchange_index_pos(self.rotor)


        return rev_rotor


    def set_position(self, new_pos):
        '''Used to set/reset rotor position so messages may be decoded. Finds minimum number of rotations (forwards or backwards) such that we get to desired position and cycle forward/backwards said number of times.

        Arguments:
            None
        '''

        # new_pos = int(
        #     input(f'What position would you like for rotor {rotor_num}? (0-25): '))

        if new_pos < self.pos:
            self.rotor = reverse_cycle_list(self.rotor, self.pos-new_pos)
            self.pos = new_pos

        if new_pos > self.pos:
            self.rotor = cycle_list(self.rotor, new_pos-self.pos)
            self.pos = new_pos


    def __str__(self):

        return str(self.rotor)