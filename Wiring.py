from random import sample

class Wiring:

    def __init__(self):
        self.wiring = self.generate_wiring()


    def generate_wiring(self):
        '''
        Generates list of corresponding pairs. i.e. l[0]=1, l[1]=0
        Returns:
        :wiring: machine wiring list
        '''
        wiring = [0 for x in range(0, 26, 1)]
        indices = [x for x in range(0, 26, 1)]

        while len(indices) > 0:
            smp = sample(indices, 2)

            for elt in smp:
                indices.remove(elt)
                wiring[smp[0]] = smp[1]
                wiring[smp[1]] = smp[0]

        return wiring


    def __str__(self):

        return str(self.wiring)