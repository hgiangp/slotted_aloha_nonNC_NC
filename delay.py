import utils 
import numpy as np 
import matplotlib.pyplot as plt 

class NetworkCoding: 
    def __init__(self):
        self._gr_arr = np.arange(0, 1.1, 0.1)
        self._gr = 0.5
        self._q = 0.6
        self._ga = 0.5
        self.no_slots = 50000

        

    def coding(self): 

        throuput_sim = []
        delay_sim = []

        for gr in self._gr_arr:
            
            pass_pkt = 0 
            delay_pkt = 0 
            A = utils.EndNode() 
            B = utils.EndNode()
            R = utils.RelayNode()

            for iter in range(self.no_slots): 
                # Node A 
                A_is_newPk_arrived = np.random.rand() > self._ga
                A_is_send = A_is_newPk_arrived or (A.qnode.qsize() > 0 and np.random.rand() > gr) 
                
                if A_is_send: 
                    A_pk = utils.Packet('A', iter) if A_is_newPk_arrived else A.qnode.get() 
                
                # Node B 
                B_is_newPk_arrived = np.random.rand() > self._ga 
                B_is_send = B_is_newPk_arrived or (B.qnode.qsize() > 0 and np.random.rand() > gr) 
                
                if B_is_send: 
                    B_pk = utils.Packet('B', iter) if B_is_newPk_arrived else B.qnode.get()

                # Node R
                R_is_send = (R.vA.qsize() > 0 or R.vB.qsize() > 0) and (np.random.rand() > self._q)

                if R_is_send == False: 
                    if A_is_send:  
                        if B_is_send: 
                            A.qnode.put(A_pk)
                            B.qnode.put(B_pk)
                        else: 
                            R.vA.put(A_pk)
                    else: 
                        if B_is_send: 
                            R.vB.put(B_pk)
                else:
                    vA_size = R.vA.qsize()
                    vB_size = R.vB.qsize()

                    if A_is_send == False and B_is_send == False: 
                        if vA_size != 0 and vB_size != 0: # R sends a coding packet 
                            pk_from_A = R.vA.get() 
                            pk_from_B = R.vB.get()
                            delay_pkt = delay_pkt + (iter - pk_from_A.t_in) + (iter - pk_from_B.t_in)
                            pass_pkt = pass_pkt + 2 
                        
                        elif vA_size != 0 and vB_size == 0: # R sends successfully a packet from A to B 
                            pk_from_A = R.vA.get()
                            pass_pkt = pass_pkt + 1 
                            delay_pkt = delay_pkt + (iter - pk_from_A.t_in) 

                        elif vB_size != 0 and vA_size == 0: # R sends successfully a packet from B to A  
                            pk_from_B = R.vB.get()
                            pass_pkt = pass_pkt + 1 
                            delay_pkt = delay_pkt + (iter - pk_from_B.t_in)
                    
                    elif A_is_send and B_is_send == False: # collision between R and A
                        if vB_size != 0: # R sent a coding packet from B and A || a native packet form B 
                            pk_from_B = R.vB.get()
                            pass_pkt = pass_pkt + 1 
                            delay_pkt = delay_pkt + (iter - pk_from_B.t_in)

                    elif A_is_send == False and B_is_send == True: 
                        if vA_size != 0: 
                            pk_from_A = R.vA.get() 
                            delay_pkt = delay_pkt + (iter - pk_from_A.t_in)
                            pass_pkt = pass_pkt + 1

            throuput_sim.append(pass_pkt/self.no_slots)
            delay_sim.append(delay_pkt/pass_pkt if pass_pkt > 0 else 0)

        return throuput_sim, delay_sim
    
    def run(self): 
        th_sim, delay_sim = self.coding()
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        ax1.plot(self._gr_arr, th_sim) 
        ax2.plot(self._gr_arr, delay_sim)
        plt.show()

NC = NetworkCoding()
NC.run()



                
            






                 

            
            
            

            