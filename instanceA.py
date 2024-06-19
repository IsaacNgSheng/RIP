import json
import csv

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
    def __init__(self, typeprod):
        self.typeprod = typeprod
        self.hauteur = 0
        self.longueur = self.typeprod.l

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
    def __init__(self, id, operation, esi, index, dernier=None, set_time=None):
        self.id = id
        self.operation = operation
        self.esi = esi
        self.index = index
        self.dernier = ""
        self.set_time = 0

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

class Commandes:
    def __init__(self, id, tps_qualite, dEnvoiPrevue, quantite, ddemande_box=None, date_envoi=None):
        self.id = id
        self.tps_qualite = tps_qualite
        self.dEnvoiPrevue = dEnvoiPrevue
        self.quantite = quantite
        self.date_envoi = 0
        self.ddemande_box = ddemande_box #si besoin de box, achat d'un box dont on cherchera la date de demande du box

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

class produitcompo: 
    def __init__(self, idcomposant, idtype, type_composant, idligne, ddebut):
        self.idcomposant = idcomposant
        self.idtype = idtype
        self.type_composant = type_composant
        self.idligne = idligne
        self.ddebut = ddebut  

class prod_unitaire: 
    def __init__(self, idcommande, c, p, idTypeProduit, index, ddebut, idcomposant =None):
        self.idcommande = idcommande #W
        self.commande = c
        self.produit = p
        self.idTypeProduit = idTypeProduit
        self.index = index
        self.ddebut = ddebut
        self.idbox = None
        self.box = None
        self.idcomposant = idcomposant 

class TypeBox:
    def __init__(self, id, h, l, prix, nb_achatbox = 0):
        self.id = id
        self.h = h
        self.l = l
        self.prix = prix
        self.nb_achatbox = nb_achatbox

    def __str__(self):
        return f"TypeBox(id={self.id}, h={self.h}, l={self.l}, prix={self.prix})"

class TypesLigne:
    def __init__(self, identifiant, types_operation, stock_esi, index, dernier=None, set_time=None):
        self.identifiant = identifiant
        self.types_operation = types_operation
        self.stock_esi = stock_esi
        self.index = index
        self.dernier = ""
        self.set_time = 0

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

    def dEnvoie(dEnvoiPrevue, ligne_product:TypesLigne):
        assem_time = ligne_product.assemblage()
        if assem_time < dEnvoiPrevue:
            return dEnvoiPrevue
        else :
            return ligne_product
        
    def __str__(self):
        return f"Stockage(types_box={self.types_box}, boxes={self.boxes})"

    def __init__(self, types_box, nb):
        self.contenu_box = []  # liste pour stocker les unites de produits par box
        self.type = types_box
        self.commande = None  # Attribut pour associer la commande à laquelle le box correspond
        self.piles = [] # liste des piles
        self.nombre_achats_box = nb  # Attribut pour suivre le nombre de box achetés de ce type
        self.long_res = self.type.l
        self.time = 0 # i added a new attribute

    def empiler(self, unite, pile) : # permet de savoir si on peut empiler dans une pile
        value = False
        if (unite.produit == pile.typeprod):
            if ((pile.hauteur<unite.produit.nbEmpileMax*unite.produit.h) and (pile.hauteur < self.type.h)) and    self.commande==unite.commande: # tant que la hauteur de la pile ne dépasse pas la hauteur du box, on peut empiler
                value = True
        return value

    def remplirPile(self,unite,p) :  
        self.contenu_box.append(unite) 
        self.commande=unite.commande #associe unité à une commande 
        p.hauteur += unite.produit.h #mise à jour pile
                
    def remplir_nouvelle_pile(self,unite) : # créer une nouvelle pile
        if (self.long_res - unite.produit.l >= 0) : 
            self.contenu_box.append(unite)
            self.commande=unite.commande
            p1 = Pile(unite.produit)
            self.piles.append(p1)
            p1.hauteur += unite.produit.h
            self.long_res -= p1.longueur
        
        
    def vider(self) :
        self.contenu_box = []
        self.piles = []
        self.commande = None
        self.long_res = self.type.l
        
    def est_vide(self) :
        value = False
        if (self.commande == None and len(self.piles) == 0 and len(self.contenu_box) == 0) :
            value = True
        return value

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

