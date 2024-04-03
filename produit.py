#!/usr/bin/env python3


class Produit:
    def __init__(self, profondeur:float, hauteur:float, empilage_max:int):
        #vous serez probablement amenés à faire évoluer cette représentation
        self.profondeur = profondeur
        self.hauteur = hauteur
        self.empilage_max = empilage_max

    def get_max_pile(self):
        return self.empilage_max

    def get_dimensions(self):
        #pour cette version on va créer un dictionnaire avec une "profondeur" et une "hauteur"
        dimensions = {"profondeur": self.profondeur,
                      "hauteur": self.hauteur}
        return dimensions

    def __str__(self):
        #renvoie une chaine de caractères
        #NB : vous pouvez utiliser la fonction id() pour clarifier l'affichage
        #https://docs.python.org/3/library/functions.html#id
        return f"{self.get_max_pile()}"

if __name__ == "__main__" :
    p = Produit(120, 115, 8)
    print(p)
