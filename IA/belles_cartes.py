# -*-coding:utf-8 -*

def belle_carte_in_jeu_d_un_joueur(table_de_jeux, numero_du_joueur, belle_carte, carte_a_poser):

    """
    Fonction changeant la carte à poser si la valeur d'une belle carte concorde avec
    celle de la carte à poser et que le joueur possède la belle carte
    :param table_de_jeux:
    :param numero_du_joueur:
    :param belle_carte:
    :param carte_a_poser:
    :return:
    """

    # Si le joueur possède la belle carte dans son jeu
    if belle_carte in table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede:

        # Alors la carte à poser devient la belle carte
        return belle_carte

    # Si le joueur ne possède pas la belle carte
    else:

        # La carte à poser reste la même qu'en entrée de la fonction
        return carte_a_poser


def verification_carte_belle_carte(table_de_jeux, numero_du_joueur, carte_a_poser):

    """
    Fonction vérifiant si le joueur possède une belle carte
    lorsqu'il doit poser une carte de valeur 7, roi, dame, valet ou 10
    :param table_de_jeux:
    :param numero_du_joueur:
    :param carte_a_poser:
    :return:
    """

    # Si la carte à poser est un 7
    if carte_a_poser[0] == 7:

        # La carte à poser devient la belle carte
        carte_a_poser = belle_carte_in_jeu_d_un_joueur(table_de_jeux, numero_du_joueur, (7, 2), carte_a_poser)

    # Si la carte à poser est un roi
    elif carte_a_poser[0] == 13:

        carte_a_poser = belle_carte_in_jeu_d_un_joueur(table_de_jeux, numero_du_joueur, (13, 1), carte_a_poser)

    # Si la carte à poser est une dame
    elif carte_a_poser[0] == 12:

        carte_a_poser = belle_carte_in_jeu_d_un_joueur(table_de_jeux, numero_du_joueur, (12, 4), carte_a_poser)

    # Si la carte à poser est un valet
    elif carte_a_poser[0] == 11:

        carte_a_poser = belle_carte_in_jeu_d_un_joueur(table_de_jeux, numero_du_joueur, (11, 3), carte_a_poser)

    # Si la carte à poser est un 10
    elif carte_a_poser[0] == 10:

        carte_a_poser = belle_carte_in_jeu_d_un_joueur(table_de_jeux, numero_du_joueur, (10, 2), carte_a_poser)

    return carte_a_poser  # On retourne la carte à poser
