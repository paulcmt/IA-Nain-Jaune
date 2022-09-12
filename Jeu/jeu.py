# -*-coding:utf-8 -*

# Importation des modules de jeu
from Jeu.class_joueurs import TableDeJeux
from Jeu.fonction_joueurs import joueur_de_depart_suivant
from Jeu.ecriture_fichier import *
from Jeu.argent import joueur_en_defaut, joueur_le_plus_riche

# Importation du module regret pour de l'IA
from IA.regret import *


def partie(mode, affichage=True, nb_de_joueurs_voulu=3, argent_de_depart_voulu=120, amelioration_continue=False,
           augmentation_data_bank=False):

    """
    Fonction exécutant une partie et retournant l'indice + 1 du joueur gagnant de la partie
    :param mode:
    :param affichage:
    :param nb_de_joueurs_voulu:
    :param argent_de_depart_voulu:
    :param amelioration_continue:
    :param augmentation_data_bank:
    :return:
    """

    """----------- Paramètres inchangés lors d'une partie entière -----------"""
    # Création de la table de jeu avec les différents joueurs
    table_de_jeux_voulu = TableDeJeux(nb_de_joueurs_voulu, argent_de_depart_voulu, mode)

    # Calcul du nombre de cartes à donner en fonction du nombre de joueurs
    nb_cartes_a_donner = nb_de_cartes_a_donner(nb_de_joueurs_voulu)
    """---------------------------- Fin paramètres ---------------------------"""

    # On initialise les variables
    joueur_de_depart = 0  # Le premier joueur à jouer est le joueur 1 donc indice 0

    # On joue tant que tous les joueurs peuvent miser (aucun joueur en défaut).
    while joueur_en_defaut(table_de_jeux_voulu) == 0:

        # On récupère les résultats d'une manche
        temp = manche(table_de_jeux_voulu, nb_cartes_a_donner, joueur_de_depart,
                      affichage=affichage)

        # Le gagnant est la première variable récupérée
        winner = temp[0]

        # On vérifie que la manche ne soit pas un grand opéra
        grand_opera = verification_grand_opera(table_de_jeux_voulu)

        # Si un grand opéra a été réalisé
        if grand_opera:

            # On calcule le joueur l'ayant réalisé
            joueur_realise_grand_opera = grand_opera_realise_belles_cartes(table_de_jeux_voulu)

            # On effectue les transferts d'argent
            grand_opera_payement(table_de_jeux_voulu, joueur_realise_grand_opera)

        # Si ce n'est pas un grand opéra, on effectue les payements et les mises de façon classique
        else:

            # On calcule les comptes destinés au joueur gagnant
            payement(table_de_jeux_voulu, winner)

            # On effectue les mises des belles cartes restantes dans les jeux des joueurs si le cas échéant
            mise_double(table_de_jeux_voulu)

        # On parcourt tous les joueurs
        for k in range(table_de_jeux_voulu.nb_de_joueurs):

            # Si le joueur est une intelligence artificielle
            if table_de_jeux_voulu.liste_joueurs[k].mode_de_jeu == 2:

                # On calcule le regret de la manche
                table_de_jeux_voulu.liste_joueurs[k].argent_strategie = \
                    table_de_jeux_voulu.liste_joueurs[k].argent \
                    - table_de_jeux_voulu.liste_joueurs[k].argent_strategie

                # On ajoute la stratégie de la manche à la liste historique
                table_de_jeux_voulu.liste_joueurs[k].historique_strategie_argent.append(
                    [table_de_jeux_voulu.liste_joueurs[k].historique_strategie.copy(),
                     table_de_jeux_voulu.liste_joueurs[k].argent_strategie])

        # Si affichage demandé
        if affichage:

            # On affiche l'argent des joueurs
            table_de_jeux_voulu.afficher_argent()

        if table_de_jeux_voulu.liste_joueurs[joueur_de_depart].mode_de_jeu == 2:

            # Si on décide d'augmenter la banque de données
            if augmentation_data_bank:

                # On écrit les stratégies des joueurs IA de la table dans le(s) fichier(s)
                ecriture_strategie_to_fichier(table_de_jeux_voulu)

                # On vérifie qu'il n'y ait pas de vide dans le fichier
                verification_vide_fichier(
                    'save_strategie' + str(table_de_jeux_voulu.liste_joueurs[joueur_de_depart].nom),
                    'save_argent' + str(table_de_jeux_voulu.liste_joueurs[joueur_de_depart].nom))

                # Sauvegarder stratégie / argent
                sauvegarde_strategie_argent(table_de_jeux_voulu)

                # On parcourt 70 stratégies
                for j in range(70):

                    # On parcourt 19 décisions
                    for i in range(19):

                        # Mise en place d'un bloc try / except IndexError :
                        # On ne connaît pas la longueur et le nombre de stratégies à l'avance
                        try:

                            # Replay d'une manche avec calcul des regrets par rapport à une stratégie
                            table_de_jeux_copie = manche_calcul_regret_autre_strategie(
                                temp[1], joueur_de_depart, strategie_a_changer=j, indice_decision=i)

                            # On parcourt tous les joueurs
                            for a in range(table_de_jeux_copie.nb_de_joueurs):

                                # Si le joueur est une IA
                                if table_de_jeux_copie.liste_joueurs[a].mode_de_jeu == 2:

                                    # On vérifie qu'il n'y est pas de vide dans les fichiers de données
                                    verification_vide_fichier(
                                        'save_strategie' + str(table_de_jeux_voulu.liste_joueurs[joueur_de_depart].nom),
                                        'save_argent' + str(table_de_jeux_voulu.liste_joueurs[joueur_de_depart].nom))

                                    # Sauvegarder stratégie / argent
                                    sauvegarde_strategie_argent(table_de_jeux_copie)

                        except IndexError:

                            pass

            # Si on décide d'améliorer les probabilités
            if amelioration_continue:

                # On améliore les probabilités en fonction du/des joueur(s) et de leur(s) stratégie(s)
                amelioration_des_probabilites(table_de_jeux_voulu)

                # On écrit les probabilités dans un fichier pour les sauvegarder et les réutiliser plus tard
                ecriture_des_proba(table_de_jeux_voulu)

                # On fixe les probabilités, s'il y a un problème (un vide présent)
                fixer_proba()

        # On calcule le joueur de depart pour la prochaine manche
        joueur_de_depart = joueur_de_depart_suivant(nb_de_joueurs_voulu, joueur_de_depart)

    # On calcule le joueur le plus riche à la fin de la partie
    winner = joueur_le_plus_riche(table_de_jeux_voulu)

    # On retourne l'indice du joueur + 1 pour pouvoir faire le nom si souhaité
    return winner + 1
