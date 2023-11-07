from projet import enregistrer_etudiant, tri_etudiants, saisir_numero, numero_existe_deja, afficher_informations_etudiant, Etudiant
import io
import sys
from unittest.mock import patch


def main():
    test_afficher_informations_etudiant()
    test_numero_existe_deja()
    test_enregistrer_etudiant()
    test_saisir_numero()
    test_tri_etudiants()


def test_enregistrer_etudiant():
    # Créer des données fictives pour le nouvel étudiant (remplacer le numéro par 1)
    numero = 1  # Modification du numéro
    matricule = "2023XA657O"
    nom = "Ambdil-kayoum"
    prenom = "MOHAMED"
    sexe = "M"
    serie = "A1"
    date_naissance = "23-03-1998, GEGE"  # Format correct
    faculte = "Faculté de Droit et Sciences Economiques(FDSE)"
    departement = "Droit"
    email = "mohamed.ambdil-kayoum@udc.edu.km"

    # Appeler la fonction enregistrer_etudiant avec le numéro fictif
    etudiants = enregistrer_etudiant(numero)

    # Vérifier que la liste des étudiants contient bien le nouvel étudiant
    assert len(etudiants) > 0  # La liste doit contenir au moins un étudiant

    # Vous pouvez vérifier que le premier étudiant ajouté est correct
    premier_etudiant = etudiants[0]  # Accéder au premier étudiant dans la liste
    assert premier_etudiant.numero == str(numero)
    assert premier_etudiant.matricule == matricule
    assert premier_etudiant.nom == nom
    assert premier_etudiant.prenom == prenom
    assert premier_etudiant.sexe == sexe
    assert premier_etudiant.serie == serie
    assert premier_etudiant.date_naissance == date_naissance  # Format identique
    assert premier_etudiant.faculte == faculte
    assert premier_etudiant.departement == departement
    assert premier_etudiant.email == email


# Définir une fonction de test
def test_numero_existe_deja():
    # Créer un numéro d'étudiant fictif qui existe déjà dans la liste des étudiants
    numero_existant = 1
    # Appeler la fonction numero_existe_deja avec ce numéro et récupérer le résultat
    resultat_existant = numero_existe_deja(numero_existant)
    # Vérifier que le résultat est bien True
    assert resultat_existant == True

    # Créer un numéro d'étudiant fictif qui n'existe pas dans la liste des étudiants
    numero_inexistant = 99999
    # Appeler la fonction numero_existe_deja avec ce numéro et récupérer le résultat
    resultat_inexistant = numero_existe_deja(numero_inexistant)
    # Vérifier que le résultat est bien False
    assert resultat_inexistant == False


# Définir une fonction de test
def test_afficher_informations_etudiant():
    # Créer un objet Etudiant fictif avec des données de l'étudiant numéro 1
    etudiant = Etudiant(
        numero = "1",
        matricule = "2023LT068L",
        nom = "AMBDIL-KAYOUM",
        prenom = "MOHAMED",
        sexe = "M",
        serie = "A1",
        date_naissance = "23-03-1998, GEGE",
        faculte = "Faculte IMAM Chafi",
        departement = "Droit Islamique",
        email = "mohamed.ambdil-kayoum@udc.edu.km"
    )

    # Capturer la sortie standard de la fonction afficher_informations_etudiant
    output = io.StringIO()
    sys.stdout = output
    afficher_informations_etudiant(etudiant)
    sys.stdout = sys.__stdout__

    # Récupérer la valeur de la sortie standard sous forme de chaîne de caractères
    output_str = output.getvalue()
    
    # Vérifier que la sortie standard contient bien le tableau attendu
    assert output_str == """\
-----------------  --------------------------------
Nom                AMBDIL-KAYOUM
Prénom             MOHAMED
Matriculation      2023LT068L
Numéro             1
Sexe               M
Série              A1
Date de Naissance  23-03-1998
Lieu de Naissance  GEGE
Age                25 ans
Faculté            Faculte IMAM Chafi
Département        Droit Islamique
Email              mohamed.ambdil-kayoum@udc.edu.km
-----------------  --------------------------------\n"""


# Définir une fonction de test
def test_saisir_numero(monkeypatch):
    # Utiliser le module monkeypatch pour simuler l'entrée de l'utilisateur
    monkeypatch.setattr('builtins.input', lambda _: "42")
    # Appeler la fonction saisir_numero et récupérer le résultat
    numero = saisir_numero()
    # Vérifier que le résultat est bien un entier
    assert isinstance(numero, int)
    # Vérifier que le résultat est bien le numéro saisi par l'utilisateur
    assert numero == 42



def test_tri_etudiants(monkeypatch, capsys):
    # Simule l'entrée utilisateur avec "IFERE"
    monkeypatch.setattr('builtins.input', lambda _: "IFERE")

    # Exécute la fonction et capture la sortie
    tri_etudiants()

    # Capture la sortie de la fonction
    captured = capsys.readouterr()

    # Vérifie si la sortie contient le texte attendu
    assert "Aucun étudiant trouvé pour le critère 'Institut de Formation (IFERE)'" in captured.out

if __name__ == "__main__":
    main()
