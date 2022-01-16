from queue import Queue 
import numpy as np 
class Packet: 
    def __init__(self, src, t_in): 
        self.src = src 
        self.t_in = t_in 
        self.t_out = 0
        self.N_T = 0
    
    def set_tout(self, t_out): 
        self.t_out = t_out
    
    def is_sent(self): 
        self.N_T = self.N_T + 1
    
    def set_tin_R(self, t_in): 
        self.t_in = t_in 
    
    def get_src(self):
        return self.src 


class EndNode: 
    def __init__(self, name, g_a, g_r): 
        self.qnode = Queue()
        self.ga = g_a 
        self.gr = g_r 
        self.name = name
        self.mode = 'B'
    
    def get_queue_length(self): 
        return self.qnode.qsize()
    

    def send_a_packet(self, id): 
        is_new_pkt = np.random.rand() < self.ga 
        is_send = is_new_pkt or (self.get_queue_length() > 0 and np.random.rand() < self.gr)
        
        A_pk = Packet(self.name, -1)
        if is_send: 
            A_pk = Packet(self.name, id) if is_new_pkt else self.qnode.get()
            A_pk.is_sent() # remember the number of trans and retransmissions

        # print(f'iter = {id} src = {A_pk.src} N_T = {A_pk.N_T} t_in = {A_pk.t_in}')
        return is_send, A_pk 
    
    def enqueue_a_packet(self, packet): # collision happened 
        self.qnode.put(packet)
    

class RelayNode: 
    def __init__(self, q): 
        self.vA = Queue()
        self.vB = Queue()
        self.q = q 
    
    def enqueue(self, pk, t_in): 
        if t_in != -1: 
            pk.set_tin_R(t_in) # set time entering the relay node R

        if pk.get_src() == 'A': 
            self.vA.put(pk)
        else: 
            self.vB.put(pk)
        

    def get_delay_pkt(self, pk, t_out): 
        delay = pk.N_T + (t_out - pk.t_in + 1) # ( # trans + retrans from end node ) + ( time in R's buffer) 
        # print(f'N_T = {pk.N_T} t_in = {pk.t_in} t_out = {t_out} delay = {delay}')
        return delay

    def send_a_packet(self): 
        size_vA = self.vA.qsize() 
        size_vB = self.vB.qsize()
        is_send = (size_vA > 0 or size_vB > 0) and (np.random.rand() < self.q)

        pk_from_A = Packet('R', -1)
        pk_from_B = Packet('R', -1)
        
        if is_send: 
            pk_from_A = self.vA.get() if size_vA > 0 else pk_from_A 
            pk_from_B = self.vB.get() if size_vB > 0 else pk_from_B
        
        # print(f'src = {pk_from_A.src} N_T = {pk_from_A.N_T} t_in = {pk_from_A.t_in} Relay node')
        # print(f'src = {pk_from_B.src} N_T = {pk_from_B.N_T} t_in = {pk_from_B.t_in} Relay node')
        

        return is_send, pk_from_A, pk_from_B


def run(): 
    A = EndNode('A', 0.5, 0.5)

# run()