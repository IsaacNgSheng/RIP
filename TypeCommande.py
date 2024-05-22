import csv

class TypeCommande():
    def __init__(self, id, stockMin, dEnvoiPrevue, nb):
        #super().__init__(id, stockMin, dEnvoiPrevue, nb)
        self.id = id
        self.stockMin = stockMin
        self.dEnvoiPrevue = dEnvoiPrevue
        self.nb = nb
        
    def __str__(self):
        return f"TypeCommande(id='{self.id}', stockMin={self.stockMin}, dEnvoiPrevue={self.dEnvoiPrevue}, nb={self.nb})"

filename = 'C:/Users/Isaac/OneDrive/Documents/NUS/Exchange/Notes/RIP/Proj/InstanceA.csv'
data_rows = []

with open(filename, mode='r') as file:
    csv_reader = csv.reader(file, delimiter=' ')
    for row in csv_reader:
        if row:  # Ensure row is not empty
            nb = [row[3], row[4]]
            data_row = TypeCommande(row[0], row[1], row[2], nb)
            data_rows.append(data_row)

# Print the list of DataRow objects
for data_row in data_rows:
    print(data_row)
