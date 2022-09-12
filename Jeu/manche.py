# -*-coding:utf-8 -*

# Importation des librairies standards
from random import shuffle
from copy import deepcopy

# Importation des modules de jeu
from Jeu.fonction_joueurs import remise_a_zero, tour_joueur
from Jeu.cartes import distribution_des_cartes, paquet_de_cartes, triage_des_jeux_des_joueurs
from Jeu.argent import mise_normale


def manche(table_de_jeux, nb_cartes_a_donner, joueur_de_depart, strategie=None, affichage=True, regret=False):

    """
    Fonction exécutant une manche :
    - remise à zéro des variables nécessaires
    - distribution des cartes
    - mise des belles cartes
    - déroulement d'une manche complète (jeu + payement)
    :param table_de_jeux:
    :param nb_cartes_a_donner:
    :param joueur_de_depart:
    :param strategie:
    :param affichage:
    :param regret:
    :return:
    """

    # Initialisation des variables
    joueur_gagnant = 0
    i = joueur_de_depart
    nb_de_joueurs_ayant_joue = 0
    continuer_de_jouer = False
    table_de_jeux_copie = None

    # Si on n'est pas dans la partie calcul regret
    if not regret:

        # Mise à 0 des composantes des joueurs lors d'une nouvelle manche
        remise_a_zero(table_de_jeux)

        # On parcourt tous les joueurs
        for j in range(table_de_jeux.nb_de_joueurs):

            # Si le joueur est une IA
            if table_de_jeux.liste_joueurs[j].mode_de_jeu == 2:

                # On sauvegarde son argent dans un autre attribut utilisé pour les regrets
                table_de_jeux.liste_joueurs[j].argent_manche = table_de_jeux.liste_joueurs[j].argent

        # Création du paquet de cartes
        table_de_jeux.paquet = paquet_de_cartes()

        # Battage du paquet de cartes
        shuffle(table_de_jeux.paquet)

        # Distribution des cartes aux joueurs
        distribution_des_cartes(table_de_jeux, nb_cartes_a_donner)

        # Triage des jeux des joueurs
        triage_des_jeux_des_joueurs(table_de_jeux)

        # Copie de la table de jeux originale
        table_de_jeux_copie = deepcopy(table_de_jeux)

        # Mise du début de partie
        mise_normale(table_de_jeux)

        # Si on demande un affichage
        if affichage:

            # Affichage de la table
            table_de_jeux.afficher_table()

    # Les joueurs jouent tant qu'un joueur peut poser une carte ou tant que tout le monde possède des cartes
    while not continuer_de_jouer or continuer_de_jouer != "Win":

        # Le joueur ne pose aucune carte avant de commencer son tour
        table_de_jeux.liste_joueurs[i].nb_de_cartes_posees = 0

        # Si on ne calcule pas des regrets
        if not regret:

            # Le joueur en question joue son tour
            continuer_de_jouer = tour_joueur(table_de_jeux, i, affichage=affichage)

        else:  # Si on calcule des regrets

            # Le joueur en question joue son tour avec une stratégie imposée
            continuer_de_jouer = tour_joueur(table_de_jeux, i, liste_strategie=strategie, affichage=affichage)

        # Si c'est le dernier joueur qui a joué son tour
        if i == table_de_jeux.nb_de_joueurs - 1:

            i = 0  # On retourne au premier joueur

        # Sinon on passe au joueur suivant
        else:

            i += 1

        nb_de_joueurs_ayant_joue += 1  # On incrémente le nombre de joueurs ayant joué un tour

        # Si tous les joueurs ont joué un tour
        if nb_de_joueurs_ayant_joue == table_de_jeux.nb_de_joueurs:

            table_de_jeux.numero_du_tour += 1  # On incrémente le numéro du tour d'une unité
            nb_de_joueurs_ayant_joue = 0  # On remet à 0 le nombre de joueurs ayant joué un tour, car nouveau tour

    # Une fois la manche finie
    if i == 0:  # Si le joueur qui allait jouer est le premier

        # Cela veut dire que c'est le dernier joueur qui a gagné
        joueur_gagnant = table_de_jeux.nb_de_joueurs - 1

    elif 0 < i <= table_de_jeux.nb_de_joueurs - 1:

        joueur_gagnant = i - 1  # Calcul de l'indice du joueur gagnant

    # Si i est sorti de son intervalle
    else:

        # Affichage d'une erreur
        print("Erreur joueur")

    # Si la fonction n'est pas utilisée pour calculer des regrets
    if not regret:

        # On retourne :
        # Le joueur gagnant pour calculer les comptes
        # La copie de la table de jeux originale pour les regrets
        return joueur_gagnant, table_de_jeux_copie

    # Si on calcule des regrets
    else:

        # on retourne juste le joueur gagnant la manche
        return joueur_gagnant
