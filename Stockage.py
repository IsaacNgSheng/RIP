# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:20:54 2024

@author: Computer
"""
from Box import Box

class Stockage:
    def __init__(self):
        self.boxes = []  # Liste  box disponibles
        self.typeB = {}  # Dictionnaire des types de box par type de produit
        self.box_counter = 0  # Compteur pour identifier les box achetés

    def ajouter_type_box(self, box_type, max_height, max_length, price):
        #Ajoute un type de box disponible dans le stockage
        self.typeB[box_type] = {'max_height': max_height, 'max_length': max_length, 'price': price}

    def acheter_box(self, box_type):
        #Achète un nouveau box et l'ajoute à la liste des box disponibles
        self.box_counter += 1
        box_info = self.typeB[box_type]
        new_box = Box(self.box_counter, box_type, box_info['max_height'], box_info['max_length'], box_info['price'])
        self.boxes.append(new_box)
        return new_box

    def trouver_box_pour_produit(self, typeP):
        #Trouve un box disponible qui peut contenir le produit ou en achète un nouveau 
        for box in self.boxes:
            if box.command_id is None or box.command_id == typeP.command_id:
                if box.can_add_unit(typeP):
                    return box

        # Si aucun box existant ne peut contenir le produit, acheter un nouveau box
        return self.acheter_box(typeP.type_id)

    def stocker_commande(self, commande):
        """ Stocke tous les produits d'une commande dans les box appropriés """
        for product in commande.nb:
            box = self.trouver_box_pour_produit(product)
            box.add_unit(product)
            commande.add_box(box)