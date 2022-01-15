from collections import deque
import numpy as np 
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
    

    def send_a_packet(self, id): 
        is_new_pkt = np.random.rand() < self.ga 
        is_send = is_new_pkt or (len(self.qnode) > 0 and np.random.rand() < self.gr)
        
        A_pk = Packet(self.name, -1)
        if is_send: 
            A_pk = Packet(self.name, id) if is_new_pkt else self.qnode.pop()
            A_pk.is_sent() # remember the number of trans and retransmissions

        return is_send, A_pk 
    
    def enqueue_a_packet(self, packet): # collision happened 
        self.qnode.appendleft(packet)
    

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
    is_send, pk = A.send_a_packet(1)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')
    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(2)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')
    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(3)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')
    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(4)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(5)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(6)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(7)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(8)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(9)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(10)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')

    A.enqueue_a_packet(pk)
    is_send, pk = A.send_a_packet(11)
    print(f'issend = {is_send} pkinfo = {pk.t_in}-{pk.N_T}')



run()