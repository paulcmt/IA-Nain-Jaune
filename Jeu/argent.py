# -*-coding:utf-8 -*

def joueur_en_defaut(table_de_jeux):

    """
    Fonction permettant de savoir s'il existe au moins un joueur, dans la table, en défaut (argent inférieur à 15)
    :param table_de_jeux:
    :return:
    """

    # On scan tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        if table_de_jeux.liste_joueurs[i].argent < 15:  # Si l'argent du joueur est inférieur à la mise de départ

            return 1  # On retourne 1 pour indiquer qu'il y a au moins un joueur en défaut

    # Si aucun joueur en défaut, on retourne 0
    return 0


def miser(table_de_jeux, numero_du_joueur, argent_a_miser, carte_a_miser):

    """
    Fonction permettant d'effectuer une mise sur une belle carte selon un joueur
    :param table_de_jeux:
    :param numero_du_joueur:
    :param argent_a_miser:
    :param carte_a_miser:
    :return:
    """

    # Vérification de l'argent disponible par rapport à l'argent à miser
    if table_de_jeux.liste_joueurs[numero_du_joueur].argent < argent_a_miser:

        print("Erreur, pas assez d'argent")

    else:

        # Débit de l'argent à miser
        table_de_jeux.liste_joueurs[numero_du_joueur].argent -= argent_a_miser

        # Ajout de l'argent à miser sur la belle carte
        table_de_jeux.cartes[carte_a_miser] += argent_a_miser


def mise_normale(table_de_jeux):

    """
    Fonction permettant d'effectuer la mise normale pour une manche
    :param table_de_jeux:
    :return:
    """

    # La mise se fait pour tous les joueurs de la table
    for i in range(table_de_jeux.nb_de_joueurs):

        # La mise se fait sur les 5 belles cartes
        for j in range(5):

            # On demande de miser avec :
            # le numéro du joueur = i
            # l'argent à miser qui vaut 1 de + que l'indice ou la carte est positionnée dans la table
            # l'indice de la carte
            miser(table_de_jeux, i, j+1, j)


def calcul_d_une_main(table_de_jeux, numero_du_joueur):

    """
    Fonction calculant la valeur de la main restante d'un joueur
    :param table_de_jeux:
    :param numero_du_joueur:
    :return:
    """

    valeur_main = 0  # On initialise la main à 0

    # On calcule suivant toutes les cartes que le joueur possède encore
    for i in range(len(table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede)):

        # S'il s'agit d'une carte classique
        if 1 <= table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[i][0] <= 10:

            # La valeur est incrementée de la valeur de la carte
            valeur_main += table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[i][0]

        # S'il s'agit d'une "tête" (valet, dame, roi)
        elif 11 <= table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede[i][0] <= 13:

            # La main est incrementée de 10
            valeur_main += 10

    # On renvoie la valeur de la main
    return valeur_main


def debit_credit_sur_un_joueur(table_de_jeux, joueur_a_debiter, joueur_a_crediter):

    """
    Fonction debitant le joueur qui soit payer et credite donc le joueur qui doit être credité (le gagnant)
    :param table_de_jeux:
    :param joueur_a_debiter:
    :param joueur_a_crediter:
    :return:
    """

    # Calcul de la valeur à débiter
    valeur_a_debiter = calcul_d_une_main(table_de_jeux, joueur_a_debiter)

    # Débit sur le joueur perdant
    table_de_jeux.liste_joueurs[joueur_a_debiter].argent -= valeur_a_debiter

    # Crédit sur le joueur gagnant
    table_de_jeux.liste_joueurs[joueur_a_crediter].argent += valeur_a_debiter


def payement(table_de_jeux, winner):

    """
    Fonction exécutant le payement des mains des joueurs non gagnant au joueur gagnant
    :param table_de_jeux:
    :param winner:
    :return:
    """

    # Pour tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # Sauf pour le gagnant
        if i != winner:

            # Payement du joueur perdant au joueur gagnant
            debit_credit_sur_un_joueur(table_de_jeux, i, winner)