#check
class composant_produit: 
    def __init__(self, identifiantComposant, identifiantType, type_composant, identifiant_ligne, date_debut):
        self.identifiantComposant = identifiantComposant
        self.identifiantType = identifiantType
        self.type_composant = type_composant
        self.identifiant_ligne = identifiant_ligne
        self.ddebut = date_debut  

class commandes:
    def __init__(self, identifiant, temps_qualite, date_envoiPrevue, nombre_unite, date_demande_box=None, date_envoi=None):
        self.identifiant = identifiant
        self.temps_qualite = temps_qualite
        self.date_envoiPrevue = date_envoiPrevue
        self.nombre_unite = nombre_unite
        self.date_envoi = 0
        self.date_demande_box = date_demande_box#W+
              
class types_lignes:
    def __init__(self, identifiant, types_operation, stock_esi, index, dernier=None, set_time=None):
        self.identifiant = identifiant
        self.types_operation = types_operation
        self.stock_esi = stock_esi
        self.index = index
        self.dernier = ""
        self.set_time = 0
    
class types_box:
    def __init__(self, id, hauteur, longueur,prix, nombre_achats_box=0):
        self.id = id
        self.h3 = hauteur
        self.l3 = longueur
        self.prixbox=prix
        self.nombre_achats_box = nombre_achats_box
        
class Pile :
    def __init__(self,type_prod):
        self.type_prod = type_prod
        self.hauteur = 0 
        self.longueur = self.type_prod.l
    
class box:
    def __init__(self, types_box, nb):
        self.contenu_box = []  # liste pour stocker les unites de produits par box
        self.type = types_box
        self.commande = None  # Attribut pour associer la commande à laquelle le box correspond
        self.piles = [] # liste des piles
        self.nombre_achats_box = nb  # Attribut pour suivre le nombre de box achetés de ce type
        self.long_res = self.type.l3
        self.time = 0 # i added a new attribute

    def empiler(self, unite, pile) : # permet de savoir si on peut empiler dans une pile
        value = False
        if (unite.produit == pile.type_prod):
            if ((pile.hauteur < unite.produit.nbEmpileMax * unite.produit.h) and (pile.hauteur < self.type.h3)) and    self.commande==unite.commande: # tant que la hauteur de la pile ne dépasse pas la hauteur du box, on peut empiler
                value = True
        return value

    def remplirPile(self,unite,p) :  
        self.contenu_box.append(unite) 
        self.commande = unite.commande #associe unité à une commande 
        p.hauteur += unite.produit.h2 #mise à jour pile
                
    def remplir_nouvelle_pile(self,unite) : # créer une nouvelle pile
        if (self.long_res - unite.produit.l>=0) : #
            self.contenu_box.append(unite) 
            self.commande=unite.commande
            p1 = Pile(unite.produit)
            self.piles.append(p1)
            p1.hauteur += unite.produit.h
            self.long_res -= p1.longueur

    def vider(self) :
        self.contenu_box =[]
        self.piles =[]
        self.commande = None
        self.long_res = self.type.l3
        
    def est_vide(self) :
        result = False
        if (self.commande == None and len(self.piles) == 0 and len(self.contenu_box) == 0) :
            result = True
        return result
    
