import os
import csv
import re

class Nod:
    def __init__(self, nume, fisier_template, fisier_csv):
        self.nume = nume
        self.fisier_template = fisier_template
        self.fisier_csv = fisier_csv
        self.copii = []

    def adauga_copil(self, copil):
        self.copii.append(copil)

    def completeaza_document(self):
        # Verificăm dacă fisierul template există
        if not os.path.exists(self.fisier_template):
            print(f"Template-ul pentru '{self.nume}' nu există.")
            return

        # Verificăm dacă fisierul CSV există
        if not os.path.exists(self.fisier_csv):
            print(f"Fișierul CSV '{self.fisier_csv}' nu există.")
            return

        # Citim template-ul și extragem variabilele
        with open(self.fisier_template, 'r') as fisier:
            continut = fisier.read()

        # Folosim expresii regulate pentru a găsi variabilele în template
        pattern = r'\{(\w+)\}'
        variabile_template = re.findall(pattern, continut)
        print(f"Variabile în template: {variabile_template}")

        # Citim valorile din fișierul CSV
        completari = {}
        with open(self.fisier_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            # Presupunem că CSV-ul conține un singur rând de date pentru completare
            for row in reader:
                # Selectăm doar variabilele care sunt prezente în template
                for variabila in variabile_template:
                    if variabila in row:
                        completari[variabila] = row[variabila]
                break

        # Înlocuim variabilele din template cu valorile din CSV și afișăm variabilele înlocuite
        for variabila, valoare in completari.items():
            continut = continut.replace(f"{{{variabila}}}", valoare)
            print(f"Variabila '{variabila}' a fost înlocuită cu valoarea '{valoare}'.")

        # Salvăm documentul completat
        output_filename = f"{self.nume}_completat.txt"
        with open(output_filename, 'w') as fisier_output:
            fisier_output.write(continut)

        print(f"Documentul '{self.nume}' a fost completat și salvat ca '{output_filename}'.")

# Exemplu de utilizare
if __name__ == "__main__":
    # Creăm nodurile
    radacina = Nod("Codul CAEN 4765", None, None)
    nod1 = Nod("Politica de Confidentialitate", "politica_confidentialitate_template.txt", "utilizatori.csv")

    # Construim arborele
    radacina.adauga_copil(nod1)

    # Afișăm structura arborelui
    print("Structura arborelui de documente:")
    for copil in radacina.copii:
        print(f"- {copil.nume}")

    # Completăm documentele
    print("\nCompletarea documentelor:")
    for copil in radacina.copii:
        copil.completeaza_document()
