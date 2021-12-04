import numpy as np
import matplotlib.pyplot as plt

A_PACKET = 1
B_PACKET = 2


class SlottedAloha:
    def __init__(self):
        self._g = np.arange(0, 2.1, 0.1)
        self._q = 0.6

        self.no_slot = 50000
        self.thput_sim = []
        self.thput_ana = []
    
    def thrput_non_coding(self, G): 
        S = G*(1-G/2)/(G + 1)
        return S 

    def non_coding(self): 

        for G in self._g:
            tmp_g = G/2
            pass_pkt = 0
            queue_length = 0
            print(tmp_g)
            queue_value = []
            for i in range(self.no_slot):  
                ATrans = np.random.rand() < tmp_g
                BTrans = np.random.rand() < tmp_g

                RTrans = (queue_length > 0) and (np.random.rand() < self._q)

                if RTrans: 
                    if (ATrans == False and BTrans == False) or (ATrans == False and BTrans == True and queue_value[0] == A_PACKET) or (ATrans == True and BTrans == False and queue_value[0] == B_PACKET): 
                        pass_pkt = pass_pkt + 1
                        queue_length = queue_length - 1
                        queue_value.remove(queue_value[0])

                else:
                    if ATrans == True and BTrans == False: 
                        queue_value.append(A_PACKET)
                        queue_length = queue_length + 1 
                    elif BTrans == True and ATrans == False: 
                        queue_value.append(B_PACKET)
                        queue_length = queue_length + 1 
                    
            # print(f'pass_pkt = {pass_pkt} queue_length = {queue_length}')
            thput = pass_pkt / self.no_slot 

            self.thput_sim.append(thput)
            self.thput_ana.append(self.thrput_non_coding(G))
            
        plt.plot(self._g, self.thput_sim, 'o', self._g, self.thput_ana, '-')
        plt.xlabel('Offer Traffic, G = 2g')
        plt.ylabel('Throughput, S')
        plt.title('Non-NC System')
        plt.legend(['Simulation', 'Theoretical'])
        plt.savefig('non_nc.png')
        # plt.show()
    
    def thrput_coding(self, G, q): 
        S = 2*q*G*(2 - G)/(q*(2 + G)**2 - G**2)
        return S
    
    def coding(self, tmp_q): 
        initial_q = tmp_q
        thput_sim = []
        thput_ana = []
        for G in self._g: 
            vA = 0 
            vB = 0 
            pass_pkt = 0 
            tmp_g = G/2

            if initial_q < 0: 
                tmp_q = G/(2 + G) + 0.01

            for i in range(self.no_slot): 
                ATrans = np.random.rand() < tmp_g 
                BTrans = np.random.rand() < tmp_g 

                RTrans = ((vA > 0) or (vB > 0)) and (np.random.rand() < tmp_q)

                if RTrans == False: 
                    if ATrans == False and BTrans: 
                        vB = vB + 1
                    if BTrans == False and ATrans: 
                        vA = vA + 1 
                else: 
                    if ATrans == False and BTrans == False: 
                        if vA != 0 and vB != 0: 
                            vA = vA - 1
                            vB = vB - 1 
                            pass_pkt = pass_pkt + 2
                        elif vA != 0 and vB == 0: 
                            vA = vA - 1 
                            pass_pkt = pass_pkt + 1 
                        elif vB != 0 and vA == 0: 
                            vB = vB - 1
                            pass_pkt = pass_pkt + 1 
                    elif ATrans == True and BTrans == False: 
                        if vB != 0: 
                            vB = vB - 1
                            pass_pkt = pass_pkt + 1 
                    elif ATrans == False and BTrans == True: 
                        if vA != 0: 
                            vA = vA - 1 
                            pass_pkt = pass_pkt + 1 
                
            thput_sim.append(pass_pkt/self.no_slot)
            thput_ana.append(self.thrput_coding(G, tmp_q))
        # plt.plot(self._g, thput_sim, 'o', self._g, thput_ana, '-')
        # plt.show()
        return thput_sim, thput_ana 

    def coding_plot(self): 

        q_arr = [0.5, 0.9, -1]
        marker_arr = ['^', 'd', 'o']
        legend_arr = []
        for i in range(len(q_arr)): 
            q = q_arr[i]
            thput_sim, thput_ana = self.coding(q)
            plt.plot(self._g, thput_sim, marker_arr[i], self._g, thput_ana, '-')
            if q > 0: 
                legend_arr.append(f'Simulation, q = {q}')
                legend_arr.append(f'Theoretical, q = {q}')
            else: 
                legend_arr.append(f'Simulation, q = G/(2 + G) + 0.01')
                legend_arr.append(f'Theoretical, q = G/(2 + G) + 0.01')
               

        plt.xlabel('Offer Traffic, G = 2g')
        plt.ylabel('Throughput, S')
        plt.title('NC System')
        plt.legend(legend_arr)
        plt.savefig('nc.png')
        # plt.show() 


                    




# if __name__ == '__main': 
SA = SlottedAloha()
SA.coding_plot()
SA.non_coding()
