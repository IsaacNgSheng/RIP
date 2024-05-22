#!/usr/bin/env python3
from produit import Produit

class Pile:
    def __init__(self, p:Produit = None):
        #ici on ne crée la pile que si on a un produit à mettre dedans
        self.Produit = p
        self.nombre = 0

    def nb_items(self):
        #nombre d'éléments dans la pile
        return self.nombre

    def is_complete(self):
        #renvoie vrai si on ne peut plus ajouter d'éléments
        if self.nb_items() >= self.Produit.get_max_pile():
            return True
        else:
            return False

    def empiler(self, p):
        #empile que si on peut rajouter des items
        if self.is_complete() == False:
            self.nombre += 1
            return True
        else:
            return False

    def __str__(self):
        #ce serait bien d'avoir une représentation un peu graphique de la pile
        return f"La pile contient {self.nombre} produits sur {self.Produit}"

if __name__ == "__main__":
    liste_p = []
    liste_p.append(Produit(120, 115, 5))
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    pile = Pile(liste_p[0])
    for i in range(1,len(liste_p)):
        print(f"\nempiler item {i} ?", pile.empiler(liste_p[i]))
        print(pile)
