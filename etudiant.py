# Ce module contient une classe qui représente un étudiant.
import random
import datetime
import re

class Student:
    """Une classe qui représente un étudiant."""

    def __init__(self):
        """Initialise les attributs de la classe."""
        self._info = {
            "Matricule": None,
            "Nom": None,
            "Prenom": None,
            "Date de naissance": None,
            "Email": None,
            "Sexe": None
        }

    @property
    def info(self) -> dict:
        """Un dictionnaire qui contient les informations de l'étudiant.

        Returns
        -------
        dict
            Le dictionnaire des informations de l'étudiant.
        """
        return self._info

    @info.setter
    def info(self, value: dict):
        """Modifie les informations de l'étudiant.

        Parameters
        ----------
        value : dict
            Le nouveau dictionnaire des informations de l'étudiant.
        
        Returns
        -------
        None
        """
        self._info = value

    def construire_matricule(self) -> None:
        """Construit un matricule aléatoire pour l'étudiant.

        Le matricule est composé de l'année courante, de deux lettres aléatoires,
        de trois chiffres aléatoires et d'une lettre aléatoire.

        Returns
        -------
        None
        """
        current_year = datetime.date.today().year # Récupère l'année courante
        random_letters = ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2)) # Génère deux lettres aléatoires
        random_letter = ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1)) # Génère une lettre aléatoire
        random_int = ''.join(random.sample('0123456789', 3)) # Génère trois chiffres aléatoires
        self.info["Matricule"] = f"{current_year}{random_letters}{random_int}{random_letter}" # Construit le matricule

    def construire_email(self) -> None:
        """Construit un email institutionnel pour l'étudiant.

        L'email est composé du prénom, du nom et du domaine de l'université.
        
        Returns
        -------
        None
        """
        if self.info["Nom"] and self.info["Prenom"]:
            first_name = self.info['Prenom'].replace(' ', '') 
            # Enlève les espaces du prénom si besoin
            name = self.info['Nom'].replace(' ', '') 
            # Enlève les espaces du nom si besoin
            self.info["Email"] = f"{first_name}.{name}@udc.edu.km".lower() 
            # Construit l'email en minuscules
        else:
            print("Erreur : Le nom et le prénom sont nécessaires pour construire l'e-mail.")

    def choisir_sexe(self):
        """
       Demande le sexe de l'utilisateur et l'affecte à l'attribut Sexe de l'objet self.

    La méthode boucle tant que le sexe saisi n'est pas M ou F.
    Elle met le sexe saisi en majuscules sans espaces.
    """
        Sexe = "" # Initialise la variable Sexe à une chaîne vide
        while not Sexe: # Boucle tant que la variable Sexe est vide
            Sexe_user = input("Sexe M ou F: ").strip().upper() 
                # Demande le sexe à l'utilisateur et le met en majuscules sans espaces
            if Sexe_user in ["F", "M"]: # Si le sexe saisi est F ou M
                Sexe = Sexe_user # Affecte le sexe saisi à la variable Sexe
                break # Sort de la boucle while
            else: # Sinon, si le sexe saisi n'est pas F ou M
                print("Le Sexe ne corréspond pas !") # Affiche un message d'erreur et recommence la boucle
        self.info["Sexe"] = Sexe # Affecte la variable Sexe à l'attribut Sexe de l'objet self

    def date_et_lieu(self) -> None:
        """
        Demande la date et le lieu de naissance de l'utilisateur et 
        les affecte aux attributs correspondants de l'objet self.

        La méthode vérifie que la date et le lieu de naissance sont au format jj/mm/aaaa, lieu, 
        avec éventuellement un espace après la virgule.
        Elle convertit la date en un objet datetime et la formate en une chaîne de caractères au format jj-mm-aaaa.
        Elle affiche un message d'erreur si le format ou la date sont invalides.
        """
        regex = r"^([0-9]{2})/([0-9]{2})/([0-9]{4}), ?(.*)$" 
            # Définit une expression régulière pour vérifier le format de la date et du lieu de naissance
            # Le format attendu est jj/mm/aaaa, lieu, avec éventuellement un espace après la virgule

        while True: # Boucle indéfiniment jusqu'à ce que la date et le lieu soient valides
            date_lieu_naissance = input("Entrez votre date et votre lieu de naissance au format jj/mm/aaaa, lieu: ").strip().upper()
                # Demande la date et le lieu de naissance à l'utilisateur sous forme d'une chaîne de caractères
            if re.match(regex, date_lieu_naissance): 
                # Vérifie que la chaîne saisie correspond à l'expression régulière définie plus haut
                jour, mois, annee, lieu_naissance = re.match(regex, date_lieu_naissance).groups() 
                    # Extrait les quatre groupes capturés par l'expression régulière : jour, mois, année et lieu de naissance
                try:
                    date_obj = datetime.datetime(int(annee), int(mois), int(jour)) 
                        # Convertit les trois premiers groupes en un objet datetime en les transformant en entiers
                    #self.info["Lieu de naissance"] = lieu_naissance 
                        # Affecte le quatrième groupe (lieu de naissance) à l'attribut Lieu de naissance de l'objet self
                    self.info["Date de naissance"] = date_obj.strftime("%d-%m-%Y") + ", "+ lieu_naissance 
                        # Formate l'objet datetime en une chaîne de caractères au format jj-mm-aaaa et l'affecte à l'attribut Date de naissance de l'objet self avec le lieu de naissance
                    break # Sort de la boucle while
                except ValueError: # Si la conversion en datetime échoue (par exemple si la date n'existe pas)
                    print("Erreur: Date de naissance invalide.") # Affiche un message d'erreur et recommence la boucle
            else: # Si la chaîne saisie ne correspond pas à l'expression régulière
                print("Erreur: Format de date et lieu de naissance incorrect.") # Affiche un message d'erreur et recommence la boucle


    def ajouter_etudiant(self) -> None:
        """Ajoute un étudiant en demandant ses informations.

        Cette méthode demande le nom, le prénom, le sexe, la date et le lieu de naissance de l'étudiant.
        Elle appelle les méthodes choisir_sexe, date_et_lieu, construire_matricule et construire_email pour affecter les attributs correspondants à l'objet self.
        Elle lève une exception ValueError si la date de naissance n'est pas valide ou si le choix du sexe n'est pas M ou F.
        
        Parameters
        ----------
        self : objet Etudiant
            L'objet sur lequel la méthode est appelée.

        Returns
        -------
        None

        Raises
        ------
        ValueError : si la date de naissance n'est pas valide ou si le choix du sexe n'est pas M ou F.
            
        """
            
        # Boucle tant que le nom, le prénom ou le sexe ne sont pas renseignés
        while not self.info["Nom"] or not self.info["Prenom"]:
            Nom = input("Entrez votre Nom: ").strip().upper() # Enlève les espaces au début et à la fin du nom saisi
            Prenom = input("Entrez votre prénom: ").strip().upper() # Enlève les espaces au début et à la fin du prénom saisi et le met en majuscules

            if not Nom or not Prenom: # Vérifie que le nom, le prénom et le sexe ne sont pas vides
                print("Erreur : Le nom, le prénom ne peuvent pas être vides.") # Affiche un message d'erreur
                continue # Recommence la boucle principale
            if not (re.match(r"^[A-Za-zéèàçëêûîôäöüïñ]+[A-Za-zéèàçëêûîôäöüïñ\s-]*$", Nom) 
            and re.match(r"^[A-Za-zéèàçëêûîôäöüïñ]+[A-Za-zéèàçëêûîôäöüïñ\s-]*$", Prenom)): 
                # Vérifie que le nom et le prénom ne contiennent que des lettres, des espaces, des tirets et des caractères accentués
                print("Erreur : Le nom et le prénom ne peuvent contenir que des lettres, \
                    des espaces, des tirets et des caractères accentués.") # Affiche un message d'erreur
                continue # Recommence la boucle principale

            self.info["Nom"] = Nom.upper().capitalize() 
            # Affecte le nom saisi à l'attribut Nom, en mettant la première lettre en majuscule et le reste en minuscule
            self.info["Prenom"] = Prenom.upper() 
            # Affecte le prénom saisi à l'attribut Prenom, en mettant tout en majuscules
        self.choisir_sexe() # Appelle la méthode choisir_sexe pour demander et affecter le sexe de l'étudiant
        self.date_et_lieu()  # Appelle la méthode date_et_lieu pour demander et affecter la date et le lieu de naissance de l'étudiant
        self.construire_matricule()
        self.construire_email() # Appelle la méthode construire_email pour générer et affecter l'email de l'étudiant
