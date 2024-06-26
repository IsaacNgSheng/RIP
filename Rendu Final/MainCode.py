import json
import csv

#Déclaration des classes
class Commandes:
    def __init__(self, id, temps_qualite, date_envoi_prevue, nombre_unites, date_demande_boite=None, date_envoi=None):
        self.id = id
        self.temps_qualite = temps_qualite
        self.date_envoi_prevue = date_envoi_prevue
        self.nombre_unites = nombre_unites
        self.date_envoi = 0
        self.date_demande_boite = date_demande_boite 
        
class Pile:
    def __init__(self, type_prod):
        self.type_prod = type_prod
        self.h = 0
        self.l = self.type_prod.l   
        
class Boite:
    def __init__(self, types_box, nb):
        self.contenu_boite = []  # liste pour stocker les unités de produits par boîte
        self.type = types_box
        self.commande = None  # Attribut pour associer la commande à laquelle la boîte correspond
        self.piles = []  
        self.nombre_achats_boite = nb  
        self.long_res = self.type.l3
        self.temps = 0  

    def Empiler(self, unite, pile):  # permet de savoir si on peut empiler dans une pile
        valeur = False
        if (unite.produit == pile.type_prod):
            if ((pile.h < unite.produit.nbEmpileMax * unite.produit.h) and (pile.h < self.type.h3)) and self.commande == unite.commande:  # tant que la h de la pile ne dépasse pas la h de la boîte, on peut empiler
                valeur = True
        return valeur

    def RemplirPile(self, unite, p):
        self.contenu_boite.append(unite)
        self.commande = unite.commande  # associe unité à une commande
        p.h += unite.produit.h  # mise à jour pile

    def RemplirNouvellePile(self, unite):  # créer une nouvelle pile
        if (self.long_res - unite.produit.l >= 0):
            self.contenu_boite.append(unite)
            self.commande = unite.commande
            p1 = Pile(unite.produit)
            self.piles.append(p1)
            p1.h += unite.produit.h
            self.long_res -= p1.l

    def Vider(self):
        self.contenu_boite = []
        self.piles = []
        self.commande = None
        self.long_res = self.type.l3

    def EstVide(self): #vérifier si le contenu de la boite est bien vide
        resultat = False
        if (self.commande is None and len(self.piles) == 0 and len(self.contenu_boite) == 0):
            resultat = True
        return resultat

class TypesLignes:
    def __init__(self, id, types_operation, stock_esi, index, dernier=None, temps_setup=None):
        self.id = id
        self.types_operation = types_operation
        self.stock_esi = stock_esi
        self.index = index
        self.dernier = ""
        self.temps_setup = 0

class types_box:
    def __init__(self, id, h, l, prix, nombre_achats_boite=0):
        self.id = id
        self.h3 = h
        self.l3 = l
        self.prixboite = prix
        self.nombre_achats_boite = nombre_achats_boite

class TypesComposants:
    def __init__(self, id, m, temps_s, temps_p, h, l, w=None):
        self.id = id
        self.m = m
        self.temps_s = temps_s
        self.temps_p = temps_p
        self.h = h
        self.l = l
        self.w = w

class ComposantProduit:
    def __init__(self, id_composant, id_type, type_composant, id_ligne, date_debut):
        self.id_composant = id_composant
        self.id_type = id_type
        self.type_composant = type_composant
        self.id_ligne = id_ligne
        self.date_debut = date_debut

class TypesProduits:
    def __init__(self, id, temps_s, temps_assemblage, h, l, w, nbEmpileMax):
        self.id = id
        self.temps_s = temps_s
        self.temps_assemblage = temps_assemblage
        self.h = h
        self.l = l
        self.w = w
        self.nbEmpileMax = nbEmpileMax

class UniteProduite:
    def __init__(self, id_commande, c, p, id_type_produit, index, date_debut, ids_composants=None):
        self.id_commande = id_commande  # W
        self.commande = c
        self.produit = p
        self.id_type_produit = id_type_produit
        self.index = index
        self.date_debut = date_debut
        self.id_boite = None
        self.boite = None
        self.ids_composants = ids_composants

