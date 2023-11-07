# Importer les modules nécessaires
import sys
from validation import verifie_adresse_email
import json
import hashlib

# Définir la classe Admin

# Il y a plusieurs methodes pour cette classe, meme si dans le programme principal, nous utilisons pour
# l'instant la methode Login() seulement
class Admin:
    """Une classe qui représente un administrateur avec un email et un mot de passe hashé."""

    # Définir le constructeur
    def __init__(self, email:str, password: str):
        """Initialiser l'instance avec l'email et le mot de passe hashé."""
        self.email = email
        self.password = hashlib.sha256(password.encode()).hexdigest()

    # Définir la méthode pour créer un admin
    @classmethod
    def create_admin(cls):
        """Créer un admin et le stocker dans un fichier json."""
        # Demander l'email et le valider et verifier si un admin avec le même
        #nom existe ou pas 
        while True:
            email = input("Entrez votre Email: ")
            if verifie_adresse_email(email): #Vérifier si l'eamil est valide, on importe validation
                 # Vérifier si un administrateur avec le même email existe déjà dans le fichier JSON
                if cls.admin_exists(email):
                    print("Cet administrateur existe déjà.")
                    continue
                else:
                    break
            else:
                print("Email invalide.")

        # Demander le mot de passe et le valider deux fois
        while True:
            password = input("Entrez votre mot de passe: ")
            confirm_password = input("Confirmez votre mot de passe: ")
            if password == confirm_password:
                break
            else:
                print("Les mots de passe ne correspondent pas.")

        # Créer l'instance d'admin
        admin = cls(email, password)
        # Stocker l'admin dans un fichier json
        with open("admins.json", "a") as f:
            json.dump(admin.__dict__, f)
            f.write("\n")
        print("Admin créé avec succès.")
        return admin


    # Définir la méthode pour supprimer un admin
    @classmethod
    def delete_admin(cls, email: str):
        """Supprimer un admin du fichier json."""
        # Ouvrir le fichier json en mode lecture
        with open("admins.json", "r") as f:
            admins = f.readlines()
        # Chercher l'admin avec l'email donné
        for i, admin in enumerate(admins):
            admin = json.loads(admin)
            if admin["email"] == email:
                # Supprimer l'admin de la liste
                admins.pop(i)
                break
        else:
            print("Aucun admin trouvé avec cet email.")
            return False
        # Ouvrir le fichier json en mode écriture
        with open("admins.json", "w") as f:
            for admin in admins:
                f.write(admin)
        print("Admin supprimé avec succès.")
        return True

    # Définir la méthode pour se connecter en tant qu'admin
    @classmethod
    def login(cls):
        """Se connecter en tant qu'admin."""
        # Demander l'email et le mot de passe
        while True:
            email = input("Entrez votre email: ")
            if verifie_adresse_email(email):
                password = input("Entrez votre mot de passe: ")
                # Ouvrir le fichier json en mode lecture
                with open("admins.json", "r") as f:
                    admins = f.readlines()
                # Chercher l'admin avec l'email et le mot de passe donnés
                for admin in admins:
                    admin = json.loads(admin)
                    if admin["email"] == email and admin["password"] == hashlib.sha256(password.encode()).hexdigest():
                        return True
                    else:
                        return False
            else:
                print("L'email ne correspond pas")
                continue

    #Définir la méthode pour verifier si un admin existe deja avec le meme nom
    @classmethod
    def admin_exists(cls, email):
        """Vérifier si un administrateur avec le même email existe dans le fichier JSON."""
        with open("admins.json", "r") as f:
            admins = f.readlines()
        for admin in admins:
            admin = json.loads(admin)
            if admin["email"] == email:
                return True
        return False


