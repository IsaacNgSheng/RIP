import json
import csv

class commandes:
    def __init__(self, id, temps_qualite, date_envoiPrevue, nombre_unite, date_demande_box=None, date_envoi=None):
        self.id = id
        self.temps_qualite = temps_qualite
        self.date_envoiPrevue = date_envoiPrevue
        self.nombre_unite = nombre_unite
        self.date_envoi = 0
        self.date_demande_box = date_demande_box#W+

class types_composants:
    def __init__(self, id, m, temps_S, temps_P, h, l, w=None):
        self.id = id
        self.m = m
        self.temps_S = temps_S
        self.temps_P = temps_P
        self.h = h
        self.l = l
        self.w = w
        
class composant_produit: 
    def __init__(self, idComposant, idType, type_composant, id_ligne, date_debut):
        self.idComposant = idComposant
        self.idType = idType
        self.type_composant = type_composant
        self.id_ligne = id_ligne
        self.date_debut = date_debut  

class types_produits:
    def __init__(self, id, temps_S, temps_assemblage, h, l, w , nbEmpileMax):
        self.id = id
        self.temps_S = temps_S
        self.temps_assemblage = temps_assemblage
        self.h = h
        self.l = l
        self.w = w
        self.nbEmpileMax = nbEmpileMax
        
class unite_produite: 
    def __init__(self, id_commande, c, p, id_typeProduit, index, date_debut, ids_composants =None):
        self.id_commande = id_commande #W
        self.commande = c
        self.produit = p
        self.id_typeProduit = id_typeProduit
        self.index = index
        self.date_debut = date_debut
        self.id_box = None
        self.box = None
        self.ids_composants = ids_composants  
              
class types_lignes:
    def __init__(self, id, types_operation, stock_esi, index, dernier=None, set_time=None):
        self.id = id
        self.types_operation = types_operation
        self.stock_esi = stock_esi
        self.index = index
        self.dernier = ""
        self.set_time = 0
    
class types_box:
    def __init__(self, id, h, l,prix, nombre_achats_box=0):
        self.id = id
        self.h3 = h
        self.l3 = l
        self.prixbox=prix
        self.nombre_achats_box = nombre_achats_box
        