#classe permettant de simuler la production de l'usine
class SimulationUsine:
    def __init__(self, fichier_csv, fichier_json):
        self.type_boite = {}
        self.composants = self.ChargerComposants(fichier_json)
        self.produits = self.ChargerProduits(fichier_json)
        self.commandes = self.ChargerCommandes(fichier_csv)
        self.lignes_production = self.ChargerLignesProduction(fichier_json)
        self.types_de_boites = self.ChargerBoitesStockage(fichier_json)
        self.boites_achetees = []
        self.unites_produites = []
        self.composants_produits = []
        self.boites_utilisees = []
        self.piles = []
        self.dict_boites_commandes = dict()
        self.boites_commandes = {}
        self.eval = 0
        self.indice = 0
        self.liste_unites_produites = []
        self.commandes.sort(key=lambda commande: commande.date_envoi_prevue)

    def ChargerComposants(self, chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            liste_composants = [TypesComposants(tc["id"], tc["m"], tc["s"], tc["t"], tc["h"], tc["l"], tc.get("w")) for tc in data["types_composants"]]
            return liste_composants

    def ChargerProduits(self, chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            liste_types_produits = [TypesProduits(tp["id"], tp["s"], tp["p"], tp["h"], tp["l"], tp["w"], tp["nbEmpileMax"]) for tp in data["types_produits"]]
            return liste_types_produits


    def ChargerCommandes(self, chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            lecteur_csv = csv.reader(fichier, delimiter=' ')

            liste_commandes = []
            for row in lecteur_csv:
                id = row[0]
                temps_qualite = int(row[1])
                date_envoi = int(row[2])

                nombre_de_chaque_produit = []

                for i in range(3, len(row)):
                    nombre_de_chaque_produit.append(int(row[i]))

                une_commande = Commandes(id, temps_qualite, date_envoi, nombre_de_chaque_produit)
                liste_commandes.append(une_commande)
            return liste_commandes

    def ChargerLignesProduction(self, chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            liste_lignes = [TypesLignes(l["id"], l["operation"], l["esi"], index + 1) for index, l in enumerate(data["lignes"])]
            return liste_lignes

    def ChargerBoitesStockage(self, chemin_fichier):
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
            liste_typeBoites = [types_box(tb["id"], tb["h"], tb["l"], tb["prix"]) for tb in data["types_box"]]
            return liste_typeBoites

    def SetEval(self, valeur):
        self.eval = valeur

        
    def lancer_simulation_production(self):
        for commande in self.commandes:
            nb_produits = 0
            i = 0
            for produit in self.produits:
                nombre_a_produire = commande.nombre_unites[i]
                nb_produits += nombre_a_produire
                if nombre_a_produire == 0:
                    i += 1
                    continue

                verre = next((composant for composant in self.composants if composant.m == "verre" and composant.h == produit.h and composant.l == produit.l), None)
                membrane = next((composant for composant in self.composants if composant.m == "membrane" and composant.h == produit.h and composant.l == produit.l), None)
                eva = next((composant for composant in self.composants if composant.m == "eva" and composant.h == produit.h and composant.l == produit.l), None)
                cellules = next((composant for composant in self.composants if produit.w == composant.w), None)

                if not verre or not membrane or not eva or not cellules:
                    print(f"Erreur : Composants manquants pour le type de produit {produit.id} dans la commande {commande.id}. Verre: {verre}, Membrane: {membrane}, EVA: {eva}, Cellules: {cellules}")
                    i += 1
                    continue

                composants_a_produire = [eva, eva, verre, membrane]
                lignes_production = [ligne for ligne in self.lignes_production if ligne.types_operation == "production"]
                lignes_production_pas_pleines = [ligne for ligne in lignes_production if ligne.stock_esi > 0]
                ligne_production_equilibre_charge = max(lignes_production_pas_pleines, key=lambda ligne: ligne.stock_esi)

                lignes_utilisees = [ligne_production_equilibre_charge]

                if ligne_production_equilibre_charge.dernier != cellules.id:
                    ligne_production_equilibre_charge.temps_setup += cellules.temps_s

                # Créer des composants pour chaque unité
                nouveaux_ids_composants = []
                for _ in range(nombre_a_produire):
                    nouveau_composant = ComposantProduit(
                        len(self.composants_produits) + 1,
                        cellules.id,
                        cellules.m,
                        ligne_production_equilibre_charge.index,
                        ligne_production_equilibre_charge.temps_setup
                    )

                    self.composants_produits.append(nouveau_composant)
                    nouveaux_ids_composants.append(nouveau_composant.id_composant)
                    ligne_production_equilibre_charge.temps_setup += cellules.temps_p
                    ligne_production_equilibre_charge.dernier = cellules.id

                ligne_production_equilibre_charge.stock_esi -= nombre_a_produire

                for composant in composants_a_produire:
                    lignes_decoupe = [ligne for ligne in self.lignes_production if ligne.types_operation == "decoupe"]
                    lignes_decoupe_pas_pleines = [ligne for ligne in lignes_decoupe if ligne.stock_esi > 0]
                    ligne_decoupe_equilibre_charge = max(lignes_decoupe_pas_pleines, key=lambda ligne: ligne.stock_esi)
                    lignes_utilisees.append(ligne_decoupe_equilibre_charge)

                    if ligne_decoupe_equilibre_charge.dernier != composant.id:
                        ligne_decoupe_equilibre_charge.temps_setup += composant.temps_s

                    # Créer des composants pour chaque unité
                    for _ in range(nombre_a_produire):
                        nouveau_composant = ComposantProduit(
                            len(self.composants_produits) + 1,
                            composant.id,
                            composant.m,
                            ligne_decoupe_equilibre_charge.index,
                            ligne_decoupe_equilibre_charge.temps_setup
                        )

                        self.composants_produits.append(nouveau_composant)
                        nouveaux_ids_composants.append(nouveau_composant.id_composant)
                        ligne_decoupe_equilibre_charge.temps_setup += composant.temps_p
                        ligne_decoupe_equilibre_charge.dernier = composant.id

                    ligne_decoupe_equilibre_charge.stock_esi -= nombre_a_produire

                ligne_finissant_la_plus_recente = max(lignes_utilisees, key=lambda ligne: ligne.temps_setup)
                composants_pret = ligne_finissant_la_plus_recente.temps_setup
                lignes_assemblage = [ligne for ligne in self.lignes_production if ligne.types_operation == "assemblage"]
                ligne_assemblage_equilibre_charge = min(lignes_assemblage, key=lambda ligne: ligne.temps_setup)
                debut_assemblage = max(composants_pret, ligne_assemblage_equilibre_charge.temps_setup)

                if ligne_assemblage_equilibre_charge.temps_setup < debut_assemblage:
                    ligne_assemblage_equilibre_charge.temps_setup = debut_assemblage

                if ligne_assemblage_equilibre_charge.dernier != produit.id:
                    ligne_assemblage_equilibre_charge.temps_setup += produit.temps_s

                for _ in range(nombre_a_produire):
                    nouvelle_unite = UniteProduite(
                        commande.id,
                        commande,
                        produit,
                        produit.id,
                        ligne_assemblage_equilibre_charge.index,
                        ligne_assemblage_equilibre_charge.temps_setup,
                        [str(nouveaux_ids_composants.pop(0)),
                         str(nouveaux_ids_composants.pop(0)),
                         str(nouveaux_ids_composants.pop(0)),
                         str(nouveaux_ids_composants.pop(0)),
                         str(nouveaux_ids_composants.pop(0))]
                    )

                    self.unites_produites.append(nouvelle_unite)
                    print(f"Commande {commande.id} produit unité de type {produit.id} avec composants {nouvelle_unite.ids_composants}")

                    ligne_assemblage_equilibre_charge.temps_setup += produit.temps_assemblage

                ligne_decoupe_equilibre_charge.dernier = composant.id

                if commande.date_demande_boite is None:
                    commande.date_demande_boite = debut_assemblage + produit.temps_s + produit.temps_assemblage

                i += 1

            commande.date_envoi = commande.date_envoi + ligne_assemblage_equilibre_charge.temps_setup + commande.temps_qualite

            if commande.date_envoi < commande.date_envoi_prevue:
                commande.date_envoi = commande.date_envoi_prevue

            self.eval += nb_produits * 10 * abs(commande.date_envoi - commande.date_envoi_prevue) #j'ai essayer un truc la mais jsp si ça marche

    def acheter_boite(self, type_boite):
        if type_boite.id not in self.type_boite.keys():
            self.type_boite[type_boite.id] = 1
        else:
            self.type_boite[type_boite.id] += 1
        b = Boite(type_boite, self.type_boite[type_boite.id])
        self.boites_utilisees.append(b)
        type_boite.nombre_achats_boite += 1
        return b

    def stockage_unite(self):
        boites_achetees = self.boites_utilisees
        valeur = True
        indice = 0
        eval_ajout = 0

        for unite in self.unites_produites:
            if unite.id_commande not in self.dict_boites_commandes:
                self.dict_boites_commandes[unite.id_commande] = [unite]
            else:
                self.dict_boites_commandes[unite.id_commande].append(unite)

            if unite.id_commande not in self.boites_commandes:
                self.boites_commandes[unite.id_commande] = []

            # Réinitialiser les boîtes si nécessaire
            for elem1 in boites_achetees:
                for elem2 in self.boites_commandes.keys():
                    if elem1 in self.boites_commandes[elem2]:
                        valeur = False
                if valeur:
                    elem1.vider()

        for elem in self.dict_boites_commandes.keys():
            for i in range(len(self.dict_boites_commandes[elem])):
                a = len(self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande])
                for k in range(a):
                    if a != 0:
                        indice = len(self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][k].piles) - 1
                        if self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][k].Empiler(
                                self.dict_boites_commandes[elem][i],
                                self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][-1].piles[
                                    indice]) == True:
                            self.dict_boites_commandes[elem][i].boite = self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][-1]
                            self.dict_boites_commandes[elem][i].id_boite = self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][-1].type.id
                            self.dict_boites_commandes[elem][i].boite.RemplirPile(self.dict_boites_commandes[elem][i],
                                                                            self.dict_boites_commandes[elem][i].boite.piles[indice])
                            self.dict_boites_commandes[elem][i].boite.commande = self.dict_boites_commandes[elem][i].commande
                        else:
                            self.dict_boites_commandes[elem][i].boite = self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][-1]
                            self.dict_boites_commandes[elem][i].id_boite = self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande][-1].type.id
                            self.dict_boites_commandes[elem][i].boite.RemplirNouvellePile(self.dict_boites_commandes[elem][i])
                            self.dict_boites_commandes[elem][i].boite.commande = self.dict_boites_commandes[elem][i].commande

                if len(self.boites_utilisees) == 0 or len(self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande]) == 0:
                    j = 0
                    while self.dict_boites_commandes[elem][i].produit.l > self.types_de_boites[j].l3 and self.dict_boites_commandes[elem][i].produit.h > self.types_de_boites[j].h3:
                        j += 1
                    if j < len(self.types_de_boites):
                        b = self.acheter_boite(self.types_de_boites[j])
                        eval_ajout += self.types_de_boites[j].prixboite
                        self.dict_boites_commandes[elem][i].boite = b
                        self.dict_boites_commandes[elem][i].id_boite = b.type.id
                        b.RemplirNouvellePile(self.dict_boites_commandes[elem][i])
                        self.dict_boites_commandes[elem][i].boite.commande = self.dict_boites_commandes[elem][i].commande
                        self.boites_commandes[self.dict_boites_commandes[elem][i].id_commande].append(b)
        self.eval += eval_ajout