def debit_doublage(table_de_jeux, numero_du_joueur, belle_carte):

    """
    Fonction permettant de debiter le joueur du montant de la belle carte et de doubler la belle carte
    :param table_de_jeux:
    :param numero_du_joueur:
    :param belle_carte:
    :return:
    """

    # On retire l'argent de la belle carte au joueur
    table_de_jeux.liste_joueurs[numero_du_joueur].argent -= table_de_jeux.cartes[belle_carte]

    # On double la belle carte
    table_de_jeux.cartes[belle_carte] *= 2


def mise_double(table_de_jeux):

    """
    Fonction déterminant si des belles cartes sont toujours en possession des joueurs.
    Si c'est le cas alors on double la mise de la belle carte en question
    :param table_de_jeux:
    :return:
    """

    # On scan tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # 7 de carreaux
        if (7, 2) in table_de_jeux.liste_joueurs[i].cartes_possede:

            debit_doublage(table_de_jeux, i, 4)

        # Roi de cœur
        if (13, 1) in table_de_jeux.liste_joueurs[i].cartes_possede:

            debit_doublage(table_de_jeux, i, 3)

        # Dame de pique
        if (12, 4) in table_de_jeux.liste_joueurs[i].cartes_possede:

            debit_doublage(table_de_jeux, i, 2)

        # Valet de trèfle
        if (11, 3) in table_de_jeux.liste_joueurs[i].cartes_possede:

            debit_doublage(table_de_jeux, i, 1)

        # 10 de carreaux
        if (10, 2) in table_de_jeux.liste_joueurs[i].cartes_possede:

            debit_doublage(table_de_jeux, i, 0)


def joueur_le_plus_riche(table_de_jeux):

    """
    Fonction retournant l'indice du joueur gagnant
    :param table_de_jeux:
    :return:
    """

    # On initialise la liste de l'argent des joueurs
    argent = []

    # On scan tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # On ajoute l'argent d'un joueur à la liste
        argent.append(table_de_jeux.liste_joueurs[i].argent)

    # On retourne l'index du joueur ayant le plus d'argent
    return argent.index(max(argent))


def grand_opera_realise_belles_cartes(table_de_jeux):

    """
    Fonction donnant l'argent des belles cartes au joueur ayant réalisé un grand opera
    et retournant l'indice du joueur du grand opéra
    :param table_de_jeux:
    :return:
    """

    # Initialisation des variables
    i = 0

    # On cherche à savoir qui est le joueur ayant réalisé le grand opéra
    for i in range(table_de_jeux.nb_de_joueurs):

        # Si un joueur a posé plus d'une carte alors c'est le joueur du grand opéra
        if table_de_jeux.liste_joueurs[i].nb_de_cartes_posees > 0:

            # On sort alors de la boucle
            break

    # On attribue l'argent des belles cartes au joueur en question
    for j in range(5):

        # On lui crédite l'argent des belles cartes
        table_de_jeux.liste_joueurs[i].argent += table_de_jeux.cartes[j]

        # On enlève l'argent des belles cartes
        table_de_jeux.cartes[j] = 0

    # On retourne l'indice du joueur du grand opéra
    return i


def grand_opera_payement(table_de_jeux, joueur_gagnant):

    """
    Fonction payant le joueur du grand opéra
    :param table_de_jeux:
    :param joueur_gagnant:
    :return:
    """

    # On parcourt tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # Si le joueur n'est pas le joueur du grand opéra
        if i != joueur_gagnant:

            # On retire le nombre de cartes qu'il possède à son argent
            table_de_jeux.liste_joueurs[i].argent -= len(table_de_jeux.liste_joueurs[i].cartes_possede)

            # On crédite le nombre de cartes qu'il restait au joueur au joueur du grand opéra
            table_de_jeux.liste_joueurs[joueur_gagnant].argent += len(table_de_jeux.liste_joueurs[i].cartes_possede)
