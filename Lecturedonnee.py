import json

class LigneProduction:
    def __init__(self, id, operation, esi):
        self.id = id
        self.operation = operation
        self.esi = esi
    
    def __str__(self):
        return f"Ligne de production {self.id}: {self.operation} (ESI: {self.esi})"

class TypeComposant:
    def __init__(self, id, m, s, t, h, l, w=None):
        self.id = id
        self.m = m
        self.s = s
        self.t = t
        self.h = h
        self.l = l
        self.w = w
    
    def __str__(self):
        return f"Type de composant {self.id}: {self.m} (S: {self.s}, T: {self.t}, H: {self.h}, L: {self.l}, W: {self.w})"

class Composant(TypeComposant):
    def ___init__(self, id, m, s, t, h, l, w=None):
        super().__init__(id, m, s, t, h, l, w=None)
    pass
    
class TypeProduit:
    def __init__(self, id, s, p, h, l, w, nbEmpileMax):
        self.id = id
        self.s = s
        self.p = p
        self.h = h
        self.l = l
        self.w = w
        self.nbEmpileMax = nbEmpileMax
    
    def __str__(self):
        return f"Type de produit {self.id}: (S: {self.s}, P: {self.p}, H: {self.h}, L: {self.l}, W: {self.w}, NbEmpileMax: {self.nbEmpileMax})"

class Produit(TypeProduit):
    def __init__(self, id, s, p, h, l, w, nbEmpileMax):
        super().__init__(self, id, s, p, h, l, w, nbEmpileMax)

class TypeBox:
    def __init__(self, id, h, l, prix):
        self.id = id
        self.h = h
        self.l = l
        self.prix = prix
    
    def __str__(self):
        return f"Type de boîte {self.id}: (H: {self.h}, L: {self.l}, Prix: {self.prix})"

class Box(TypeBox):
    def __init__ (self, id, h, l, prix):
        super().__init__(id, h, l, prix)
        self.listePile = []
    pass

class Commande:
    def __init__(self,id, stockMin, dEnvoiPrevue, nb)
        self.id = id
        self.stockMin = stockMin
        self.dEnvoiPrevue = dEnvoiPrevue
        self.nb = nb
    pass

def lire_fichier_json(nom_fichier):
    with open(nom_fichier, 'r') as f:
        data_str = f.read()  # Lire le fichier en tant que chaîne de caractères
        data = json.loads(data_str)  # Charger la chaîne de caractères en tant que JSON
        lignes = [LigneProduction(l["id"], l["operation"], l["esi"]) for l in data["lignes"]]
        types_composants = [TypeComposant(tc["id"], tc["m"], tc["s"], tc["t"], tc["h"], tc["l"], tc.get("w")) for tc in data["types_composants"]]
        types_produits = [TypeProduit(tp["id"], tp["s"], tp["p"], tp["h"], tp["l"], tp["w"], tp["nbEmpileMax"]) for tp in data["types_produits"]]
        types_box = [TypeBox(tb["id"], tb["h"], tb["l"], tb["prix"]) for tb in data["types_box"]]
    return lignes, types_composants, types_produits, types_box

lignes, types_composants, types_produits, types_box = lire_fichier_json(r"C:\Scolaire\INSA Lyon\2023 2024\RIP\InstanceA.json")

for ligne in types_composants:
    print(ligne)
    