# -*-coding:utf-8 -*

# Importation du module cartes
from Jeu.cartes import tf_comparer_deux_cartes


def creer_suite(cartes_du_joueur):

    """
    Fonction créant une suite de carte en fonction d'un trié en entrée
    :param cartes_du_joueur:
    :return:
    """

    # Initialisation des variables
    i = 0
    suite = list()

    # Ajout de la première carte du jeu à la suite
    suite.append(cartes_du_joueur.pop(0))

    # On parcourt toutes les cartes du jeu donné
    while i < len(cartes_du_joueur):

        # La carte choisie est la première carte du jeu
        carte_choisie = cartes_du_joueur[i]

        # Si la dernière carte de la suite est un roi
        if suite[-1][0] == 13:

            suite.append(carte_choisie)  # On ajoute la carte à la suite
            cartes_du_joueur.pop(i)  # On retire la carte jouée du jeu
            i = -1  # On modifie l'indice pour choisir la prochaine carte

        else:  # Sinon

            # Vérification que les deux cartes se suivent (carte choisie et dernière carte de la suite)
            if tf_comparer_deux_cartes(suite[-1], carte_choisie):

                suite.append(carte_choisie)  # On ajoute la carte à la suite
                cartes_du_joueur.remove(carte_choisie)  # On retire la carte jouée du jeu
                i -= 1  # On modifie l'indice pour choisir la prochaine carte

                # Si la carte choisie est un roi
                if carte_choisie[0] == 13:

                    # Initialisation de la variable
                    nombre_de_tete_restante = 0

                    # On parcourt toutes les têtes
                    for i in range(10, 14):

                        # On parcourt toutes les couleurs
                        for j in range(1, 5):

                            # On incrémente le nombre de têtes restantes si la tête est dans le jeu
                            nombre_de_tete_restante += cartes_du_joueur.count((i, j))

                    # S'il reste des têtes dans le jeu
                    if nombre_de_tete_restante > 0:

                        # On va faire suivre les têtes qui restent
                        i = -2

                    else:

                        # On repart de la carte la plus faible
                        i = -1

        # On augmente l'indice pour choisir la prochaine carte
        i += 1

    # On retourne la suite que l'on vient de créer
    return suite


def calcul_valeur_suite(suite):

    """
    Fonction retournant la valeur d'une suite entrée
    :param suite:
    :return:
    """

    # Initialisation de la variable
    valeur_suite = 0

    # On parcourt toute la suite
    for i in range(len(suite)):

        # On récupère les informations d'une carte
        a, b = suite[i]

        # Si la carte est une tête
        if a >= 11:

            # La valeur de la suite augmente de 10
            valeur_suite += 10

        # Sinon
        else:

            # La valeur de la suite augmente de la valeur de la carte
            valeur_suite += a

    # On retourne la valeur de la suite
    return valeur_suite


def strategie_minimiser(table_de_jeux, numero_du_joueur):

    """
    Fonction définissant la stratégie pour minimiser les pertes.
    Elle retourne quelle est la carte à jouer pour effectuer la meilleure suite (en termes de valeur)
    :param table_de_jeux:
    :param numero_du_joueur:
    :return:
    """

    # Initialisation des variables
    suites_de_cartes = []
    valeurs_des_suites_de_cartes = []
    i = 0

    # Copie des cartes du joueur dans une liste
    cartes_a_suitees = table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede.copy()

    # Tant que toutes les cartes n'ont pas été utilisées pour faire des suites
    while len(cartes_a_suitees) != 0:

        # On crée une suite
        suites_de_cartes.append(creer_suite(cartes_a_suitees))

        # On calcule la valeur de la suite créée
        valeurs_des_suites_de_cartes.append(calcul_valeur_suite(suites_de_cartes[i]))

        i += 1  # On augmente l'indice pour les prochaines suites

    # On calcule l'index de la première carte qui donne la plus grande suite (en termes de valeur)
    index_valeur_max_suite = valeurs_des_suites_de_cartes.index(max(valeurs_des_suites_de_cartes))

    # On retourne la première carte qui permet de faire la plus grande suite
    return suites_de_cartes[index_valeur_max_suite][0]
