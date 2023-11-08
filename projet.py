"""
|-------------------------------------------------------------------|
|    Programme: Gestion des Préinscriptions                         |
|    Développé par : Ambdil-Kayoum MOHAMED                          |
|    Date de développement: Novembre 2023                           |
|    Cours: HarvardX CS50s Introduction to Programming with Python  |
|                                                                   |
|    NB: Beaucoup des choses à ameliorer, je suis encore novice !   |
|-------------------------------------------------------------------|
"""

# Importer les modules nécessaires
import re
import time
import csv
import datetime
from tabulate import tabulate
from genererPDF import generer_pdf_etudiant
from validation import verifie_adresse_email
from universite import Universite
from etudiant import Student
from admin import Admin
from rich.console import Console
from rich import print
from pyfiglet import Figlet


# Constantes
FILENAME = 'students.csv'
MAX_TENTATIVES = 3
DELAI = 1.2

console = Console() # Pour l'utilisation de rich


def main():
    """
    Fonction principale qui essaie d'appeller la fonction gestion, s'il ne lève pas une exception
    Selon les exigences du projet, cette fonction main() doit être au début """
    try:
        gestion()
    
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


# Classe Etudiant qui hérite de Student
class Etudiant(Student):
    """Représente un étudiant inscrit à l'université.

    Attributs:
        numero (int): le numéro d'ordre de l'étudiant.
        matricule (str): le matricule de l'étudiant.
        nom (str): le nom de famille de l'étudiant.
        prenom (str): le prénom de l'étudiant.
        sexe (str): le sexe de l'étudiant ('M' ou 'F').
        serie (str): la série du baccalauréat de l'étudiant.
        date_naissance (str): la date et le lieu de naissance de l'étudiant.
        faculte (str): la faculté à laquelle appartient l'étudiant.
        departement (str): le département auquel appartient l'étudiant.
        email (str): l'adresse email de l'étudiant.
    """

    def __init__(self, numero, matricule, nom, prenom, sexe, serie, date_naissance, faculte, departement, email):
        """Initialise un objet Etudiant avec les attributs donnés."""

        super().__init__()
        self.numero = numero
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.serie = serie
        self.faculte = faculte
        self.date_naissance = date_naissance
        self.departement = departement
        self.email = email

    
    def modifier_informations(self):
        """
        Methode pour modifier les informations de l'etdudiant, 
        """
        print(f"Les informations actuelles de l'étudiant sont :")
        print(self)

        # Crée un menu avec les options de modification
        menu = """
        [bold][magenta]
        Quelles informations souhaitez-vous modifier ?
        1. Date et lieu de naissance
        2. Sexe
        3. Nom et prénom
        4. Choix d'etudes
        5. Quitter
        """

        # Crée une variable pour contrôler la boucle
        continuer = True
        while continuer:
            print(menu)

            choix = console.input(f"[bold white]Entrez votre choix (1-5) : [reset]")

            if choix in ["1", "2", "3", "4", "5"]:
                choix = int(choix)

                if choix == 1:
                    self.modifier_date_lieu()
                    self.enregistrer_dans_csv()

                elif choix == 2:
                    self.modifier_sex()
                    self.enregistrer_dans_csv()

                elif choix == 3:
                    self.modifier_nom_prenom()
                    self.enregistrer_dans_csv()

                elif choix == 4:
                    self.modifi_universite()
                    self.enregistrer_dans_csv()

                else:
                    continuer = False
            else:
                print(f"'{choix}' ne fait pas partie des options !")
                continue

    def modifier_nom_prenom(self):

        nouveau_nom = input("Entrez le nouveau nom : ").strip().upper()
        nouveau_prenom = input("Entrez le nouveau prénom : ").strip().upper()

        if self.valider_nom_prenom(nouveau_nom, nouveau_prenom):
            self.nom = nouveau_nom
            self.prenom = nouveau_prenom

            # Mettre à jour les attributs Nom et First Nom de la classe parente (Student)
            self.info["Nom"] = nouveau_nom
            self.info["Prenom"] = nouveau_prenom

            self.nv_email(nouveau_nom, nouveau_prenom)
            console.print("[bold green]Le nom et le prénom ont été modifiés avec succès.[reset]")

    def valider_nom_prenom(self, nom: str, prenom: str) -> bool:
        """Valide le nom et le prénom saisis.
    
    Args:
        nom: str  # Le nom de famille saisi.
        prenom: str  # Le prénom saisi.

    Returns:
        bool: True si le nom et le prénom sont valides, False sinon.
    """
        if nom and prenom:
            if (re.match(r"^[A-Za-zéèàçëêûîôäöüïñ]+[A-Za-zéèàçëêûîôäöüïñ\s-]*$", nom) and
                re.match(r"^[A-Za-zéèàçëêûîôäöüïñ]+[A-Za-zéèàçëêûîôäöüïñ\s-]*$", prenom)):
                return True
            else:
                print("Erreur : Le nom et le prénom ne peuvent contenir que des lettres, des espaces, des tirets et des caractères accentués.")
        else:
            print("Erreur : Le nom et le prénom ne peuvent pas être vides.")
        return False
    

    def nv_email(self, nom: str, prenom: str) -> str:
        """Construit l'email de l'étudiant à partir de son nom et prénom.
        
        Args:
            nom: str  # Le nom de famille de l'étudiant.
            prenom: str  # Le prénom de l'étudiant.

        Returns:
            str: L'adresse email générée.
        """
        # Supprimer les espaces du nom et prénom
        nom_sans_espaces = nom.replace(' ', '')
        prenom_sans_espaces = prenom.replace(' ', '')
        
        # Construit l'email avec le nouveau nom et prénom sans espaces
        self.email = f"{prenom_sans_espaces.lower()}.{nom_sans_espaces.lower()}@udc.edu.km"
        return self.email
    

    def modifier_sex(self) -> str:
        """Méthode pour modifier le sexe de l'étudiant.
        Demande à l'utilisateur d'entrer le nouveau sexe (M ou F).
        Met à jour l'attribut sexe de l'étudiant.
        """
        while True:
            # Demande à l'utilisateur d'entrer le nouveau sexe
            nouveau_sexe = input("Entrez le nouveau sexe (M ou F) : ")
            # Vérifie si le nouveau sexe est valide (M ou F)
            if nouveau_sexe in ["M", "F"]:
                # Met à jour l'attribut sexe avec le nouveau sexe
                self.sexe = nouveau_sexe
                # Affiche un message de confirmation
                console.print(f"[bold green]Le sexe a été modifié avec succès.[reset]")
                return self.sexe    
            else:
                # Affiche un message d'erreur si le nouveau sexe n'est pas valide
                print("Erreur : Le sexe doit être M ou F.")
                continue

    def modifier_date_lieu(self) -> str:
        regex = r"^([0-9]{2})/([0-9]{2})/([0-9]{4}), ?(.*)$"

        while True:
            # Demande à l'utilisateur d'entrer la nouvelle date et le nouveau lieu de naissance
            nouvelle_date_lieu_naissance = input("Entrez la nouvelle date et le nouveau lieu de naissance au format jj/mm/aaaa,lieu: ").strip().upper()

            # Vérifie si la chaîne saisie correspond à l'expression régulière
            if re.match(regex, nouvelle_date_lieu_naissance):
                # Extrait les quatre groupes capturés par l'expression régulière
                jour, mois, annee, lieu_naissance = re.match(regex, nouvelle_date_lieu_naissance).groups()

                # Essaye de convertir les trois premiers groupes en un objet datetime
                try:
                    date_obj = datetime.datetime(int(annee), int(mois), int(jour))

                    # Met à jour les attributs date_naissance et lieu_naissance avec les nouvelles valeurs
                    self.date_naissance = date_obj.strftime("%d-%m-%Y") + ", "+ lieu_naissance
                    # Affiche un message de confirmation
                    console.print(f"[bold green]La date et le lieu de naissance ont été modifiés avec succès.[reset]")
                    return self.date_naissance
                except ValueError: # Si la conversion en datetime échoue (par exemple si la date n'existe pas)
                    # Affiche un message d'erreur
                    print("Erreur: Date de naissance invalide.")
                    continue
            else: # Si la chaîne saisie ne correspond pas à l'expression régulière
                    # Affiche un message d'erreur
                print("Erreur: Format de date et lieu de naissance incorrect.")
                continue


    def modifi_universite(self):
        universite = Universite()

        # Affecte la série actuelle de l'étudiant à l'attribut serie de l'objet Universite
        universite.serie = self.serie

        # Appelle la méthode choisir_faculte pour demander la nouvelle faculté à l'étudiant
        universite.choisir_faculte()

        # Met à jour l'attribut faculte avec la nouvelle valeur
        self.faculte = universite.faculte

        universite = Universite()

        # Affecte la faculté actuelle de l'étudiant à l'attribut faculte de l'objet Universite
        universite.faculte = self.faculte

        # Appelle la méthode choisir_departement pour demander le nouveau département à l'étudiant
        universite.choisir_departement()

        # Met à jour l'attribut departement avec la nouvelle valeur
        self.departement = universite.departement

        # Affiche un message de confirmation
        console.print("[bold green]Vos choix ont été modifiés avec succès[reset]")
        

    def enregistrer_dans_csv(self):
        # Ouvrir le fichier CSV en mode lecture
        with open('students.csv', encoding="utf-8",  mode='r') as fichier_csv:
            lecteur = csv.reader(fichier_csv)
            lignes = list(lecteur)

        # Trouver la ligne à mettre à jour (par exemple, en utilisant le numéro de table)
        for index, ligne in enumerate(lignes):
            if ligne[0] == self.numero:
                # Mettre à jour les données de la ligne avec les attributs mis à jour
                lignes[index] = [self.numero, self.matricule,
                                  self.nom, self.prenom, 
                                  self.sexe, self.serie, 
                                  self.date_naissance, 
                                  self.faculte, self.departement, 
                                  self.email]

        # Enregistrer les modifications dans le fichier CSV
        with open('students.csv', mode='w', encoding="utf-8", newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerows(lignes)


    def __str__(self):
        """Renvoie une représentation sous forme de chaîne de caractères d'un objet Etudiant.

        Retour:
            str: une chaîne contenant les informations principales sur l'étudiant.
        """
        return f"{self.numero}, {self.matricule}, {self.nom}, {self.prenom}, {self.serie}, {self.date_naissance}, {self.faculte}, {self.departement}, {self.email}"


# Demande à l'utilisateur de saisir son numéro d'étudiant et le valide
def saisir_numero() -> int:
    """Demande à l'utilisateur de saisir son numéro de table du baccalauréat et le valide.

    Retour:
        int: le numéro d'étudiant saisi par l'utilisateur.

    Lève:
        ValueError: si l'utilisateur entre une valeur qui n'est pas un entier.
    """
    while True:
        try:
            numero = int(input("Entrez votre numéro de table (BAC): "))
            if numero > 0:
                return numero
            else:
                print("Le numero doit etre supérieur à O")
        except ValueError:
            print("Veuillez entrez un numéro")


# Charge la liste des étudiants à partir du fichier CSV
def charger_etudiants() -> list:
    """Charge la liste des étudiants à partir du fichier CSV.

    Retour:
        list: Une liste d'objets Etudiant.

    Lève:
        FileNotFoundError: Si le fichier students.csv n'existe pas.
    """
    try:
        # Ouvrir le fichier CSV en mode lecture
        with open(FILENAME, encoding="utf-8", mode='r') as read_csv_file:
            # Utiliser un lecteur CSV pour parcourir les lignes du fichier
            read = csv.DictReader(read_csv_file, delimiter=',')
            etudiants = []
            # Parcourir chaque ligne du fichier CSV et créer un objet Etudiant à partir des données
            for row in read:
                etudiant = Etudiant(
                    row["Numero"],
                    row["Marticule"],
                    row["Nom"],
                    row["Prenom"],
                    row["Sexe"],
                    row["Serie"],
                    row["Date et Lieu de Naissance"],
                    row["Faculte"],
                    row["Departement"],
                    row["Email"]
                )
                etudiants.append(etudiant)
            # Retourner la liste d'objets Etudiant
            return etudiants
    except FileNotFoundError:
        # Lever une exception si le fichier students.csv n'existe pas
        raise FileNotFoundError("Le fichier students.csv n'existe pas.")


#Trié les etudiants selon la faculté
def tri_etudiants() -> None:
    """Trie les étudiants selon la faculté choisie par l'utilisateur.

    Demande à l'utilisateur d'entrer l'acronyme d'une faculté parmi une liste de choix.

    Retour:
        None: La fonction ne renvoie rien.

    Lève:
        FileNotFoundError: Si le fichier students.csv n'existe pas.
    """
    criteres = {
        "FDSE": "Faculté de Droit et Sciences Economiques(FDSE)",
        "FLSH": "Faculté des Lettres et Sciences Humaines (FLSH)",
        "IUT": "Institut Universitaire de Technologie (IUT)",
        "IFERE": "Institut de Formation (IFERE)",
        "EMSP": "Ecole de Médecine et de Santé Publique (EMSP)",
        "FST": "Faculté des Sciences et Techniques (FST)",
        "FIC": "Faculté IMAM Chafi (FIC)"
    }

    while True:
        acronyme = input(f"Entrez l'acronyme de la faculté ({', '.join(criteres.keys())}): ").strip().upper()

        if acronyme in criteres:
            faculte = criteres[acronyme]
            etudiants = charger_etudiants()
            etudiants_tries = [e for e in etudiants if e.faculte == faculte]
            etudiants_tries = [[e.matricule, e.nom, e.prenom, e.sexe, e.faculte, e.departement,] for e in etudiants_tries]

            if etudiants_tries:
                print(f"Il y a '{len(etudiants_tries)}' étudiant(s) pour la faculté '{acronyme.upper()}'")
                # Afficher le tableau des étudiants trié, pas toutes les informatins   
                print(tabulate(etudiants_tries, headers=["Matricule", "Nom", "Prenom", "Sexe", "Faculte", "Departement"], tablefmt="grid"))
                break
            else:
                print(f"Aucun étudiant trouvé pour le critère '{faculte}'.")
                return
        else:
            print(f"L'acronyme '{acronyme}' n'est pas valide. Veuillez entrer un acronyme valide.")


#Afficher les informations de l'etudiant
def afficher_informations_etudiant(etudiant: Etudiant):
    """Affiche les informations principales d'un objet Etudiant sous forme de tableau.

    Paramètres:
        etudiant (Etudiant): L'objet Etudiant dont on veut afficher les informations.
    """
    # Découper la date de naissance en date et lieu
    date_naissance, lieu_naissance = etudiant.date_naissance.split(", ")
    # Convertir la date de naissance en objet datetime
    date_naissance = datetime.datetime.strptime(date_naissance, "%d-%m-%Y")
    # Formater la date de naissance en chaîne de caractères
    date_naissance_str = date_naissance.strftime('%d-%m-%Y')
    # Calculer l'âge de l'étudiant
    age = f"{datetime.datetime.now().year - date_naissance.year} ans"

    # Créer une liste de listes pour stocker les informations sous forme de tableaux
    infos = [
        ["Nom", etudiant.nom],
        ["Prénom", etudiant.prenom],
        ["Matriculation", etudiant.matricule],
        ["Numéro", etudiant.numero],
        ["Sexe", etudiant.sexe],
        ["Série", etudiant.serie],
        ["Date de Naissance", date_naissance_str],
        ["Lieu de Naissance", lieu_naissance],
        ["Age", age],
        ["Faculté", etudiant.faculte],
        ["Département", etudiant.departement],
        ["Email", etudiant.email]
    ]
    # Afficher les informations sous forme de tableau à l'aide de la fonction tabulate
    print(tabulate(infos))


# Vérifie si le numéro d'étudiant existe déjà dans la liste
def numero_existe_deja(numero: int) -> bool:
    """Vérifie si le numéro d'étudiant existe déjà dans la liste des étudiants.

    Paramètres:
        numero (int): le numéro d'étudiant à vérifier.

    Retour:
        bool: True si le numéro existe déjà, False sinon.
    """
    return any(etudiant.numero == str(numero) for etudiant in charger_etudiants())


# Enregistre un nouvel étudiant dans la liste et dans le fichier CSV
def enregistrer_etudiant(numero: int) -> list:
    """
    Enregistre un nouvel étudiant dans la liste des étudiants et dans le fichier CSV.

    Paramètres:
        numero (int): Le numéro d'ordre du nouvel étudiant.

    Retour:
        list: La liste des objets Etudiant mise à jour.

    Lève:
        FileNotFoundError: Si le fichier students.csv n'existe pas.
    """
    # Charge la liste actuelle des étudiants à partir du fichier CSV
    etudiants = charger_etudiants()

    # Vérifie si un étudiant avec le même numéro existe déjà
    if numero_existe_deja(numero):
        # Si oui, renvoie la liste existante des étudiants sans ajouter le nouvel étudiant
        return etudiants
    
    # Crée un nouvel objet 'Student' pour collecter les informations de l'étudiant
    etudiant = Student()
    etudiant.ajouter_etudiant()

    # Crée un objet 'Universite' pour collecter les informations sur la série, la faculté et le département
    universite = Universite()
    universite.choisir_serie()
    universite.choisir_faculte()
    universite.choisir_departement()

    # Crée un nouvel objet 'Etudiant' avec les informations collectées
    nouvel_etudiant = Etudiant(
        str(numero),
        etudiant.info["Matricule"],
        etudiant.info["Nom"],
        etudiant.info["Prenom"],
        etudiant.info["Sexe"],
        universite.serie,
        etudiant.info["Date de naissance"],
        universite.faculte,
        universite.departement,
        etudiant.info["Email"]
    )

    # Ajoute le nouvel étudiant à la liste des étudiants
    etudiants.append(nouvel_etudiant)
    
    # Enregistre le nouvel étudiant dans le fichier CSV
    enregistrer_donne([nouvel_etudiant])

    # Affiche les informations du nouvel étudiant
    console.print("[cyan]L'étudiant avec les informations suivantes a été enregistré avec succès:[/cyan]")
    afficher_informations_etudiant(nouvel_etudiant)
    console.print("[bold][bright_red]Votre adresse email et Matricule gardez-les bien car c'est ce qui va vous aider à vous connecter.[/bright_red][/bold]")
    
    #genere un pdf contenant les informations de l'Etudiant qui vient juste de s'inscrire
    generer_pdf_etudiant(nouvel_etudiant)
    # Renvoie la liste mise à jour des étudiants
    return etudiants


# Connecte un étudiant existant et affiche ses informations
def connecter_etudiant(num_etudiant: int):
    """Connecte un étudiant existant.
    
    Args:
        num_etudiant (int): Le numéro d'étudiant à connecter.

    Effects:
        Cette fonction effectue les étapes nécessaires pour connecter un étudiant existant.
        - Elle recherche l'étudiant dans la liste des étudiants.
        - Elle masque partiellement le matricule et l'email de l'étudiant existant pour la saisie.
        - Elle gère les tentatives de connexion.
        - Si la connexion réussit, elle affiche les informations de l'étudiant.

        Si le nombre maximum de tentatives est atteint, le programme se termine.

    Returns:
        None
    """
    # Recherche de l'étudiant dans la liste des étudiants
    etudiants = charger_etudiants()
    etudiant_existant = [exist for exist in etudiants if exist.numero == str(num_etudiant)]

    # Masquage partiel du matricule et de l'email pour la saisie
    matricule_cache = "".join([etudiant.matricule.replace(etudiant.matricule[5:9], "***")
                               for etudiant in etudiant_existant])
    email_cache = "".join([etudiant.email.replace(etudiant.email[2:-12], "****")
                           for etudiant in etudiant_existant])

    # Affichage du message d'information
    console.print(f"[bold]L'étudiant avec le numéro '{num_etudiant}' est déjà inscrit.[/bold]")
    #print("S'il s'agit d'une erreur, veuillez contacter le support à 'support.inscription@udc.edu.km'")
    print()
    time.sleep(0.56)
    console.print("[bold]Pour voir toutes vos informations, connectez-vous avec votre adresse email et matricule.[/bold]")

    # Gestion des tentatives de connexion
    for _ in range(MAX_TENTATIVES):  # Trois tentatives maximum
        while True:
           email = input(f"Entrez votre adresse e-mail institutionnelle, '{email_cache}' : \n").lower().strip()
           if verifie_adresse_email(email):
               break
           else:
                print("Email incorrect. Veuillez réessayer.")
                continue
        matricule = input(f"Entrez votre matricule, '{matricule_cache}' : \n").upper().strip()
        
        # Vérification des informations de l'étudiant
        for etudiant in etudiant_existant:
            if etudiant.email == email and etudiant.matricule == matricule:
                # Affichage des informations de l'étudiant
                console.print("[bright_magenta]Connexion réussie... Voici vos informations :[/bright_magenta]")
                time.sleep(0.6)
                console.print(f"[bold][bright_green]Bonjour {etudiant.prenom}, vous êtes connecté(e).[/bright_green][/bold]")
                time.sleep(DELAI)
                afficher_informations_etudiant(etudiant)

                while True:
                    reponse = input("Souhaitez-vous modifier vos informations ? (O/N) : ").strip().upper()
                    # Vérifie si la réponse est valide (O ou N)
                    if reponse in ["O", "N"]:
                        # Si la réponse est O, appelle la méthode modifier_etudiant avec le numéro de l'étudiant
                        if reponse == "O":
                            etudiant.modifier_informations()
                            break
                        # Si la réponse est N, affiche un message de fin
                        elif reponse == "N":
                            console.print(f"[bold]Très bien, passez une bonne journée {etudiant.nom}.[/bold]")
                            return
                    else:
                        # Affiche un message d'erreur si la réponse n'est pas valide
                        print("Erreur : Veuillez choisir O ou N.")

                # Affichage des informations modifiées de l'étudiant
                console.print("[bold][bright_red]Voici vos informations modifiées :[/bright_red][/bold]")
                time.sleep(DELAI)
                afficher_informations_etudiant(etudiant)
                print(f"[bright_green]Voici votre nouveau certificat avec vos nouvelles informations[reset]")
                time.sleep(DELAI)
                generer_pdf_etudiant(etudiant)
                return
            # Affichage d'un message d'erreur en cas de correspondance incorrecte
            print("Les informations saisies ne correspondent pas. Réessayez.")
    # Message en cas d'échec du nombre maximum de tentatives
    print("Nombre maximum de tentatives atteint. Le programme se termine.")


# Enregistre la liste des étudiants dans le fichier CSV
def enregistrer_donne(donne: list):
    """Enregistre la liste des étudiants dans le fichier CSV.

    Paramètres:
        donne (list): Une liste d'objets Etudiant à enregistrer.

    Effet de bord:
        Cette fonction écrit les données des étudiants dans un fichier CSV.
        Si le fichier est vide, elle crée l'en-tête du fichier.

    Lève:
        FileNotFoundError: Si le fichier students.csv n'existe pas.
    """
    # Ouvrir le fichier CSV en mode 'ajout' (append) pour ajouter de nouvelles données
    with open(FILENAME, mode='a', encoding='utf-8', newline='') as csv_file: 
        # Définir les noms des champs (colonnes) dans le fichier CSV
        fieldnames = ["Numero","Marticule","Nom", "Prenom", "Sexe", "Serie", "Date et Lieu de Naissance","Faculte", "Departement", "Email"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Si le fichier est vide, écrire l'en-tête3
        if csv_file.tell() == 0:
            writer.writeheader()

        # Pour chaque étudiant dans la liste donnée
        for etudiant in donne:
            # Vérifier si le numéro d'étudiant n'existe pas déjà dans le fichier
            if not numero_existe_deja(etudiant.numero):
                # Écrire les données de l'étudiant dans le fichier CSV
                writer.writerow({
                    "Numero": etudiant.numero,
                    "Marticule": etudiant.matricule,
                    "Nom": etudiant.nom,
                    "Prenom": etudiant.prenom,
                    "Sexe": etudiant.sexe,
                    "Serie": etudiant.serie,
                    "Date et Lieu de Naissance": etudiant.date_naissance,
                    "Faculte": etudiant.faculte,
                    "Departement": etudiant.departement,
                    "Email": etudiant.email
                })


#// Cette partie conssite la gestion du Menu
#// Le menu qui s'affiche dans le terminal
#// Toutes les fonctions ci-dessous gerent la partie menu


def display_menu(menu_text):
    """Affiche un menu et retourne le choix de l'utilisateur."""
    console.print(menu_text)
    return console.input('[bold white]Entrez votre choix : [reset]').strip()


def register_student():
    """ 
    Cette fonction demande permet d'enregistrer un etudiant 
    elle est à la fois utiliser pour l'administration et la partie Etudiant
    """
    num_etudiant = saisir_numero()
    if numero_existe_deja(num_etudiant):
        connecter_etudiant(num_etudiant)
    else:
        donnee_etudiant = enregistrer_etudiant(num_etudiant)
        enregistrer_donne(donnee_etudiant)


def display_student_info():
    """
    Cette fonction c'est pour afficher les infos d'etudiants
    """
    num_etudiant = console.input("[bold white]Entrez votre numéro de (BAC) : [reset]").strip()
    if num_etudiant.isdigit():
        num_etudiant = int(num_etudiant)
        connecter_etudiant(num_etudiant)
    else:
        print("Le numéro d'étudiant doit être un entier.")


def gestion():
    continuer = True

    figlet = Figlet()
    figlet = figlet.getFonts()
    figlet = Figlet(font='big')
    print(figlet.renderText("KARIBU"))

    console.print("[bold underline][red]PLATEFORME DE PRÉINSCRIPTION DES ÉTUDIANTS AUX ÉTUDES SUP[/red][/bold underline]")
    
    menu_gestion = """
    [bold]VEUILLEZ CHOISIR UNE OPTION :[/bold]

    [bold][bright_green]
    [1] Se connecter en tant qu'admin
    [2] S'inscrire en tant qu'étudiant
    [3] Afficher ses informations en tant qu'étudiant
    [4] Quitter le programme
    """

    while continuer:
        try:
            choix = display_menu(menu_gestion)
            if choix == "1":
                if Admin.login():
                    admin_message = """
        [bold][green]CONNEXION REUSSI EN TANT QU'ADMIN[/green][/bold]
                    """
                    console.print(admin_message)
                    time.sleep(DELAI)
                    menu_admin = """
                    [bold][cyan]VEUILLEZ CHOISIR UNE OPTION :[/cyan][/bold]

                    [bold][blue]
                    [1]. Modifier un étudiant
                    [2]. Afficher tous les étudiants
                    [3]. Trier les étudiants
                    [4]. Retourner au menu principal
                    """
                    while True:
                        choix_admin = display_menu(menu_admin)
                        if choix_admin == "1":
                            numero = input("Entrez le numéro de l'étudiant à modifier : ").strip()
                            if numero.isdigit():
                                numero = int(numero)
                                connecter_etudiant(numero)
                            else:
                                print("Numéro d'étudiant invalide. Veuillez réessayer.")
                        elif choix_admin == "2":
                            console.print(f"[bold reed]-- Il y a {len(charger_etudiants())} étudiants inscrits -- [reset]")
                        elif choix_admin == "3":
                            tri_etudiants()
                        elif choix_admin == "4":
                            break
                        else:
                            print("Choix invalide. Veuillez réessayer.")
                else:
                    print("Email ou mot de passe incorect")

            elif choix == "2":
                register_student()
                continue
            elif choix == "3":
                display_student_info()
            elif choix == "4":
                continuer = False
            else:
                print("Choix invalide. Veuillez réessayer.")

        except KeyboardInterrupt:
            # Afficher un message d'erreur si l'utilisateur interrompt le programme avec Ctrl+C
            print("Interruption du programme. Veuillez réessayer.")
            continue
    print()
    console.print("[bold magenta]Merci d'avoir utilisé le système de préinscription des étudiants.[reset]")
    print()


if __name__ == "__main__":
    main()