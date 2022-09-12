# -*-coding:utf-8 -*

def couleur(couleur_var):

    """
    Fonction permettant de créer un jeu d'une couleur demandée
    :param couleur_var:
    :return:
    """

    assert couleur_var in (1, 2, 3, 4), "La couleur proposée n'existe pas."
    # 1 --> coeur
    # 2 --> carreau
    # 3 --> trèfle
    # 4 --> pique

    # On retourne le jeu sous forme de liste de tuple (couple)
    return [(k, couleur_var) for k in range(1, 14)]


def paquet_de_cartes():

    """
    Fonction retournant un paquet de 52 cartes
    :return:
    """

    return couleur(1) + couleur(2) + couleur(3) + couleur(4)


def nb_de_cartes_a_donner(nb_de_joueurs):

    """
    Fonction déterminant le nombre de cartes à donner par joueurs en fonction du nombre de joueurs
    :param nb_de_joueurs:
    :return:
    """

    # Les équations suivantes calculées en fonction du tableau Wikipédia
    # Objectif : clean code

    if 3 <= nb_de_joueurs <= 5:

        return -3 * nb_de_joueurs + 24

    elif 6 <= nb_de_joueurs <= 8:

        return -nb_de_joueurs + 14

    else:  # Nombre de joueurs invalide

        print("Erreur")
        return 0


def distribution_des_cartes(table_de_jeux, nb_de_cartes):

    """
    Fonction distribuant les cartes aux joueurs
    :param table_de_jeux:
    :param nb_de_cartes:
    :return:
    """

    # On distribue des cartes à tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # On distribue les cartes nécessaires
        for j in range(nb_de_cartes):

            # On memorise la carte
            carte = table_de_jeux.paquet[-1]

            # On retire la carte du paquet
            table_de_jeux.paquet.remove(carte)

            # On ajoute la carte au jeu du joueur
            table_de_jeux.liste_joueurs[i].ajout_cartes(carte)

    # Talon du jeu
    for k in range(len(table_de_jeux.paquet)):

        table_de_jeux.paquet.pop(0)  # On retire une carte du paquet

    # Va permettre de savoir si le paquet est vide ou non
    # (0, 0) indique que le paquet du jeu est vide
    table_de_jeux.paquet.append((0, 0))


def triage_des_jeux_des_joueurs(table_de_jeux):

    """
    Fonction triant les jeux des joueurs
    :param table_de_jeux:
    :return:
    """

    # Pour tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # On trie la liste de carte (le jeu du joueur)
        table_de_jeux.liste_joueurs[i].cartes_possede.sort()


def derniere_carte_du_paquet(paquet):

    """
    Fonction affichant la dernière carte du paquet
    :param paquet:
    :return:
    """

    # Affichage de la dernière carte du paquet
    print("Carte sur la table : " + str(paquet[-1]) + "\n")


def demander_une_carte():

    """
    Fonction demandant une carte à poser
    :return:
    """

    # Boucle infinie, tant que la carte à poser n'est pas un tuple
    while True:

        # Demande de saisie d'une carte
        carte_a_poser = input("Carte à poser : ")

        try:

            # Tentative de convertir l'entrée en tuple
            carte_a_poser = tuple(map(int, carte_a_poser.split(",")))

            # Si c'est réussi alors on retourne la carte
            return carte_a_poser

        except ValueError:  # Mauvaise saisie de la carte

            # Message d'erreur
            print("Veuillez saisir une carte correctement")


def tf_comparer_deux_cartes(premiere_carte, deuxieme_carte):

    """
    Fonction qui détermine si 2 cartes se suivent
    La première carte est la dernière carte du paquet
    La deuxième carte est la carte qu'on cherche à savoir si c'est la suivante
    :param premiere_carte:
    :param deuxieme_carte:
    :return:
    """

    # Si la dernière carte du paquet + 1 est égale à la carte que l'on souhaite comparer
    if premiere_carte[0] + 1 == deuxieme_carte[0]:

        return True  # La deuxième carte peut être posée

    else:

        return False  # La deuxième carte ne peut pas être posée


def tf_une_carte_possible(table_de_jeux, paquet, numero_du_joueur):

    """
    Fonction qui détermine s'il existe une carte suivant l'actuelle pour un joueur
    :param table_de_jeux:
    :param paquet:
    :param numero_du_joueur:
    :return:
    """

    if paquet[-1][0] == 0 or paquet[-1][0] == 13:  # Si la dernière carte du paquet est rien (0,0) ou un roi

        return True  # Une carte est alors possible

    # Si la dernière carte du paquet n'est pas un roi ou rien
    # alors la carte suivante doit être +1 de la carte actuelle du paquet
    else:

        # Toutes les cartes du joueur sont testés
        for i in range(len(table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede)):

            # Si la carte du joueur suit la carte actuelle
            if tf_comparer_deux_cartes(paquet[-1], table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[i]):

                return True  # Alors, il existe une carte possible

        return False  # Si aucune carte ne suit l'actuelle alors pas de carte possible


def poser_une_carte(table_de_jeux, paquet, carte_a_poser, numero_du_joueur, affichage=True):

    """
    Fonction permettant de poser une carte sur le paquet et la retirer des cartes du joueur
    :param table_de_jeux:
    :param paquet:
    :param carte_a_poser:
    :param numero_du_joueur:
    :param affichage:
    :return:
    """

    # On ajoute la carte à poser au paquet
    paquet.append(carte_a_poser)

    # On retire la carte à poser du paquet du joueur
    table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede.remove(carte_a_poser)

    # On regarde si la carte à poser est une belle carte, une carte qui rapporte de l'argent
    detection_belles_cartes(table_de_jeux, numero_du_joueur, carte_a_poser)

    if affichage:

        # Affichage de la carte posée
        print("Carte posée : ", carte_a_poser)