#affichage des résultats trouvés
    def imprimer_resultats(self, nom_fichier):
        commandes = self.commandes
        unites_produites = self.unites_produites
        composants_produits = self.composants_produits
        typeBoites = self.types_de_boites
        eval = self.eval

        with open(nom_fichier, 'w') as fichier:
            fichier.write(f"{eval}\n")

            for boite in typeBoites:
                fichier.write(f"{boite.id} {boite.nombre_achats_boite}\n")

            for commande in commandes:
                print(f"{commande.id} demande de stockage à {commande.date_demande_boite}")
                print(f"{commande.id} a terminé le stockage à {commande.date_envoi}")
                fichier.write(f"{commande.id} {commande.date_envoi}\n")

            for unite_produite in unites_produites:
                fichier.write(f"{unite_produite.id_commande} {unite_produite.id_type_produit} {unite_produite.index} {unite_produite.date_debut} {unite_produite.boite.type.id} {unite_produite.boite.nombre_achats_boite} {' '.join(unite_produite.ids_composants)}\n")

            for composant_produit in composants_produits:
                fichier.write(f"{composant_produit.id_composant} {composant_produit.id_type} {composant_produit.id_ligne} {composant_produit.date_debut}\n")


# Principal
if __name__ == "__main__":
    simulation_usine = SimulationUsine("InstanceB.csv", "instanceB.json")
    simulation_usine.lancer_simulation_production()
    simulation_usine.stockage_unite()
    simulation_usine.imprimer_resultats("instanceB_c.sol")
