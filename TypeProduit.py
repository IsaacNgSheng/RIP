class TypeProduit():
    def __init__(self, id:str, s:int, p=int, h_prod=int, l_prod=int, w_prod=int, nbEmpileMax=int):
        #id = identifier; s = setup time; p = assembly time; h_prod = height, l_prod = length, 
        #w_prod = width; nbEmpileMax = maximum number of items;
        #super().__init__(id, s, p, h_prod, l_prod, w_prod, nbEmpileMax)
        self.id = id
        self.s = s
        self.p = p
        self.h_prod = h_prod
        self.l_prod = l_prod
        self.w_prod = w_prod
        self.nbEmpileMax = nbEmpileMax
        
    def __str__(self):
        return f"Type de composant {self.id}: {self.m} (S: {self.s}, T: {self.t}, H: {self.h_prod}, L: {self.l_prod}, W: {self.w_prod}, nbEmpileMax: {self.nbEmpileMax})"

