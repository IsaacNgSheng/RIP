import TypeProduit
import TypeCommande
import TypeComposant
import Lecturedonnee

class Lignes_de_Production:
    def __init__(self, id:str, operation:str, esi:int, current_storage=0):
        self.id = id
        self.operation = operation
        self.esi = esi
        self.current_storage = current_storage
        self.composant = None
        self.produit = 0
        self.current_time = 0
        self.materials = {"verre": 0, "membrane": 0, "eva": 0, "cell_A" : 0, "cell_B" : 0}

    def __str__(self):
        return f"Ligne de production {self.id}: {self.operation} (ESI: {self.esi})"

    def fabrication(self, composant:TypeComposant):
        if self.operation == "fabrication":
            self.composant = composant
            lignes, types_composants, types_produits, types_box = Lecturedonnee.lire_fichier_json(r"..\Proj\InstanceA.json")
            id_01, id_02, id_03 = types_composants["id"].get("01"), types_composants["id"].get("02"), types_composants["id"].get("03")


            #Setup time
            self.current_time += self.composant.s
            print(f"Waited {self.composant.s}time to adjust machines, current time: {self.current_time}")

            #Production time
            self.current_time += self.composant.t
            print(f"Spent {self.composant.t}time to produce each unit, current time: {self.current_time}")

        else:
            print("Operation is not Fabrication")
            return False

    def decoupe(self, composant:TypeComposant):
        if self.operation == "decoupe":
            self.composant = composant

            #Setup time
            self.current_time += self.composant.s
            print(f"Waited {self.composant.s}time to adjust machines, current time: {self.current_time}")

            #Production time
            self.current_time += self.composant.t
            print(f"Spent {self.composant.t}time to produce each unit, current time: {self.current_time}")

        else:
            print("Operation is not Decoupe")
            return False

    def assemblage(self, produit:TypeProduit):
        if self.operation == "assemblage":
            self.produit = produit
            
            PA = TypeCommande.get().nb[0]
            PB = TypeCommande.get().nb[1]

            while PA > 0:
                self.materials["verre"] += 1
                self.materials["membrane"] += 1
                self.materials["eva"] += 2
                self.materials["cell_A"] += 1
                PA -= 1

            while PB > 0:
                self.materials["verre"] += 1
                self.materials["membrane"] += 1
                self.materials["eva"] += 2
                self.materials["cell_B"] += 1
                PB -= 1

        else:
            print("Operation is not Assemblage")
            return False