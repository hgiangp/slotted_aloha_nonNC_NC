from collections import deque
import numpy as np

ACK = 1
FAILED = 2

BACKLOGGED_MODE = 1
NORMAL_MODE = 2
class Packet: 
    def __init__(self, src, t_in): 
        self.src = src 
        self.t_in = t_in 
        self.t_out = 0
        self.N_T = 0
    
    def set_tout(self, t_out): 
        self.t_out = t_out

    def get_delay(self): 
        return (self.t_out - self.t_in + 1)
    
    def is_sent(self): 
        self.N_T = self.N_T + 1
    
    def set_tin_R(self, t_in): 
        self.t_in = t_in 
    
    def get_src(self):
        return self.src 


class EndNode: 
    def __init__(self, name, g_a, g_r): 
        self.qnode = deque()
        self.ga = g_a 
        self.gr = g_r 
        self.name = name
        self.mode = BACKLOGGED_MODE
        self.tmp_pk = Packet(self.name, -1)

    def set_mode(self, mode): 
        self.mode = mode
    

    def send_a_packet(self, id): 
        is_new_pkt = np.random.rand() < self.ga 
        if is_new_pkt:
            is_send = True 
            self.set_mode(NORMAL_MODE)
            self.tmp_pk = Packet(self.name, id)
        else:
            self.set_mode(BACKLOGGED_MODE) 
            is_send = len(self.qnode) > 0 and np.random.rand() < self.gr
            self.tmp_pk = self.qnode[0] if is_send else Packet(self.name, -1)
            
        return is_send, self.tmp_pk 
    
    def received_feedback(self, fb):
        if fb == ACK: 
            self.qnode.pop()
        else: 
            if self.mode == NORMAL_MODE: 
                self.qnode.append(self.tmp_pk)
                self.set_mode(BACKLOGGED_MODE)
    

class RelayNode: 
    def __init__(self, q): 
        self.vA = deque()
        self.vB = deque()
        self.q = q 
    
    def enqueue(self, pk, t_in): 
        if t_in != -1: 
            pk.set_tin_R(t_in) # set time entering the relay node R

        if pk.get_src() == 'A': 
            self.vA.append(pk)
        else: 
            self.vB.append(pk)
    
    def enqueue_collision(self, pk): 
        if pk.get_src() == 'A': 
            self.vA.appendleft(pk)
        else: 
            self.vB.appendleft(pk)

    def get_delay_pkt(self, pk, t_out): 
        delay = pk.N_T + (t_out - pk.t_in + 1) # ( # trans + retrans from end node ) + ( time in R's buffer) 
        return delay

    def send_a_packet(self): 
        size_vA = len(self.vA) 
        size_vB = len(self.vB)
        is_send = (size_vA > 0 or size_vB > 0) and (np.random.rand() < self.q)

        pk_from_A = Packet('R', -1)
        pk_from_B = Packet('R', -1)
        
        if is_send: 
            pk_from_A = self.vA.pop() if size_vA > 0 else pk_from_A 
            pk_from_B = self.vB.pop() if size_vB > 0 else pk_from_B

        return is_send, pk_from_A, pk_from_B


def run(): 
    A = EndNode('A', 0.5, 0.5)

run()