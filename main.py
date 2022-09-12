# -*-coding:utf-8 -*

# Importation des modules
from Jeu.menu import *
from Jeu.jeu import partie
from Jeu.ecriture_fichier import initialisation_des_proba, rogner_proba
from Jeu.affichage_fichier import *
from os import system


def lancement_jeu(nb_iterations, initialisation=False, affichage=True, amelioration_continue=False,
                  augmentation_data_bank=False):

    """
    Fonction permettant de lancer une partie complète
    :param nb_iterations:
    :param initialisation:
    :param affichage:
    :param amelioration_continue:
    :param augmentation_data_bank:
    :return:
    """

    # Si on demande une initialisation des probabilités à 50%
    if initialisation:

        # On initialise les probabilités
        initialisation_des_proba()

    # Demande des infos + récupération
    # parametres_de_la_partie = parametres_partie()
    nb_de_joueurs_voulu = 3  # parametres_de_la_partie[0]
    argent_de_depart_voulu = 120  # parametres_de_la_partie[1]

    # Mode de jeu des différents joueurs
    # 0 : mode manuel
    # 1 : mode automatique posant la carte la plus basse à chaque fois sans détection belles cartes
    # 2 : intelligence artificielle
    # 3 : mode de jeu naturel (stratégie finir tout le temps avec détection belles cartes et carte qui passe)
    mode_de_jeu = [2, 3, 3, 1, 1, 1, 1, 1]

    # On initialise la liste contenant les indices des futurs joueurs gagnants
    liste_winner = []

    # On exécute une partie le nombre de fois voulu
    for i in range(nb_iterations):

        # Lancement d'une partie
        liste_winner.append(partie(
            mode_de_jeu, affichage=affichage, nb_de_joueurs_voulu=nb_de_joueurs_voulu,
            argent_de_depart_voulu=argent_de_depart_voulu, amelioration_continue=amelioration_continue,
            augmentation_data_bank=augmentation_data_bank))

        system("cls")

        # Affichage de l'avancé
        print(str(round(float((i + 1) / nb_iterations * 100), 2)) + str(" %"))

    # On parcourt les 3 joueurs
    for j in range(1, nb_de_joueurs_voulu + 1):

        # On affiche le pourcentage de gagne du joueur
        print("Joueur " + str(j) + " : " + str(round(float(liste_winner.count(j) / nb_iterations) * 100, 2)))


lancement_jeu(1, initialisation=False, affichage=False, amelioration_continue=False, augmentation_data_bank=False)
rogner_proba()
affichage_proba()
