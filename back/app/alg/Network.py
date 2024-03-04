import numpy as np
from pydantic import BaseModel
from typing import Any

class Trans(BaseModel):
    befor: Any
    after: Any

class Node:
    def __init__(self):
        self.trans={}
        self.Object=None
    def add_trans(self,name:str,trans:Trans):
        self.trans[name]=trans

class Network:
    def __init__(self,nodes:list[Node]):
        self.nodes=nodes
        self.A=np.zeros([len(nodes),len(nodes)],dtype=np.int8)
    def gen_network(self,st):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if st(self.nodes[i],self.nodes[j]):
                    self.A[i][j]=1