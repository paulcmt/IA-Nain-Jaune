# -*-coding:utf-8 -*

# Importation du module cartes
from Jeu.cartes import tf_comparer_deux_cartes, choisir_une_carte_automatiquement


def strategie_finir(table_de_jeux, paquet, numero_du_joueur):

    """
    Fonction définissant la stratégie pour ne plus avoir de cartes en main.
    Elle retourne la carte à poser.

    - Pose des cartes qui permet de passer un tour
    - Pose la carte la plus basse

    :param table_de_jeux:
    :param paquet:
    :param numero_du_joueur:
    :return:
    """

    # S'il existe une carte qui permet de passer un tour
    if len(table_de_jeux.cartes_qui_pass) > 0:

        # On va vérifier la possibilité d'une carte qui passe un tour
        for i in range(len(table_de_jeux.cartes_qui_pass)):

            # Si la carte à poser suit la dernière carte du paquet
            if tf_comparer_deux_cartes(paquet[-1], table_de_jeux.cartes_qui_pass[i]):

                # Si la carte est dans le jeu du joueur
                if table_de_jeux.cartes_qui_pass[i] in table_de_jeux.liste_joueurs[numero_du_joueur].cartes_possede:

                    # On retourne la carte
                    return table_de_jeux.cartes_qui_pass[i]

    # S'il n'existe pas de carte qui font passer un tour
    # On retourne une carte automatiquement, la plus basse
    return choisir_une_carte_automatiquement(table_de_jeux, paquet, numero_du_joueur)
