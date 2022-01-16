from curses.ascii import ACK
from email import utils
import utils2 
import numpy as np 
from matplotlib import pyplot as plt 

class NetworkCoding: 
    def __init__(self):
        # self._gr_arr = np.arange(0.1, 1.1, 0.1)
        self._g = np.arange(0, 1.1, 0.1)
        # self._gr_arr = np.array([0.5, 0.6])
        self._gr = 0.5
        self._q = 5
        self._ga = 0.5
        self.no_slots = 10000

    def delay_coding(self, gr, G, q): 
        if gr != 0: 
            delay = 1 + (q * G * (6 + G) - G*G)/ (2 * gr * q * (2 - G)) + 4/((2 - G) * (q *(2 + G) - G))
        else: 
            delay = 0
        return delay 
    
    def thrput_coding(self, G, q): 
        S = 2*q*G*(2 - G)/(q*(2 + G)**2 - G**2)
        return S

    def coding(self): 

        throuput_sim = []
        delay_sim = []
        through_ana = []
        delay_ana = []


        for g in self._g:
            ga = g
            gr = g

            pass_pkt = 0 
            delay_pkt = 0 
            A = utils2.EndNode('A', ga, gr) 
            B = utils2.EndNode('B', ga, gr)
            R = utils2.RelayNode(self._q)

            for islot in range(self.no_slots): 
                # Node A 
                A_is_send, A_pk = A.send_a_packet(islot)

                # Node B 
                B_is_send, B_pk = B.send_a_packet(islot)

                # Node R
                R_is_send, pk_from_A, pk_from_B = R.send_a_packet()
                
                vA_not_empty = pk_from_A.t_in != -1  
                vB_not_empty = pk_from_B.t_in != -1 

                if R_is_send == False: 
                    if A_is_send:  
                        if B_is_send: 
                            A.received_feedback(utils2.FAILED)
                            B.received_feedback(utils2.FAILED)
                        else:
                            R.enqueue(A_pk, islot)
                            A.received_feedback(ACK)
                    else: 
                        if B_is_send: 
                            R.enqueue(B_pk, islot)
                            B.received_feedback(ACK)

                else:
                    if A_is_send == False and B_is_send == False: 
                        if vA_not_empty and vB_not_empty: # R sends a coding packet        
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_A, islot) + R.get_delay_pkt(pk_from_B, islot)
                            pass_pkt = pass_pkt + 2
                        
                        elif vA_not_empty and vB_not_empty == False: # R sends successfully a packet from A to B 
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_A, islot)
                            pass_pkt = pass_pkt + 1

                        elif vB_not_empty and vA_not_empty == False: # R sends successfully a packet from B to A  
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_B, islot)
                            pass_pkt = pass_pkt + 1 
                    
                    elif A_is_send and B_is_send == False: # collision between R and A
                        if vB_not_empty: # R sent a coding packet from B and A || a native packet form B 
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_B, islot)
                            pass_pkt = pass_pkt + 1
                        if vA_not_empty: 
                            R.enqueue_collision(pk_from_A)
                            A.received_feedback(utils2.FAILED)
                            
                    elif A_is_send == False and B_is_send == True: 
                        if vA_not_empty != 0: 
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_A, islot)
                            pass_pkt = pass_pkt + 1
                        if vB_not_empty: 
                            R.enqueue_collision(pk_from_B)
                            B.received_feedback(utils2.FAILED)


            throuput_sim.append(pass_pkt/self.no_slots)
            delay_sim.append(delay_pkt/pass_pkt if pass_pkt > 0 else 0)
            delay_ana.append(self.delay_coding(gr, G=2*g, q=self._q))
            through_ana.append(self.thrput_coding(G=2*g, q=self._q))

            print(f'passpkt = {pass_pkt}, delay = {delay_pkt}' )

        return throuput_sim, through_ana, delay_sim, delay_ana
    
    def run(self): 
        th_sim, th_ana, delay_sim, delay_ana = self.coding()
        print(delay_ana)
        G = self._g*2 
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        ax1.plot(G, th_sim, '-o', label='thput_sim')
        ax1.plot(G, th_ana, '-d', label='thput_ana') 
        ax1.legend()
        ax1.grid()

        ax2.plot(G, delay_sim, '-o', label='delay_sim')
        ax2.plot(G, delay_ana, '-d', label='delay_ana') 

        ax2.grid()
        ax2.legend()
        # plt.show()
        plt.savefig(f'./th_delay_2_{self.no_slots}.png')


NC = NetworkCoding()
NC.run()
print(NC.delay_coding(0.5, 1, 0.6))            