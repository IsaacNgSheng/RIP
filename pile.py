#!/usr/bin/env python3
from produit import Produit

class Pile:
    def __init__(self, p:Produit = None):
        #ici on ne crée la pile que si on a un produit à mettre dedans
        self.Produit = Produit

    def nb_items(self):
        #nombre d'éléments dans la pile
        return self.Produit.get_max_pile()

    def is_complete(self):
        #renvoie vrai si on ne peut plus ajouter d'éléments
        if self.nb_items()

    def empiler(self, p):
        #empile que si on peut rajouter des items
        pass

    def __str__(self):
        #ce serait bien d'avoir une représentation un peu graphique de la pile
        pass

if __name__ == "__main__":
    liste_p = []
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    liste_p.append(Produit(120, 115, 4))
    pile = Pile(liste_p[0])
    for i in range(1,len(liste_p)):
        print(f"\nempiler item {i} ?", pile.empiler(liste_p[i]))
        print(pile)
