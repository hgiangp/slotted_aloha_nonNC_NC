import queue

class Packet: 
    def __init__(self, src, t_in): 
        self.src = src 
        self.t_in = t_in 
        self.t_out = 0 
    
    def t_out(self, t_out): 
        self.t_out = t_out
    

class EndNode: 
    def __init__(self): 
        self.q = queue.Queue()

class RelayNode: 
    def __init__(self): 
        self.vA = queue.Queue()
        self.vB = queue.Queue()
    

def run(): 
    pk = Packet('A', 3)
    R = RelayNode() 
    print('running')
    R.vA.put(pk)
    print('run')
    pk2 = R.vA.get()
    print(f'pk2 src = {pk2.src} t_out = {pk2.t_out} t_in = {pk2.t_in}' )

run()