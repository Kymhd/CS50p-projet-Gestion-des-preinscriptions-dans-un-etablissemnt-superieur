import re
from datetime import datetime

def verifie_adresse_email(email):
    return bool(re.match(r"^[\w.%+-]+@udc\.edu\.km$", email))


def afficher_date_formattee():
    # Obtenir la date actuelle
    aujourd_hui = datetime.now()

    # Liste des noms des jours de la semaine
    noms_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    # Liste des noms des mois
    noms_mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", 
                 "août", "septembre", "octobre", "novembre", "décembre"]

    # Extraire le jour, le mois et l'année
    jour_semaine = noms_jours[aujourd_hui.weekday()]
    jour = aujourd_hui.day
    mois = noms_mois[aujourd_hui.month - 1]  # Soustrayez 1 car les mois sont indexés à partir de 1
    annee = aujourd_hui.year

    # Formatter la date
    date_formattee = f"{jour_semaine}, le {jour} {mois} {annee}".capitalize()

    # Afficher la date formatée
    return date_formattee




