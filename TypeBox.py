# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:31:23 2024

@author: Computer
"""
class TypeBox:
    def __init__(self, id, h, l, price):
        self.id = id  # Identifiant unique du type de produit
        self.h = h  # Htype(t) : Hauteur d'une unité de ce type
        self.l = l  # Ltype(t) : Longueur d'une unité de ce type
        self.price = price

    def get_height(self):
        return self.h

    def get_length(self):
        return self.l
    
    def __str__(self):
        return f"Type de boîte {self.id}: (H: {self.h}, L: {self.l}, Prix: {self.prix})"
    