class Pile :
    def __init__(self,type_prod):
        self.type_prod = type_prod
        self.h = 0 
        self.l = self.type_prod.l
    
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
            if ((pile.h < unite.produit.nbEmpileMax * unite.produit.h) and (pile.h < self.type.h3)) and    self.commande==unite.commande: # tant que la h de la pile ne dépasse pas la h du box, on peut empiler
                value = True
        return value

    def remplirPile(self,unite,p) :  
        self.contenu_box.append(unite) 
        self.commande = unite.commande #associe unité à une commande 
        p.h += unite.produit.h #mise à jour pile
                
    def remplir_nouvelle_pile(self,unite) : # créer une nouvelle pile
        if (self.long_res - unite.produit.l>=0) : #
            self.contenu_box.append(unite) 
            self.commande=unite.commande
            p1 = Pile(unite.produit)
            self.piles.append(p1)
            p1.h += unite.produit.h
            self.long_res -= p1.l

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
            listComposants = [types_composants(tc["id"], tc["m"], tc["s"], tc["t"], tc["h"], tc["l"], tc.get("w")) for tc in data["types_composants"]]
            return listComposants

    def load_products(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            listTypesProduits = [types_produits(tp["id"], tp["s"], tp["p"], tp["h"], tp["l"], tp["w"], tp["nbEmpileMax"]) for tp in data["types_produits"]]
            return listTypesProduits

    def load_orders(self, file_path):
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=' ')
            
            listCommandes = []
            for row in csv_reader:
                id = row[0]
                temps_qualite = int(row[1])
                date_envoi = int(row[2])

                numberOfEachProduct = []

                for i in range(3, len(row)):
                    numberOfEachProduct.append(int(row[i]))

                oneCommande = commandes(id, temps_qualite, date_envoi, numberOfEachProduct)
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
                nombre_a_produire = Commande.nombre_unite[i]
                nb_produits += nombre_a_produire
                if nombre_a_produire == 0:
                    i += 1
                    continue
    
                verre = next((Component for Component in listComposants if Component.m == "verre" and Component.h == Product.h and Component.l == Product.l), None)
                membrane = next((Component for Component in listComposants if Component.m == "membrane" and Component.h == Product.h and Component.l == Product.l), None)
                eva = next((Component for Component in listComposants if Component.m == "eva" and Component.h == Product.h and Component.l == Product.l), None)
                cellules = next((Component for Component in listComposants if Product.w == Component.w), None)
    
                if not verre or not membrane or not eva or not cellules:
                    print(f"Error: Missing components for product type {Product.id} in order {Commande.id}. Verre: {verre}, Membrane: {membrane}, EVA: {eva}, Cellules: {cellules}")
                    i += 1
                    continue
    
                components_tobe_produced = [eva, eva, verre, membrane]
                lines_production = [Line for Line in listLignes if Line.types_operation == "production"]
                lines_production_notfull = [Line for Line in lines_production if Line.stock_esi > 0]
                line_production_notfull_balancingload = max(lines_production_notfull, key=lambda Line: Line.stock_esi)
    
                lines_used = [line_production_notfull_balancingload]
    
                if line_production_notfull_balancingload.dernier != cellules.id:
                    line_production_notfull_balancingload.set_time += cellules.temps_S
    
                # Create components for each unit
                new_component_ids = []
                for _ in range(nombre_a_produire):
                    nouvelle_composant = composant_produit(
                        len(self.components_produced) + 1,
                        cellules.id,
                        cellules.m,
                        line_production_notfull_balancingload.index,
                        line_production_notfull_balancingload.set_time
                    )
    
                    self.components_produced.append(nouvelle_composant)
                    new_component_ids.append(nouvelle_composant.idComposant)
                    line_production_notfull_balancingload.set_time += cellules.temps_P
                    line_production_notfull_balancingload.dernier = cellules.id
    
                line_production_notfull_balancingload.stock_esi -= nombre_a_produire
    
                for Component in components_tobe_produced:
                    lines_decoupe = [Line for Line in listLignes if Line.types_operation == "decoupe"]
                    lines_decoupe_notfull = [Line for Line in lines_decoupe if Line.stock_esi > 0]
                    if lines_decoupe_notfull:
                        line_decoupe_notfull_balancingload = max(lines_decoupe_notfull, key=lambda Line: Line.stock_esi)
                        lines_used.append(line_decoupe_notfull_balancingload)

                        if line_decoupe_notfull_balancingload.dernier != Component.id:
                            line_decoupe_notfull_balancingload.set_time += Component.temps_S

                    # Create components for each unit
                    for _ in range(nombre_a_produire):
                        nouvelle_composant = composant_produit(
                            len(self.components_produced) + 1,
                            Component.id,
                            Component.m,
                            line_decoupe_notfull_balancingload.index,
                            line_decoupe_notfull_balancingload.set_time
                        )
    
                        self.components_produced.append(nouvelle_composant)
                        new_component_ids.append(nouvelle_composant.idComposant)
                        line_decoupe_notfull_balancingload.set_time += Component.temps_P
                        line_decoupe_notfull_balancingload.dernier = Component.id
    
                    line_decoupe_notfull_balancingload.stock_esi -= nombre_a_produire
    
                line_finishing_the_latest = max(lines_used, key=lambda Line: Line.set_time)
                when_components_ready = line_finishing_the_latest.set_time
                lines_assemblage = [Line for Line in listLignes if Line.types_operation == "assemblage"]
                line_assemblage_balancingload = min(lines_assemblage, key=lambda Line: Line.set_time)
                starting_assembly = max(when_components_ready, line_assemblage_balancingload.set_time)
    
                if line_assemblage_balancingload.set_time < starting_assembly:
                    line_assemblage_balancingload.set_time = starting_assembly
    
                if line_assemblage_balancingload.dernier != Product.id:
                    line_assemblage_balancingload.set_time += Product.temps_S
    
                for _ in range(nombre_a_produire):
                    nouvelle_unite = unite_produite(
                        Commande.id,
                        Commande,
                        Product,
                        Product.id,
                        line_assemblage_balancingload.index,
                        line_assemblage_balancingload.set_time,
                        [str(new_component_ids.pop(0)),
                         str(new_component_ids.pop(0)),
                         str(new_component_ids.pop(0)),
                         str(new_component_ids.pop(0)),
                         str(new_component_ids.pop(0))]
                    )
    
                    self.listProducedUnities.append(nouvelle_unite)
                    print(f"Commande {Commande.id} produit unité de type {Product.id} avec composants {nouvelle_unite.ids_composants}")
    
                    line_assemblage_balancingload.set_time += Product.temps_assemblage
    
                line_decoupe_notfull_balancingload.dernier = Component.id
    
                if Commande.date_demande_box is None:
                    Commande.date_demande_box = starting_assembly + Product.temps_S + Product.temps_assemblage
    
                i += 1
    
            Commande.date_envoi = Commande.date_envoi + line_assemblage_balancingload.set_time + Commande.temps_qualite
    
            if Commande.date_envoi < Commande.date_envoiPrevue:
                Commande.date_envoi = Commande.date_envoiPrevue
    
            eval += nb_produits * 10 * abs(Commande.date_envoi - Commande.date_envoiPrevue)
            self.set_eval(eval)



  
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
            if unite.id_commande not in self.dict_box_commande:
                self.dict_box_commande[unite.id_commande] = [unite]
            else:
                self.dict_box_commande[unite.id_commande].append(unite)

            if unite.id_commande not in self.box_commande:
                self.box_commande[unite.id_commande] = []

            # Ensure boxes are reset if necessary
            for elem1 in boxachetes:
                for elem2 in self.box_commande.keys():
                    if elem1 in self.box_commande[elem2]:
                        value = False
                if value == True:
                    elem1.vider()
        for elem in self.dict_box_commande.keys():
            for i in range(len(self.dict_box_commande[elem])):
                a = len(self.box_commande[self.dict_box_commande[elem][i].id_commande])
                #print(self.box_commande)
                for k in range(a):
                    if a != 0:
                        indice = len(self.box_commande[self.dict_box_commande[elem][i].id_commande][k].piles) - 1
                        if self.box_commande[self.dict_box_commande[elem][i].id_commande][k].empiler(
                                self.dict_box_commande[elem][i],
                                self.box_commande[self.dict_box_commande[elem][i].id_commande][-1].piles[
                                    indice]) == True:
                            self.dict_box_commande[elem][i].box = self.box_commande[self.dict_box_commande[elem][i].id_commande][-1]
                            self.dict_box_commande[elem][i].id_box = self.box_commande[self.dict_box_commande[elem][i].id_commande][-1].type.id
                            self.dict_box_commande[elem][i].box.remplirPile(self.dict_box_commande[elem][i],
                                                                            self.dict_box_commande[elem][i].box.piles[indice])
                            self.dict_box_commande[elem][i].box.commande = self.dict_box_commande[elem][i].commande
                        else:
                            self.dict_box_commande[elem][i].box = self.box_commande[self.dict_box_commande[elem][i].id_commande][-1]
                            self.dict_box_commande[elem][i].id_box = self.box_commande[self.dict_box_commande[elem][i].id_commande][-1].type.id
                            self.dict_box_commande[elem][i].box.remplir_nouvelle_pile(self.dict_box_commande[elem][i])
                            self.dict_box_commande[elem][i].box.commande = self.dict_box_commande[elem][i].commande

                if len(self.boxachetes) == 0 or len(self.box_commande[self.dict_box_commande[elem][i].id_commande]) == 0:    
                    j = 0
                    while self.dict_box_commande[elem][i].produit.l > self.type_de_box[j].l3 and self.dict_box_commande[elem][i].produit.h > self.type_de_box[j].h3:
                        j += 1
                    if j < len(self.type_de_box):
                        B = self.acheter_box(self.type_de_box[j])
                        addEval += self.type_de_box[j].prixbox
                        self.dict_box_commande[elem][i].box = B
                        self.dict_box_commande[elem][i].id_box = B.type.id
                        B.remplir_nouvelle_pile(self.dict_box_commande[elem][i])
                        self.dict_box_commande[elem][i].box.commande = self.dict_box_commande[elem][i].commande
                        self.box_commande[self.dict_box_commande[elem][i].id_commande].append(B)
        self.eval = self.eval + addEval
            
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
                print(f"{commande.id} requires stocking at {commande.date_demande_box}")
                print(f"{commande.id} completed stocking at {commande.date_envoi}")
                file.write(f"{commande.id} {commande.date_envoi}\n")
    
            for commande in listCommandes:
                for ProducedUnity in listProducedUnities:
                    if ProducedUnity.id_commande == commande.id:
                        file.write(f"{commande.id} {ProducedUnity.id_typeProduit} {ProducedUnity.index} {ProducedUnity.date_debut} {ProducedUnity.box.type.id} {ProducedUnity.box.nombre_achats_box} {' '.join(ProducedUnity.ids_composants)}\n")
    
            for ProducedComponent in listProducedComponents:
                file.write(f"{ProducedComponent.idComposant} {ProducedComponent.idType} {ProducedComponent.id_ligne} {ProducedComponent.date_debut}\n")

# Main
if __name__ == "__main__":
    
    factory_simulation = FactorySimulation("InstanceB.csv", "instanceB.json")
    factory_simulation.run_simulation_production()
    factory_simulation.stockage_unite()
    factory_simulation.print_results("instanceB_c.sol")