class FactorySimulation:
    def __init__(self, file_CSV, file_JSON):
        self.type_box = {}
        self.components = self.load_components(file_JSON)
        self.products = self.load_products(file_JSON)
        self.orders = self.load_orders(file_CSV)
        self.production_lines = self.load_production_lines(file_JSON)
        self.type_de_box = self.load_storage_boxes(file_JSON)
        self.boxachetes = []
        self.unities_produced = []
        self.components_produced = []
        self.box_used = []
        self.pile = []
        self.dict_box_commande = dict()
        self.box_commande = {}
        self.eval = 0
        self.indice = 0
        self.listProducedUnities = []
        
        # Optimizing
        self.orders.sort(key=lambda order: order.date_envoiPrevue)
        

    def load_components(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            listComposants = [TypeComposant(tc["id"], tc["m"], tc["s"], tc["t"], tc["h"], tc["l"], tc.get("w")) for tc in data["types_composants"]]
            return listComposants

    def load_products(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            listTypesProduits = [TypeProduit(tp["id"], tp["s"], tp["p"], tp["h"], tp["l"], tp["w"], tp["nbEmpileMax"]) for tp in data["types_produits"]]
            return listTypesProduits

    def load_orders(self, file_path):
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=' ')
            
            listCommandes = []
            for row in csv_reader:
                identifiant = row[0]
                temps_qualite = int(row[1])
                date_envoi = int(row[2])

                numberOfEachProduct = []

                for i in range(3, len(row)):
                    numberOfEachProduct.append(int(row[i]))

                oneCommande = commandes(identifiant, temps_qualite, date_envoi, numberOfEachProduct)
                listCommandes.append(oneCommande)
            return listCommandes

    def load_production_lines(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            listLignes = [types_lignes(l["id"], l["operation"], l["esi"], index + 1) for index, l in enumerate(data["lignes"])]
            return listLignes
    
    def load_storage_boxes(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            listTypesBox = [types_box(tb["id"], tb["h"], tb["l"], tb["prix"]) for tb in data["types_box"]]
            return listTypesBox
        
    def set_eval(self, value):
        self.eval = value
       
    def run_simulation_production(self):
        listCommandes = self.orders
        listTypesProduits = self.products
        listComposants = self.components
        listLignes = self.production_lines
        eval = self.eval
        
        for Commande in listCommandes:
            nb_produits = 0
            i = 0
            for Product in listTypesProduits:
                nb_produits = nb_produits + Commande.nombre_unite[i]
                if Commande.nombre_unite[i] == 0:
                    pass
                else:
                    verre = next((Component for Component in listComposants if Component.m == "verre" and Component.h == Product.h and Component.l == Product.l), None)

                    membrane = next((Component for Component in listComposants if Component.m == "membrane" and Component.h == Product.h and Component.l == Product.l), None)
                    
                    eva = next((Component for Component in listComposants if Component.m == "eva" and Component.h == Product.h and Component.l == Product.l), None)
                    
                    cellules = next((Component for Component in listComposants if Product.w == Component.w), None)

                    components_tobe_produced = [eva, eva, verre, membrane]
                    
                    lines_production = [ Line for Line in listLignes if Line.types_operation == "production" ]
                    lines_production_notfull = [ Line for Line in lines_production if Line.stock_esi > 0 ]
                    line_production_notfull_balancingload = max(lines_production_notfull, key=lambda Line: Line.stock_esi)
                    
                    lines_used = []
                    lines_used.append(line_production_notfull_balancingload)

                    if line_production_notfull_balancingload.dernier != cellules.id:
                        line_production_notfull_balancingload.set_time = line_production_notfull_balancingload.set_time + cellules.s
                        
                    nouvelle_componant = composant_produit(
                            len(self.components_produced) + 1,
                            cellules.id,
                            cellules.m,
                            line_production_notfull_balancingload.index,
                            line_production_notfull_balancingload.set_time
                        )

                    # Aggiunta dell'oggetto alla lista
                    self.components_produced.append(nouvelle_componant)
                    
                    line_production_notfull_balancingload.set_time = line_production_notfull_balancingload.set_time + cellules.t 
                      
                    line_production_notfull_balancingload.dernier = cellules.id
                    
                    line_production_notfull_balancingload.stock_esi = line_production_notfull_balancingload.stock_esi - Commande.nombre_unite[i]
                    
                    for Component in components_tobe_produced:
                        lines_decoupe = [Line for Line in listLignes if Line.types_operation == "decoupe"]
                        lines_decoupe_notfull = [Line for Line in lines_decoupe if Line.stock_esi > 0]
                        line_decoupe_notfull_balancingload = max(lines_decoupe_notfull, key=lambda Line: Line.stock_esi)
                        
                        lines_used.append(line_decoupe_notfull_balancingload)
                        
                        if line_decoupe_notfull_balancingload.dernier != Component.id:
                            line_decoupe_notfull_balancingload.set_time = line_decoupe_notfull_balancingload.set_time + Component.s
                        
                        nouvelle_componant = composant_produit(
                            len(self.components_produced) + 1,
                            Component.id,
                            Component.m,
                            line_decoupe_notfull_balancingload.index,
                            line_decoupe_notfull_balancingload.set_time
                        )

                        # Aggiunta dell'oggetto alla lista
                        self.components_produced.append(nouvelle_componant)
                        
                        line_decoupe_notfull_balancingload.set_time = line_decoupe_notfull_balancingload.set_time + Component.t 

                        line_decoupe_notfull_balancingload.dernier = Component.id
                        
                        line_decoupe_notfull_balancingload.stock_esi = line_decoupe_notfull_balancingload.stock_esi - Commande.nombre_unite[i]
                          
                    
                    line_finishing_the_latest = max(lines_used, key=lambda Line: Line.set_time)
                    when_components_ready = line_finishing_the_latest.set_time
                    lines_assemblage = [Line for Line in listLignes if Line.types_operation == "assemblage"]
                    line_assemblage_balancingload = min(lines_assemblage, key=lambda Line: Line.set_time)
                    starting_assembly = max(when_components_ready,line_assemblage_balancingload.set_time)
                    
                    if line_assemblage_balancingload.set_time < starting_assembly:
                        line_assemblage_balancingload.set_time = starting_assembly                        
                    if line_assemblage_balancingload.dernier != Component.id:
                        line_assemblage_balancingload.set_time = line_assemblage_balancingload.set_time + Product.s
                    
                    nouvelle_unite = prod_unitaire(
                            Commande.identifiant,
                            Commande,
                            Product,
                            Product.id,
                            line_assemblage_balancingload.index,
                            line_assemblage_balancingload.set_time,
                            [str(self.components_produced[len(self.components_produced)-5].identifiantComposant),
                             str(self.components_produced[len(self.components_produced)-4].identifiantComposant),
                             str(self.components_produced[len(self.components_produced)-3].identifiantComposant),
                             str(self.components_produced[len(self.components_produced)-2].identifiantComposant),
                             str(self.components_produced[len(self.components_produced)-1].identifiantComposant)]
                        )
                    
                    self.listProducedUnities.append(nouvelle_unite)
                    line_assemblage_balancingload.set_time = line_assemblage_balancingload.set_time + Commande.nombre_unite[i]*Product.p #rimuovi setup quando non serve  
                    line_decoupe_notfull_balancingload.dernier = Component.id
                    if Commande.date_demande_box == None:
                        Commande.date_demande_box = starting_assembly + Product.s + Product.p   
                i += 1
            
            Commande.date_envoi = Commande.date_envoi + line_assemblage_balancingload.set_time + Commande.temps_qualite #= max(pi,p2,p3,..)+stockmin+duree
            
            if Commande.date_envoi < Commande.date_envoiPrevue:
                Commande.date_envoi = Commande.date_envoiPrevue
            
            eval = eval + nb_produits * 10 * abs(Commande.date_envoi - Commande.date_envoiPrevue)
            factory_simulation.set_eval(eval)

    def acheter_box(self, type_box):
        if type_box.id not in self.type_box.keys():
            self.type_box[type_box.id] = 1
        else:
            self.type_box[type_box.id] += 1
        B = box(type_box, self.type_box[type_box.id])
        self.boxachetes.append(B)
        type_box.nombre_achats_box += 1
        return B

    def stockage_unite(self):
        boxachetes = self.boxachetes
        value = True
        indice = self.indice
        addEval = 0

        for unite in self.listProducedUnities:
            if unite.idcommande not in self.dict_box_commande:
                self.dict_box_commande[unite.idcommande] = [unite]
            else:
                self.dict_box_commande[unite.idcommande].append(unite)

            if unite.idcommande not in self.box_commande:
                self.box_commande[unite.idcommande] = []

            # Ensure boxes are reset if necessary
            for elem1 in boxachetes:
                for elem2 in self.box_commande.keys():
                    if elem1 in self.box_commande[elem2]:
                        value = False
                if value == True:
                    elem1.vider()
        for elem in self.dict_box_commande.keys():
            for i in range(len(self.dict_box_commande[elem])):
                a = len(self.box_commande[self.dict_box_commande[elem][i].idcommande])
                for k in range(a):
                    if a != 0:
                        indice = len(self.box_commande[self.dict_box_commande[elem][i].idcommande][k].piles) - 1
                        if self.box_commande[self.dict_box_commande[elem][i].idcommande][k].empiler(
                                self.dict_box_commande[elem][i],
                                self.box_commande[self.dict_box_commande[elem][i].idcommande][-1].piles[
                                    indice]) == True:
                            self.dict_box_commande[elem][i].box = self.box_commande[self.dict_box_commande[elem][i].idcommande][-1]
                            self.dict_box_commande[elem][i].identifiant_box = self.box_commande[self.dict_box_commande[elem][i].idcommande][-1].type.id
                            self.dict_box_commande[elem][i].box.remplirPile(self.dict_box_commande[elem][i],
                                                                            self.dict_box_commande[elem][i].box.piles[indice])
                            self.dict_box_commande[elem][i].box.commande = self.dict_box_commande[elem][i].commande
                        else:
                            self.dict_box_commande[elem][i].box = self.box_commande[self.dict_box_commande[elem][i].idcommande][-1]
                            self.dict_box_commande[elem][i].identifiant_box = self.box_commande[self.dict_box_commande[elem][i].idcommande][-1].type.id
                            self.dict_box_commande[elem][i].box.remplir_nouvelle_pile(self.dict_box_commande[elem][i])
                            self.dict_box_commande[elem][i].box.commande = self.dict_box_commande[elem][i].commande

                if len(self.boxachetes) == 0 or len(self.box_commande[self.dict_box_commande[elem][i].idcommande]) == 0:    
                    j = 0
                    while self.dict_box_commande[elem][i].produit.l > self.type_de_box[j].l3 and self.dict_box_commande[elem][i].produit.h > self.type_de_box[j].h3:
                        j += 1
                    if j < len(self.type_de_box):
                        B = self.acheter_box(self.type_de_box[j])
                        addEval += self.type_de_box[j].prixbox
                        self.dict_box_commande[elem][i].box = B
                        self.dict_box_commande[elem][i].identifiant_box = B.type.id
                        B.remplir_nouvelle_pile(self.dict_box_commande[elem][i])
                        self.dict_box_commande[elem][i].box.commande = self.dict_box_commande[elem][i].commande
                        self.box_commande[self.dict_box_commande[elem][i].idcommande].append(B)
        self.eval += addEval
            
    def print_results(self, filename):
        listCommandes = self.orders
        listProducedUnities = self.listProducedUnities
        listProducedComponents = self.components_produced
        listBoxes = self.type_de_box
        eval = self.eval

        with open(filename, 'w') as file:
            file.write(f"{eval}\n")

            for box in listBoxes:
                file.write(f"{box.id} {box.nombre_achats_box}\n")

            for commande in listCommandes:
                print(f"{commande.identifiant} requires stocking at {commande.date_demande_box}")
                print(f"{commande.identifiant} completed stocking at {commande.date_envoi}")
                file.write(f"{commande.identifiant} {commande.date_envoi}\n")

            for ProducedUnity in listProducedUnities:
                if ProducedUnity.box:  # Check if box is not None
                    file.write(f"{ProducedUnity.idcommande} {ProducedUnity.idTypeProduit} {ProducedUnity.index} {ProducedUnity.ddebut} {ProducedUnity.box.type.id} {ProducedUnity.box.nombre_achats_box} {' '.join(ProducedUnity.idcomposant)}\n")

            for ProducedComponent in listProducedComponents:
                file.write(f"{ProducedComponent.identifiantComposant} {ProducedComponent.identifiantType} {ProducedComponent.identifiant_ligne} {ProducedComponent.ddebut}\n")
              

# Main
if __name__ == "__main__":
    instanceA_csv = r"..\InstanceA.csv"
    instanceA_json = r"..\instanceA.json"
    instanceA_sol = r"C:\Scolaire\INSA Lyon\2023 2024\RIP\data\instanceA_c.sol"
    factory_simulation = FactorySimulation(instanceA_csv, instanceA_json)
    factory_simulation.run_simulation_production()
    factory_simulation.stockage_unite()
    factory_simulation.print_results(instanceA_sol)
