import json
import csv
from datetime import datetime, timedelta

class Produit:
    def __init__(self, profondeur, hauteur, empilage_max):
        self.profondeur = profondeur
        self.hauteur = hauteur
        self.empilage_max = empilage_max

    def get_max_pile(self):
        return self.empilage_max

    def get_dimensions(self):
        return {"profondeur": self.profondeur, "hauteur": self.hauteur}

    def __str__(self):
        return f"Produit(profondeur={self.profondeur}, hauteur={self.hauteur}, empilage_max={self.empilage_max})"

class Pile:
    def __init__(self, p=None):
        self.produit = p
        self.nombre = 0

    def nb_items(self):
        return self.nombre

    def is_complete(self):
        return self.nb_items() >= self.produit.get_max_pile()

    def empiler(self, p):
        if not self.is_complete():
            self.nombre += 1
            return True
        else:
            return False

    def __str__(self):
        return f"Pile(nombre={self.nombre}, produit={self.produit})"

class LigneProduction:
    def __init__(self, id, operation, esi):
        self.id = id
        self.operation = operation
        self.esi = esi

    def __str__(self):
        return f"LigneProduction(id={self.id}, operation={self.operation}, esi={self.esi})"

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
        return f"TypeComposant(id={self.id}, m={self.m}, s={self.s}, t={self.t}, h={self.h}, l={self.l}, w={self.w})"

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
        return f"TypeProduit(id={self.id}, s={self.s}, p={self.p}, h={self.h}, l={self.l}, w={self.w}, nbEmpileMax={self.nbEmpileMax})"

class TypeCommande:
    def __init__(self, id, stockMin, dEnvoiPrevue, nb):
        self.id = id
        self.stockMin = stockMin
        self.dEnvoiPrevue = dEnvoiPrevue
        self.nb = list(map(int, nb))

    def __str__(self):
        return f"TypeCommande(id={self.id}, stockMin={self.stockMin}, dEnvoiPrevue={self.dEnvoiPrevue}, nb={self.nb})"

class TypeBox:
    def __init__(self, id, h, l, prix):
        self.id = id
        self.h = h
        self.l = l
        self.prix = prix

    def __str__(self):
        return f"TypeBox(id={self.id}, h={self.h}, l={self.l}, prix={self.prix})"

class Stockage:
    def __init__(self):
        self.types_box = {}
        self.boxes = []
        self.nb_total_achetes = 0  

    def ajouter_type_box(self, id, h, l, prix):
        self.types_box[id] = {"h": h, "l": l, "prix": prix, "nb_achetes": 0}

    def acheter_box(self, id, nb_achetes):
        if id in self.types_box:
            for i in range(nb_achetes):
                self.types_box[id]["nb_achetes"] += 1
                self.boxes.append({"id": id, "num": self.types_box[id]["nb_achetes"]})
                self.nb_total_achetes += nb_achetes 

    def __str__(self):
        return f"Stockage(types_box={self.types_box}, boxes={self.boxes})"

class Box(TypeBox):
    def __init__(self, typeB, s, p, mh, id, h, l, prix, nbEmpileMax):
        super().__init__(id, h, l, prix)
        self.s = s
        self.p = p
        self.mh = mh
        self.typeB = typeB
        self.pileL = 0
        self.pileH = {}
        self.command_id = None
        self.nbEmpileMax = nbEmpileMax
        self.pile = []

    def __str__(self):
        return f"Box(typeB={self.typeB}, s={self.s}, p={self.p}, mh={self.mh}, id={self.id}, h={self.h}, l={self.l}, prix={self.prix}, nbEmpileMax={self.nbEmpileMax}, pileL={self.pileL}, pileH={self.pileH}, command_id={self.command_id})"

    def get_price(self):
        return self.prix

    def is_empty(self):
        return len(self.pile) == 0

    def can_add_unit(self, typeP):
        if self.command_id is None:
            return True
        if self.pileL + typeP.l <= self.l:
            return True
        if typeP.id not in self.pileH:
            return True
        return self.pileH[typeP.id] + typeP.h <= self.h

    def add_unit(self, typeP):
        if not self.can_add_unit(typeP):
            raise ValueError("Cannot add unit to this box")
        if self.command_id is None:
            self.command_id = typeP.id

        if typeP.id not in self.pileH:
            self.pileH[typeP.id] = 0
            self.pile.append([])

        for p in self.pile:
            if len(p) < self.nbEmpileMax and (not p or p[0].id == typeP.id):
                p.append(typeP)
                self.pileH[typeP.id] += typeP.h
                return

        self.pile.append([typeP])
        self.pileL += typeP.l
        self.pileH[typeP.id] += typeP.h

    def empty_box(self):
        self.pile = []
        self.pileL = 0
        self.pileH = {}
        self.command_id = None

def lire_json(fichier):
    with open(fichier, 'r') as f:
        return json.load(f)

def lire_csv(fichier):
    with open(fichier, 'r') as f:
        reader = csv.reader(f)
        return [row for row in reader]

def obtenir_identifiants_composants(composants):
    # Dictionnaire pour stocker les identifiants des composants
    identifiants = {
        "cellules": None,
        "eva": None,
        "verre": None,
        "membrane": None
    }

    # Parcourir la liste des composants pour trouver leurs identifiants
    for composant in composants:
        if composant.m == "cellules" and identifiants["cellules"] is None:
            identifiants["cellules"] = composant.id
        elif composant.m == "verre" and identifiants["verre"] is None:
            identifiants["verre"] = composant.id
        elif composant.m == "membrane" and identifiants["membrane"] is None:
            identifiants["membrane"] = composant.id
        elif composant.m == "eva" and identifiants["eva"] is None:
            identifiants["eva"] = composant.id

    return identifiants

