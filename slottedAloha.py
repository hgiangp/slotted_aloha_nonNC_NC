from random import Random
import random
import numpy as np
import matplotlib.pyplot as plt 


class SlottedAloha:
    def __init__(self):
        self._g = np.arange(0, 1, 0.1)
        self._mu = 0.6
        self._q = 0.7

        self.queue_length = 0
        self.no_slot = 10000
        self.throughput = []

    def non_coding(self): 

        for G in self._g:
            tmp_g = G/2
            pass_pkt = 0
            queue_length = 0 
            print(tmp_g)
            first_iteration = True 
            for i in range(self.no_slot):  
                Atrans = False 
                BTrans = False 
                gA = np.random.rand()
                if gA > tmp_g: 
                    Atrans = True 
                gB = np.random.rand()
                if gB > tmp_g: 
                    BTrans = True 

                if first_iteration == True: 
                    first_iteration = False
                    if Atrans == True: 
                        queue_length += 1 
                    if BTrans == True: 
                        queue_length += 1 

                if queue_length > 0: 
                    gR = np.random.rand()
                    if gR > self._q: 
                        if Atrans == False and BTrans == False: 
                            queue_length = queue_length - 1 
                            pass_pkt += 1   
                    else: 
                        if Atrans == True: 
                            queue_length += 1 
                        if BTrans == True: 
                            queue_length += 1 
            
            print(f'pass_pkt = {pass_pkt} queue_length = {queue_length} total = {pass_pkt + queue_length}')
            thput = pass_pkt/(pass_pkt + queue_length)
            
            self.throughput.append(thput)
            
        plt.plot(self._g, self.throughput, 'o-')
        plt.show()

               










# if __name__ == '__main': 
SA = SlottedAloha()
SA.non_coding()


