import utils 
import numpy as np 
from matplotlib import pyplot as plt 

class NetworkCoding: 
    def __init__(self):
        # self._g = np.arange(0, 1.01, 0.05)
        self._ga = np.array([0, 0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1])
        self._gr = np.array([0, 0.0, 0.3, 0.2, 0.2, 0.2, 0.25, 0.3, 0.35, 0.5, 1])
        self._g = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        self._q = 0.6
        self.no_slots = 100000

    def delay_coding(self, gr, G, q):
        delay1 = 1 if G != 0 else 0 
        delay2 = (q * G * (6 + G) - G*G)/ (2 * gr * q * (2 - G)) if (gr != 0 and G != 2) else 0 
        delay3 = 4/((2 - G) * (q *(2 + G) - G)) if (G!= 2 and G != 0) else 0 
        return (delay1 + delay2 + delay3)
    
    def thrput_coding(self, G, q): 
        S = 2*q*G*(2 - G)/(q*(2 + G)**2 - G**2)
        return S

    def coding(self): 

        throuput_sim = []
        delay_sim = []
        through_ana = []
        delay_ana = []


        for idx in range(len(self._g)):

            # ga = self._g[idx]
            # gr = 0
                        
            ga = self._ga[idx]
            gr = self._gr[idx]
            g = self._g[idx]
            print(f'{idx} - {g}')

            pass_pkt = 0 
            delay_pkt = 0

            A = utils.EndNode('A', ga, gr) 
            B = utils.EndNode('B', ga, gr)
            R = utils.RelayNode(self._q)

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
                            A.enqueue_a_packet(A_pk)
                            B.enqueue_a_packet(B_pk)
                        else:
                            R.enqueue(A_pk, islot)
                    else: 
                        if B_is_send: 
                            R.enqueue(B_pk, islot)

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
                    
                    elif B_is_send and A_is_send == False: # collision between R and A
                        if vB_not_empty: # R sent a coding packet from B and A || a native packet form B 
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_B, islot)
                            pass_pkt = pass_pkt + 1
                        if vA_not_empty: 
                            R.enqueue(pk_from_A, -1)
                        B.enqueue_a_packet(B_pk)
                            
                    elif B_is_send == False and A_is_send == True: 
                        if vA_not_empty: 
                            delay_pkt = delay_pkt + R.get_delay_pkt(pk_from_A, islot)
                            pass_pkt = pass_pkt + 1
                        if vB_not_empty: 
                            R.enqueue(pk_from_B, -1)
                        A.enqueue_a_packet(A_pk)
                    
                    else: 
                        A.enqueue_a_packet(A_pk)
                        B.enqueue_a_packet(B_pk)
                        if vA_not_empty: 
                            R.enqueue(pk_from_A, -1)
                        if vB_not_empty: 
                            R.enqueue(pk_from_B, -1)


            throuput_sim.append(pass_pkt/self.no_slots)
            delay_sim.append(delay_pkt/pass_pkt if pass_pkt > 0 else 0)
            delay_ana.append(self.delay_coding(gr, G=2*g, q=self._q))
            through_ana.append(self.thrput_coding(G=2*g, q=self._q))

            # print(f'passpkt = {pass_pkt}, delay = {delay_pkt}' )

        return throuput_sim, through_ana, delay_sim, delay_ana
    
    def run(self): 
        th_sim, th_ana, delay_sim, delay_ana = self.coding()
        print(delay_ana)
        G = self._g*2 
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        print(G)
        print(th_sim)
        ax1.plot(G, th_ana, '-', label='thput_ana') 
        ax1.plot(G, th_sim, 'o', label='thput_sim')
        ax1.set_xlabel('Offered traffic, G')
        ax1.set_title('Throughput, S (pkts/slot)')
        ax1.legend()
        ax1.grid()

        ax2.plot(G, delay_ana, '-', label='delay_ana') 
        ax2.plot(G, delay_sim, 'o', label='delay_sim')
        ax2.set_xlabel('Offered traffic, G')
        ax2.set_title('Delay, D (slots)')


        ax2.grid()
        ax2.legend()
        # plt.show()
        plt.savefig(f'./th_delay_collsion_{self.no_slots}.png')
        plt.close()

        plt.plot(G, delay_ana, '-', label='delay_ana') 
        plt.plot(G, delay_sim, 'o', label='delay_sim')
        plt.xlabel('Offered traffic, G')
        plt.title('Delay, D (slots)')
        plt.xticks(G)
        plt.grid()
        plt.savefig(f'delay.png')




NC = NetworkCoding()
NC.run()
# print(NC.delay_coding(0.5, 1, 0.6))    