import os
import csv
import re
from reportlab.pdfgen import canvas
from datetime import datetime

class Nod:
    def __init__(self, nume, fisier_template, fisier_csv):
        self.cod_caen = None
        self.nume = nume
        self.fisier_template = fisier_template
        self.fisier_csv = fisier_csv
        self.copii = []

    def adauga_copil(self, copil):
        self.copii.append(copil)

    def completeaza_document(self):
        # Verificam daca fisierul template exista
        if not os.path.exists(self.fisier_template):
            print(f"Template-ul pentru '{self.nume}' nu exista.")
            return

        # Verificam daca fisierul CSV exista
        if not os.path.exists(self.fisier_csv):
            print(f"Fisierul CSV '{self.fisier_csv}' nu exista.")
            return

        # Citim template-ul si extragem variabilele
        with open(self.fisier_template, 'r', encoding='utf-8') as fisier:
            continut = fisier.read()

        # Folosim expresii regulate pentru a gasi variabilele in template
        pattern = r'\{(\w+)\}'
        variabile_template = re.findall(pattern, continut)
        

        # Citim valorile din fisierul CSV
        completari = {}
        cod_caen = None
        with open(self.fisier_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Presupunem ca CSV-ul contine un singur rand de date pentru completare
            for row in reader:
                # Selectam doar variabilele care sunt prezente in template
                for variabila in variabile_template:
                    if variabila in row:
                        completari[variabila] = row[variabila].strip()  # Eliminam eventualele spatii
                # Extragem codul CAEN
                if 'cod_caen' in row:
                    cod_caen = row['cod_caen'].strip()
                    print(f"Codul CAEN extras din fisier este: {cod_caen}")
                    self.cod_caen = cod_caen
                break

        # Inlocuim variabilele din template cu valorile din CSV si afisam variabilele inlocuite
        for variabila, valoare in completari.items():
            continut = continut.replace(f"{{{variabila}}}", valoare)                                                         

        # Salvam documentul completat
        output_filename = f"{self.nume}_completat.txt"
        with open(output_filename, 'w', encoding='utf-8') as fisier_output:
            fisier_output.write(continut)

        print(f"Documentul '{self.nume}' a fost completat si salvat ca '{output_filename}'.")

        # Convertim fisierul text completat in PDF
        self.converteste_in_pdf(output_filename, cod_caen)

    def converteste_in_pdf(self, fisier_text, cod_caen):
        # Verificam daca fisierul text exista
        if not os.path.exists(fisier_text):
            print(f"Fisierul text '{fisier_text}' nu exista pentru a fi convertit in PDF.")
            return

        # Cream PDF folosind reportlab
        pdf_filename = fisier_text.replace(".txt", ".pdf")
        c = canvas.Canvas(pdf_filename)
        c.setFont("Helvetica", 12)

        # Adaugam data generarii PDF-ului in coltul din dreapta sus
        data_generare = datetime.now().strftime("Data: %d/%m/%Y")
        c.drawRightString(550, 820, data_generare)

        # Adaugam codul CAEN, daca este disponibil
        if cod_caen:
            c.drawString(30, 820, f"Cod CAEN: {cod_caen}")

        # Citim continutul fisierului text si il adaugam in PDF
        with open(fisier_text, 'r', encoding='utf-8') as fisier:
            linie_y = 800  # Coordonata y pentru plasarea randurilor
            for linie in fisier:
                c.drawString(30, linie_y, linie.strip())
                linie_y -= 15  # Scadem coordonata pentru urmatorul rand

        # Salvam PDF-ul
        c.save()
        print(f"Documentul PDF '{pdf_filename}' a fost creat.")

# Exemplu de utilizare
if __name__ == "__main__":
    # Cream nodurile
    # Citim codul CAEN din fisierul CSV
    cod_caen = None
    with open("utilizatori_final.csv", 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Cod_CAEN' in row:
                cod_caen = row['Cod_CAEN'].strip()
                break
    
    if cod_caen is None:
        print("Eroare: Nu s-a gasit niciun cod CAEN in fisierul CSV.")
        exit(1)

    # Cream radacina folosind codul CAEN
    print(f"Pentru urm cod CAEN: {cod_caen} se folosesc documentele: ")
    radacina = Nod(f"Codul CAEN {cod_caen}", None, "utilizatori_final.csv")
    
    # Nodurile sunt create manual, dar pentru viitor, nodurile acestea vor fi generate in functie de o matrice ce 
    # contine pe prima coloana toate codurile CAEN din baza noastra de date (adica fisierul csv), iar pentru fiecare cod
    # vor exista pe liniile corespunzatoare adrese catre numele fisierlor ce trebuie afisate odata cu codul CAEN respectiv
    
    # Just for demonstration 
    nod1 = Nod("Politica de Confidentialitate", "politica_confidentialitate_template.txt", "utilizatori_final.csv")
    nod2 = Nod("Politica de Cookies", "Politica_fisiere_cookies.txt", "utilizatori_final.csv")
    nod3 = Nod("Termeni si Conditii", "Termeni_si_Conditii.txt", "utilizatori_final.csv")
    nod4 = Nod("Declaratie de Conformitate", "DECLARATIE_DE_CONFORMITATE.TXT", "utilizatori_final.csv")
    nod5 = Nod("Certificat de Garantie", "Certificat_Garantie.txt", "utilizatori_final.csv")

    # Construim arborele
    radacina.adauga_copil(nod1)
    radacina.adauga_copil(nod2)
    radacina.adauga_copil(nod3)
    radacina.adauga_copil(nod4)
    radacina.adauga_copil(nod5)

    # Afisam structura arborelui
    print("Structura arborelui de documente:")
    for copil in radacina.copii:
        print(f"- {copil.nume}")

    # Completam documentele
    print("\nCompletarea documentelor:")
    for copil in radacina.copii:
        copil.completeaza_document()
