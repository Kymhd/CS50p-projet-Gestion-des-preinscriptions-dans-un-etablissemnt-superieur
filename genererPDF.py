# -*- coding: utf-8 -*
from fpdf import FPDF
import qrcode
import os
from validation import afficher_date_formattee

dossier_images = 'images'

class PDF(FPDF):
    def header(self):
        """Ajoute l'en-tête du PDF.

        Affiche un titre centré en haut de chaque page du PDF.
        """
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "Certificat d'inscription à l'Université Des Comores", 0, 1, 'C')

    def footer(self):
        """Ajoute le pied de page du PDF.

        Affiche le une chaine de caractère qui montre qu'il sagit s'un faux ceritificat.
        Mais en général, c'est ici on met le numero des pasge 
        // self.set_font('Arial', 'I', 8)
        // self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'L')
        """
        self.set_y(-15)
        self.set_font('Times', 'I', 10)
        self.cell(0, 10, '''C'est un faux certificat, ça ne représente pas l'Université Des Comores, il s'agit d'un projet d'apprentissage. Merci''', 0, 0, 'C')

        # Ajoutez une ligne horizontale pour la bordure inférieure
        self.set_draw_color(102, 204, 102)
        self.set_line_width(0.3)
        self.line(10, self.h - 15, self.w - 10, self.h - 15)


    def chapter_title(self, title):
        """Ajoute un titre de chapitre au PDF.

        Affiche un titre de chapitre centré dans une nouvelle ligne.
        
        Paramètres:
            title (str): Le titre du chapitre.
        """
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10)
        self.cell(0, 20, title, 0, 1, 'C')
        self.ln()

    def chapter_body(self, body):
        """Ajoute le corps du chapitre au PDF.

        Affiche le contenu du chapitre dans le PDF.
        
        Paramètres:
            body (str): Le contenu du chapitre.
        """
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.set_font('Arial', 'B', 12)
        self.ln()


    def add_qr_code(self, text, x, y, size=25):
        """Ajoute un code QR au PDF.

        Crée un code QR à partir du texte spécifié et l'ajoute au PDF à la position indiquée.
        
        Paramètres:
            text (str): Les données à encoder dans le code QR.
            x (int): La position X où ajouter le code QR.
            y (int): La position Y où ajouter le code QR.
            size (int): La taille du code QR.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qrcode.png")
        self.image("qrcode.png", x=x, y=y, w=size, h=size)
        os.remove("qrcode.png")


    def add_stamp(self, stamp_file, x, y, size=30):
        """Ajoute un tampon (image) au PDF.

        Ajoute une image (tampon) au PDF à la position indiquée.
        
        Paramètres:
            stamp_file (str): Le chemin de l'image du tampon.
            x (int): La position X où ajouter le tampon.
            y (int): La position Y où ajouter le tampon.
            size (int): La taille du tampon.
        """
        self.image(stamp_file, x=x, y=y, w=size, h=size)


def generer_pdf_etudiant(etudiant):
    """Génère un fichier PDF personnalisé pour un étudiant.

    Crée un fichier PDF contenant les informations de l'étudiant, un code QR et un tampon.
    
    Paramètres:
        etudiant (Etudiant): L'objet étudiant contenant les informations à inclure dans le PDF.
    """
    pdf = PDF()
    pdf.add_page()

    # Ajoutez le logo
    logo_path = os.path.join(dossier_images, 'udc.jpeg')
    pdf.image(logo_path, x=10, y=8, w=25)

    # Ajoutez le QR code
    qr_code_data = f"Nom: {etudiant.nom}\nPrénom: {etudiant.prenom}\nMatricule: {etudiant.matricule}"
    pdf.add_qr_code(qr_code_data, x=160, y=8, size=25)

    pdf.ln(20)

    # Formatez le titre avec un f-string
    title = f'Nom : {etudiant.nom}\nPrénom : {etudiant.prenom}'
    pdf.set_font('Times', 'B', 12)
    pdf.multi_cell(0, 10, title)
    pdf.set_text_color(0, 0, 0)
    
    date = afficher_date_formattee()
    # Formatez le corps du texte avec des f-strings
    body = f'{"Matricule :"} {etudiant.matricule}\n'
    body += f'{"Numéro Table (BAC) :"} {etudiant.numero}\n'
    body += f'{"Sexe :"} {etudiant.sexe}\n'
    body += f'{"Série :"} {etudiant.serie}\n'
    body += f'{"Date de Naissance :"} {etudiant.date_naissance}\n'
    body += f'{"Faculté :"} {etudiant.faculte}\n'
    body += f'{"Département :"} {etudiant.departement}\n'
    body += f'{"Email :"} {etudiant.email}'

    pdf.set_font('Times', 'B', 12)
    pdf.chapter_body(body)
    pdf.set_font('Times', '', 12)

    #pdf.add_stamp('cache.jpeg', x=130, y=140, size=30) Cachet UNION DES COMORES
    # Pour ajouter le tampon 'signature.png'
    signature_path = os.path.join(dossier_images, 'signature.png')
    pdf.add_stamp(signature_path, x=95, y=160, size=22)

    # Pour ajouter le tampon 'approuver.png'
    approuver_path = os.path.join(dossier_images, 'approuver.png')
    pdf.add_stamp(approuver_path, x=97, y=172, size=33)

    pdf.set_font('Times', '', 13)
    pdf.cell(0, 10, f'{date}',0, 1, 'C')

    pdf.set_font('Times', 'B', 13)
    pdf.cell(0, 10, 'Dr Zgnama MOHAMED', 0, 1, 'C')
    pdf.set_font('Times', '', 13)
    pdf.cell(0, 10, 'Chef de scolarité', 0, 1, 'C')
    

    filename = f'{etudiant.matricule}.pdf'
    pdf.output(filename)

    print(f'Votre cerificat PDF "{filename}" a été généré avec succès.')