def verification_carte(table_de_jeux, paquet, carte_a_poser, numero_du_joueur, affichage=True):

    """
    Fonction permettant de vérifier si une carte donnée est valide
    :param table_de_jeux:
    :param paquet:
    :param carte_a_poser:
    :param numero_du_joueur:
    :param affichage:
    :return:
    """

    # Si la carte à poser est présente dans le paquet du joueur
    if carte_a_poser in table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede:

        # Si la dernière carte du paquet est un roi ou rien
        if paquet[-1] == (0, 0) or paquet[-1][0] == 13:

            # On pose la carte sur le paquet
            poser_une_carte(table_de_jeux, paquet, carte_a_poser, numero_du_joueur, affichage)

        else:  # Sinon

            # Vérification que les deux cartes se suivent
            if tf_comparer_deux_cartes(paquet[-1], carte_a_poser):

                # On pose la carte sur le paquet
                poser_une_carte(table_de_jeux, paquet, carte_a_poser, numero_du_joueur, affichage)

            else:  # Carte voulue ne suit pas la dernière carte du paquet

                print("La carte voulue ne suit pas la précédente")

        # On ajoute la carte jouée dans la liste du joueur
        table_de_jeux.liste_joueurs[numero_du_joueur].cartes_posees.append(carte_a_poser)

        # On augmente le nombre de cartes posées du joueur
        table_de_jeux.liste_joueurs[numero_du_joueur].nb_de_cartes_posees += 1

    else:  # Le joueur ne possède pas la carte dans son jeu

        print("Erreur, carte non possédée par le joueur")


def tf_cartes_en_main(table_de_jeux, numero_du_joueur):

    """
    Fonction indiquant si un joueur précisé possède encore des cartes dans son jeu
    :param table_de_jeux:
    :param numero_du_joueur:
    :return:
    """

    if len(table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede) == 0:  # Si plus de carte en main

        return False  # On retourne le fait que le joueur ne possède plus de cartes

    else:

        return True  # Le joueur possède encore des cartes


def choisir_une_carte_automatiquement(table_de_jeux, paquet, numero_du_joueur):

    """
    Fonction qui choisi une carte automatiquement en fonction de l'actuelle et des cartes d'un joueur
    :param table_de_jeux:
    :param paquet:
    :param numero_du_joueur:
    :return:
    """

    carte_a_poser = (50, 50)  # Initialisation de la carte à poser

    if paquet[-1][0] == 0 or paquet[-1][0] == 13:  # Si la dernière carte du paquet est rien ou un roi

        # Choix de la carte la plus basse parmi les cartes du joueur
        carte_a_poser = table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[0]

    else:  # Sinon (carte différente d'un roi ou rien)

        # Toutes les cartes du joueur sont testées
        for i in range(len(table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede)):

            # Si la carte testée est la suivante par rapport au paquet
            if tf_comparer_deux_cartes(paquet[-1], table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[i]):

                # Choix de la carte valide comme carte à poser
                carte_a_poser = table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[i]
                break  # On sort de la boucle, car une carte est trouvée

    return carte_a_poser  # On retourne la carte à poser


def belles_cartes(table_de_jeux, numero_du_joueur, indice_carte):

    """
    Fonction distribuant l'argent au joueur possédant une belle carte
    :param table_de_jeux:
    :param numero_du_joueur:
    :param indice_carte:
    :return:
    """

    # On crédite l'argent de la belle carte au joueur
    table_de_jeux.liste_joueurs[numero_du_joueur].argent += table_de_jeux.cartes[indice_carte]

    # On enlève l'argent de la belle carte
    table_de_jeux.cartes[indice_carte] = 0


def detection_belles_cartes(table_de_jeux, numero_du_joueur, carte_a_poser):

    """
    Fonction détectant si la carte à poser est une belle carte, si oui alors versement argent
    :param table_de_jeux:
    :param numero_du_joueur:
    :param carte_a_poser:
    :return:
    """

    # 7 de carreaux
    if carte_a_poser == (7, 2):

        # Versement de l'argent au joueur selon la belle carte
        belles_cartes(table_de_jeux, numero_du_joueur, 4)

    # Roi de cœur
    elif carte_a_poser == (13, 1):

        belles_cartes(table_de_jeux, numero_du_joueur, 3)

    # Dame de pique
    elif carte_a_poser == (12, 4):

        belles_cartes(table_de_jeux, numero_du_joueur, 2)

    # Valet de trèfle
    elif carte_a_poser == (11, 3):

        belles_cartes(table_de_jeux, numero_du_joueur, 1)

    # 10 de carreaux
    elif carte_a_poser == (10, 2):

        belles_cartes(table_de_jeux, numero_du_joueur, 0)


def verification_grand_opera(table_de_jeux):

    """
    Fonction vérifiant si un grand opera a été réalisé
    :param table_de_jeux:
    :return:
    """

    # On initialise les variables
    nb_de_joueurs_ayant_posee_une_carte = 0

    # On parcourt tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # Si le nombre de cartes posées du joueur est supérieur à 0
        if table_de_jeux.liste_joueurs[i].nb_de_cartes_posees > 0:

            # On incrémente le nombre de joueurs ayant posé au moins une carte
            nb_de_joueurs_ayant_posee_une_carte += 1

    # S'il n'y a qu'un seul joueur ayant posé une carte
    if nb_de_joueurs_ayant_posee_une_carte == 1:

        # On retourne True pour dire que la manche est un grand opéra
        return True

    # Si plusieurs joueurs ont posé au moins une carte
    else:

        # On retourne False pour dire que la manche n'est pas un grand opéra
        return False