def main():
    instanceA = lire_json('../RIP/instanceA.json')
    csv_file = 'InstanceA.csv'

    # Creation des objets a partir des donnees JSON
    lignes = [LigneProduction(**ligne) for ligne in instanceA['lignes']]
    composants = [TypeComposant(**composant) for composant in instanceA['types_composants']]
    produits = [TypeProduit(**produit) for produit in instanceA['types_produits']]
    types_box = [TypeBox(**box) for box in instanceA['types_box']]
    commandes = []


    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        for row in csv_reader:
            if row:
                nb = [row[3], row[4]]
                try:
                    dEnvoiPrevue = row[2]
                    commandes.append(TypeCommande(row[0], row[1], dEnvoiPrevue, nb))
                except ValueError:
                    continue
                
    # Obtenir les identifiants des composants en appelant la fonction
    identifiants_composants = obtenir_identifiants_composants(composants)
    
    stockage = Stockage()
    for box in types_box:
        stockage.ajouter_type_box(box.id, box.h, box.l, box.prix)
    # Exemple d'utilisation
    lignes_production = [
        LigneProduction(1, "fabrication", 50),
        LigneProduction(2, "decoupe", 60),
        LigneProduction(3, "assemblage", 70)
    ]

    # Calcul de l'évaluation de la solution
    eval_solution = 0

       # Ajout du coût des boxes achetées
    for box_id, box_info in stockage.types_box.items():
        #nb_achetes = box_info["nb_achetes"] 
        #PROBLEME nb_achetes est toujours à 0, pour avoir une coherence pour la suite on fixe nb_achetes
        nb_achetes = 1
        eval_solution += int(box_info["prix"]) * nb_achetes  

    # Acheter les boîtes en utilisant la valeur capturée ci-dessus
    for box_id, box_info in stockage.types_box.items():
        nb_achetes = 1
        stockage.acheter_box(box_id, nb_achetes)


    # Dictionnaire pour stocker les dates d'envoi réelles de chaque commande
    dates_dEnvoi = {}

    for commande in commandes:
        date_envoi = "2995"  # PB a changer et a calculer (date à laquelle on a vide tous les box de la commande)
        dates_dEnvoi[commande.id] = date_envoi

    # Ajout de la pénalité pour les délais des commandes
    for commande in commandes:
        nb_produits = sum(commande.nb)  # Nombre total de produits pour la commande
        dEnvoi = dates_dEnvoi.get(commande.id)
        if dEnvoi:
            # Calculer la différence en jours
            days_difference = abs(int(dEnvoi) - int(commande.dEnvoiPrevue))
            eval_solution += nb_produits * 10 * days_difference

    # Ecrire les résultats dans le fichier de sortie
    total_time = 0
    output_file = '../RIP/instanceA.sol'
    with open(output_file, 'w') as file:
        file.write(f"Evaluation solution = {eval_solution}\n")
        for box_id, box_info in stockage.types_box.items():
            file.write(f"BOX = {box_id} et nombre de box achetés = {box_info['nb_achetes']}\n")
        for commande in commandes:
            file.write(f"COMMANDE = {commande.id} et date d'envoie = {dates_dEnvoi[commande.id]}\n")

        # Simulation
        current_box_index = 0
        current_ligne_index = 0

        # Vérification si nombre de box achete est nul
        if stockage.boxes:
            for commande in commandes:
                for idx, nb in enumerate(commande.nb):
                    for _ in range(nb):
                        id_commande = commande.id
                        id_type = types_box[idx].id
                        date_debut_production = "3000"
                        
                        # Vérifier que current_box_index ne dépasse pas les limites de stockage.boxes
                        if current_box_index < len(stockage.boxes):
                            id_box = stockage.boxes[current_box_index]["id"]
                            num_box = stockage.boxes[current_box_index]["num"]
                            
                            # Vérifier que current_ligne_index ne dépasse pas les limites de lignes_production
                            num_ligne = lignes_production[current_ligne_index].id if current_ligne_index < len(lignes_production) else None
                            
                            # Identifiants des composants extraits
                            cellules_id = identifiants_composants["cellules"]
                            eva_id = identifiants_composants["eva"]
                            verre_id = identifiants_composants["verre"]
                            membrane_id = identifiants_composants["membrane"]
                            
                            # Écrire les informations dans le fichier (a savoir, on a fixe pour les box nb_achete = 1)
                            file.write(f" Id commande = {id_commande} Type = {id_type} Num ligne = {num_ligne} Date debut prod = {date_debut_production} Box id = {id_box} Num box = {num_box} Composants = {cellules_id} {eva_id} {eva_id} {verre_id} {membrane_id}\n")
                            
                            # Passer à la box suivante
                            current_box_index = (current_box_index + 1) % len(stockage.boxes)
                        
                            # Passer à la ligne suivante
                            current_ligne_index = (current_ligne_index + 1) % len(lignes_production)
        else:
            print("Erreur: Aucune box disponible dans stockage.boxes.")

        for composant in composants:
            num_ligne = lignes_production[current_ligne_index].id if current_ligne_index < len(lignes_production) else None
            file.write(f"Id = {composant.id} Type = {composant.m} Num ligne = {num_ligne}\n ") 
            #ligne qui l'a produite
            file.write(f"Date envoi prevue: {datetime.now() + timedelta(minutes=total_time - (composant.s + composant.t))}\n")
            current_ligne_index = (current_ligne_index + 1) % len(lignes_production)
                                
                                
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
