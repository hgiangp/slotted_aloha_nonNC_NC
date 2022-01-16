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

    def delay_coding(self, q, gr, G): 
        D = 1 + 3*G/(gr* (2 - G)) + 2 /((2 - G)*(q(1 + G) - G))
        return D

    def non_coding(self): 

        for G in self._g:
            tmp_g = G/2
            pass_pkt = 0
            queue_length = 0
            # print(tmp_g)
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
        plt.grid(True)
        # plt.xlim([0, 2])
        plt.xlabel('Offer Traffic, G = 2g')
        plt.ylabel('Throughput, S')
        plt.title('Non-NC System')
        plt.legend(['Simulation', 'Theoretical'])
        plt.savefig('non_nc.png')
        # plt.show()
        plt.close()
    
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
               
        plt.grid(True)
        # plt.xlim([0, 2])
        plt.xlabel('Offer Traffic, G = 2g')
        plt.ylabel('Throughput, S')
        plt.title('NC System')
        plt.legend(legend_arr)
        plt.savefig('nc.png')
        # plt.show() 
        plt.close()

    def ga_g_relation(self, gr, ga, q):
        vA = 0
        vB = 0
        collisionA = False
        collisionB = False 
        cnt_trans = 0  

        for i in range(self.no_slot): 

            ATrans = np.random.rand() < ga or ( collisionA and np.random.rand() < gr)
            BTrans = np.random.rand() < ga or ( collisionB and np.random.rand() < gr)

            cnt_trans = cnt_trans + ATrans + BTrans

            # RTrans = ((vA > 0)) and (np.random.rand() < q)

            # if RTrans and ATrans: # collision 
            #     collision = True # A retrans in next slot
            # else: 
            #     collision = False # reset colliison 
            #     vA = vA + 1
            RTrans = ((vA > 0) or (vB > 0)) and (np.random.rand() < q)

            if RTrans == False: 
                if ATrans:  
                    if BTrans: 
                        collisionA = True 
                        collisionB = True 
                    else:
                        collisionA = False 
                        vA = vA + 1 
                else: 
                    if BTrans: 
                        collisionB = False 
                        vB = vB + 1
            else:
                if BTrans: 
                    collisionB = True 
                if ATrans: 
                    collisionA = True 

        return (cnt_trans/2)/self.no_slot
    
    def run(self): 

        gr = np.arange(0, 1.1, 0.1)
        ga = np.arange(0, 1.1, 0.1)
        q = 0.6 
        g_arr = []
        legend_arr = []

        fig2, (ax2, ax3) = plt.subplots(nrows=1, ncols=2) # two axes on figureax3.plot(x, -z)
        for ga_idx in ga: 
            g_arr = [] 
            for gr_idx in gr: 
                g = self.ga_g_relation(gr_idx, ga_idx, q)
                g_arr.append(g)
            
            ax2.plot(gr, g_arr, label='{:.1f}'.format(ga_idx))
             
            ax2.set_xlabel('g_r')
            ax2.set_ylabel('g')
            ax2.grid()
            ax2.legend()


        for gr_idx in gr: 
            g_arr = [] 
            for ga_idx in ga: 
                g = self.ga_g_relation(gr_idx, ga_idx, q)
                g_arr.append(g)
             
            ax3.plot(ga, g_arr, label='{:.1f}'.format(gr_idx))
             
            ax3.set_xlabel('g_a')
            ax3.set_ylabel('g')
            ax3.grid()
            ax3.legend()



        plt.savefig(f'./ga_gr/gr_g_relation.png')

    def run2(self):
        gr = np.arange(0, 1.1, 0.1)
        ga = np.arange(0, 1.1, 0.1)
        q = 0.6
        g_arr = []

        for ga_idx in ga: 
            g_arr = [] 
            for gr_idx in gr: 
                g = self.ga_g_relation(gr_idx, ga_idx, q)
                g_arr.append(g)
            
            plt.plot(gr, g_arr, '-o', label='{:.1f}'.format(ga_idx))
             
            plt.xlabel('g_r')
            plt.ylabel('g')
            plt.yticks(np.arange(0, 1.1, step=0.1))
            plt.grid()
            plt.legend()
            plt.savefig(f'./ga_gr/gr_g_collision_{q}.png')
        

            # plt.show()




# if __name__ == '__main': 
SA = SlottedAloha()
# SA.non_coding()
# SA.coding_plot()
# SA.run()
SA.run2()
# print(np.arange(0, 1.1, step=0.1))
