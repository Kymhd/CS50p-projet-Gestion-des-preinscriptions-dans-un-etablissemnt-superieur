# Ce module contient une classe qui représente une université.
class Universite:
    """Une classe qui représente une université."""

    def __init__(self):
        """Initialise les attributs de la classe.

        Cette méthode crée une instance de la classe Universite avec des attributs pour
        stocker des informations sur les facultés, les départements, la série de
        baccalauréat, la faculté choisie et le département choisi.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
            """
        # Constantes pour les noms des facultés
        FDSE = "Faculté de Droit et Sciences Economiques(FDSE)"
        FLSH = "Faculté des Lettres et Sciences Humaines (FLSH)"
        IUT = "Institut Universitaire de Technologie (IUT)"
        IFERE = "Institut de Formation (IFERE)"
        EMSP = "Ecole de Médecine et de Santé Publique (EMSP)"
        FST = "Faculté des Sciences et Techniques (FST)"
        FIC = "Faculté IMAM Chafi (FIC)"

        # Constantes pour les noms des départements
        DROIT = "Droit"
        SE = "Sciences Economiques"
        AES = "Administration Economique et Sociale (AES)"
        GEO = "Géographie"
        MATH = "Mathématiques"
        PHY = "Physique"
        CHIM = "Chimie"
        PC = "Physique-Chimie (PC)"
        SV = "Sciences de la Vie (SV)"
        SM = "Sciences Marines"
        LMF = "Lettres Modernes Françaises (LMF)"
        LEA = "Langues Etrangères Appliquées (LEA)"
        HIST = "Histoire"
        LC = "Langue Chinoise"
        SI = "Sciences Islamiques"
        LA = "Lettres Arabes"
        GEA = "(GEA)"
        COM = "Commerce"
        GI = "Génie Informatique"
        STAT = "Statistique"
        TH = "Tourisme et Hôtellerie"
        MSID = "Mathématique, Statistique et Informatique Décisionnelle (MSID)"
        FPE = "Formation de Professeur des Ecoles"
        SI = "Soins Infirmiers"
        SO = "Soins Obstétricaux"


        # tuples pour les facultés par campus
        self.facultes = {
            "A4": (FDSE, FLSH, IUT, IFERE, EMSP),
            "A1": (FDSE, FLSH, IUT, IFERE, EMSP),
            "C": (FST, IUT, FDSE, IFERE, EMSP),
            "D": (FST, IUT, FDSE, IFERE, EMSP),
            "A2": (FIC, IFERE),
            "G": (IUT, FDSE, FLSH, IFERE, EMSP)
        }

        # Ensembles pour les départements par faculté
        self.departements = {
            FDSE: [DROIT, SE, AES],
            FST: [MATH, PHY, CHIM, PC, SV, SM],
            FLSH: [LMF, LEA, HIST, GEO, LC],
            FIC: [SI, LA],
            IUT: [GEA, COM, GI, STAT, TH, MSID],
            IFERE: [FPE],
            EMSP: [SI, SO]
        }
        
        self.serie = None
        self.faculte = None
        self.departement = None

    def choisir_serie(self) -> None:
        """Demande à l'utilisateur de choisir sa série de baccalauréat.

        Cette méthode permet à l'utilisateur de choisir sa série de baccalauréat parmi
        les options disponibles. La série choisie est ensuite stockée dans l'attribut
        "self.serie".

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None
        """
        serie_bac = ["A4", "A1", "A2", "C", "D", "G"]
        while not self.serie:
            serie = input(f"Entrez votre série de baccalauréat ({(', ').join(serie_bac)}) : ")\
                    .upper().strip()
            if serie in self.facultes:
                self.serie = serie
            else:
                print(f"Série invalide. Veuillez choisir parmi '{(', ').join(serie_bac)}'.")

    def choisir_faculte(self):
        """Demande à l'utilisateur de choisir sa faculté.

        Cette méthode permet à l'utilisateur de choisir sa faculté parmi les options
        disponibles pour sa série de baccalauréat. La faculté choisie est stockée dans
        l'attribut "self.faculte".

        Parameters
        ----------
        None

        Returns
        -------
        str

        Raises
        ------
        ValueError : si l'utilisateur entre un choix qui n'est pas un entier valide.
        """
        if self.serie:
            print("Les facultés disponibles pour votre série sont :")
            # Utilisation d'une compréhension de liste pour afficher les facultés
            print("\n".join(f"{i}. {faculte}" for i, faculte in 
                            enumerate(self.facultes[self.serie], 1)))

            while not self.faculte:
                try:
                    choix = int(input("Choisissez une faculté (entrez le numéro) : "))
                    if 1 <= choix <= len(self.facultes[self.serie]):
                        self.faculte = self.facultes[self.serie][choix - 1]
                        return self.faculte
                    else:
                        print("Option invalide. Veuillez choisir un numéro parmi les "
                              "options disponibles.")
                except ValueError:
                    print("Option invalide. Veuillez choisir un numéro parmi les "
                          "options disponibles.")


    def choisir_departement(self):
        """Demande à l'utilisateur de choisir son département.

        Cette méthode permet à l'utilisateur de choisir son département parmi les
        options disponibles pour la faculté sélectionnée. Le département choisi est
        stocké dans l'attribut "self.departement".

        Parameters
        ----------
        None

        Returns
        -------
        str

        Raises
        ------
        ValueError : si l'utilisateur entre un choix qui n'est pas un entier valide.
        """
        if self.faculte:
            print(f"Les départements de la faculté '{self.faculte}' sont :")
            # Utilisation d'une compréhension de liste pour afficher les départements
            print("\n".join(f"{i}. {departement}" for i, departement in 
                            enumerate(self.departements[self.faculte], 1)))

            while not self.departement:
                try:
                    choix = int(input("Choisissez un département (entrez le numéro) : "))
                    if 1 <= choix <= len(self.departements[self.faculte]):
                        self.departement = self.departements[self.faculte][choix - 1]
                        return self.departement
                    else:
                        print("Option invalide. Veuillez choisir un numéro parmi les "
                              "options disponibles.")
                except ValueError:
                    print("Option invalide. Veuillez choisir un numéro parmi les "
                          "options disponibles.")

   