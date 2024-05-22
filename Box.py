# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:52:31 2024

@author: Computer
"""
from TypeBox import TypeBox 

class Box (TypeBox):
    def __init__(self, typeB, s, p, mh, id, h, l, price, nbEmpileMax):
        super().__init__(id, h, l, price)
        self.s = s  # s(t) : Temps de réglage des machines pour ce type
        self.p = p  # p(t) : Temps de production d'une unité
        self.mh = mh  # nbEmpileMax(t) : Hauteur maximale d'une pile
        self.typeB = typeB  # Type du box
        self.pileL = 0  # Longueur actuelle des piles dans le box
        self.pileH = {}  # Dictionnaire pour suivre la hauteur actuelle des piles par type de produit
        self.command_id = None  # Identifiant de la commande associée au box
        self.nbEmpileMax = nbEmpileMax
    
#get methods

    def get_price(self):
        return self.price

    def is_empty(self):
        return len(self.stacks) == 0
    
#constraints methods
    def can_add_unit(self, typeP):
        """ Vérifie si une unité de ce type peut être ajoutée au box --> contrainst 3 """
        #Dans chaque box et à chaque instant, les produits stockés doivent appartenir à la même commande (4).
        if self.command_id is None:
            return True
        #produit peut il rentrer dans la box en longueur et hauteur
        if self.pileL + typeP.get_length() <= self.max_length:
            return True
        if typeP.id not in self.pileH:
            return True
        return self.pileH[typeP.id] + typeP.get_height() <= self.max_height

    def add_unit(self, typeP):
        """ Ajoute une unité de produit au box """
        if not self.can_add_unit(typeP):
            raise ValueError("Cannot add unit to this box")
        #on associe à la commande son id
        if self.command_id is None:
            self.command_id = typeP.id

        #tu mets ton produit dans la box
        if typeP.id not in self.pileH:
            self.pileH[typeP.id] = 0
            self.stacks.append([])

        for stack in self.stacks:
            if len(stack) < typeP.self.nbEmpileMax and stack[0].id == typeP.id:
                stack.append(typeP)
                self.pileH[typeP.id] += typeP.get_height()
                return

        self.stacks.append([typeP])
        self.pileL += typeP.get_length()
        self.pileH[typeP.id] += typeP.get_height()

    def empty_box(self):
        """ Vide le box """
        self.stacks = []
        self.pileL = 0
        self.pileH = {}
        self.command_id = None
        
