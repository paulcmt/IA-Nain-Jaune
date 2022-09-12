# -*-coding:utf-8 -*

# Importation du module de jeu
from Jeu.cartes import tf_cartes_en_main, \
    tf_une_carte_possible, derniere_carte_du_paquet, demander_une_carte, verification_carte

# Importation des modules relatifs à l'IA
from IA.belles_cartes import *
from IA.strategie_finir import *
from IA.strategie_minimiser import *
from IA.strategie import *


def calcul_des_pass(table_de_jeux):

    """
    Fonction calculant le nombre de joueurs qui ont passé
    :param table_de_jeux:
    :return:
    """

    # On calcule des pass des joueurs → Savoir si tout le monde n'a pas la carte suivante
    somme_des_pass = 0  # On initialise la somme

    for i in range(table_de_jeux.nb_de_joueurs):  # On boucle pour le nombre de joueurs présents

        somme_des_pass += table_de_jeux.liste_joueurs[i].nombre_de_fois_pass  # On incrémente les pass

    return somme_des_pass  # On retourne le nombre de joueurs qui ont passé


def tour_joueur(table_de_jeux, numero_du_joueur, liste_strategie=None, affichage=True):

    """
    Fonction qui exécute le tour d'un joueur
    :param table_de_jeux:
    :param numero_du_joueur:
    :param liste_strategie:
    :param affichage:
    :return:
    """

    # Si la stratégie n'est pas donnée
    if liste_strategie is None:

        # Liste comprehension pour calculer toutes les décisions
        liste_strategie = ['a' for _ in range(20)]

    # Boucle infinie, car le joueur doit jouer tant qu'il le peut
    while True:

        if tf_cartes_en_main(table_de_jeux, numero_du_joueur):  # Si le joueur possède des cartes en main

            somme_des_pass = calcul_des_pass(table_de_jeux)  # On calcule le nombre de joueurs qui ont passé

            # S'il existe une carte suivant la dernière du paquet
            if somme_des_pass == table_de_jeux.nb_de_joueurs:  # Si tous les joueurs ont passé

                """ Le code qui suit en vert est une variante
                if paquet[-1][0] == 13:  # Si la dernière carte du paquet est un roi alors

                    paquet.append((0, 0))  # On remet le paquet à rien pour cela joue le rôle du roi

                else:  # Si il ne faut pas mettre un roi

                    paquet.append((paquet[-1][0] + 1, 0))  # On augmente la dernière carte du paquet d'une unité
                """

                # Si demande d'affichage
                if affichage:

                    print("Tout le monde a passé une fois !")

                # On ajoute la carte qui permet de passer un tour
                table_de_jeux.cartes_qui_pass.append(table_de_jeux.paquet[-1])
                table_de_jeux.cartes_qui_pass.sort()

                # On remet le paquet à vide
                table_de_jeux.paquet.append((0, 0))

            # Si le joueur peut poser une carte
            if tf_une_carte_possible(table_de_jeux, table_de_jeux.paquet, numero_du_joueur):

                # On stocke le mode de jeu dans une variable
                mode_de_jeu_joueur = table_de_jeux.liste_joueurs[numero_du_joueur].mode_de_jeu

                carte_a_poser = None  # Initialisation de la variable

                if mode_de_jeu_joueur == 0:  # Mode de jeu manuel

                    # Affichage de la dernière carte du paquet
                    derniere_carte_du_paquet(table_de_jeux.paquet)

                    # Affichage des cartes du joueur exécutant son tour
                    table_de_jeux.liste_joueurs[numero_du_joueur].afficher_cartes()

                    # Demande à l'utilisateur de choisir une carte à poser
                    carte_a_poser = demander_une_carte()

                elif mode_de_jeu_joueur == 1:  # Mode de jeu automatique

                    # Choix de la carte à poser la plus simple
                    carte_a_poser = choisir_une_carte_automatiquement(
                        table_de_jeux, table_de_jeux.paquet, numero_du_joueur)

                elif mode_de_jeu_joueur == 2:  # Mode de jeu : Intelligence artificielle

                    # Si le joueur peut décider
                    if table_de_jeux.paquet[-1][0] == 0 or table_de_jeux.paquet[-1][0] == 13:

                        try:

                            # On charge la stratégie
                            strategie = liste_strategie[table_de_jeux.liste_joueurs[numero_du_joueur].numero_decision]

                        except IndexError:  # Si pas de stratégie définit

                            strategie = 'a'  # La stratégie doit être calculée

                        # Si la stratégie doit être calculée
                        if strategie == "a":

                            # Calcul de la stratégie de l'intelligence artificielle
                            strategie = calcul_strategie(
                                table_de_jeux.liste_joueurs[numero_du_joueur].tableau_des_proba, table_de_jeux)

                        if strategie == "f":  # Si strategie est de finir

                            # On détermine la carte à poser
                            carte_a_poser = strategie_finir(table_de_jeux, table_de_jeux.paquet, numero_du_joueur)

                            # On ajoute les composantes pour l'IA
                            table_de_jeux.liste_joueurs[numero_du_joueur].historique_strategie.append(
                                str(strategie) + str(table_de_jeux.numero_du_tour))

                            # On incrémente le nombre de décisions
                            table_de_jeux.liste_joueurs[numero_du_joueur].numero_decision += 1

                        elif strategie == "m":  # Si strategie est de minimiser

                            # On détermine la carte à poser
                            carte_a_poser = strategie_minimiser(table_de_jeux, numero_du_joueur)

                            # On ajoute les composantes pour l'IA
                            table_de_jeux.liste_joueurs[numero_du_joueur].historique_strategie.append(
                                str(strategie) + str(table_de_jeux.numero_du_tour))

                            # On incrémente le nombre de décisions
                            table_de_jeux.liste_joueurs[numero_du_joueur].numero_decision += 1

                        # Sinon, signalement d'une erreur
                        else:

                            print("Erreur stratégie joueur")

                    else:

                        # Choix de la carte à poser la plus simple
                        carte_a_poser = choisir_une_carte_automatiquement(table_de_jeux, table_de_jeux.paquet,
                                                                          numero_du_joueur)

                    # Vérification existence carte à poser = belle carte
                    carte_a_poser = verification_carte_belle_carte(table_de_jeux, numero_du_joueur, carte_a_poser)

                elif mode_de_jeu_joueur == 3:  # Mode jeu d'un joueur classique

                    # On détermine la carte à poser
                    carte_a_poser = strategie_finir(table_de_jeux, table_de_jeux.paquet, numero_du_joueur)

                    # Vérification existence carte à poser = belle carte
                    carte_a_poser = verification_carte_belle_carte(table_de_jeux, numero_du_joueur, carte_a_poser)

                # Sinon, signalement d'une erreur
                else:

                    carte_a_poser = (0, 0)
                    print("Erreur de mode de jeu")

                # Vérification de la carte voulue + pose de la carte si valide (dans la fonction)
                verification_carte(table_de_jeux, table_de_jeux.paquet, carte_a_poser, numero_du_joueur,
                                   affichage)

                # Compteur de cartes passées remis à 0 pour ce tour pour tous les joueurs
                for i in range(table_de_jeux.nb_de_joueurs):

                    table_de_jeux.liste_joueurs[i].nombre_de_fois_pass = 0

            else:  # Aucune carte possible pour le joueur

                # Le joueur passe
                table_de_jeux.liste_joueurs[numero_du_joueur].nombre_de_fois_pass = 1

                # Si affichage voulu
                if affichage:

                    # Affichage de la passe du joueur
                    print(table_de_jeux.liste_joueurs[
                              numero_du_joueur].nom + " ne pose pas la carte suivante. Au joueur suivant !\n")

                return False  # Le joueur ne possède donc pas de carte valide

        else:  # Si le joueur n'a plus de cartes en main alors il a gagné

            # Si affichage voulu
            if affichage:

                # Affichage du gagnant
                print("Fin du jeu ! Le joueur " + str(
                    table_de_jeux.liste_joueurs[numero_du_joueur].nom) + " a gagné la manche !")

            return "Win"  # Le joueur ne possède donc pas de carte valide


def joueur_de_depart_suivant(nb_de_joueurs, joueur_de_depart):

    """
    Fonction permettant de passer au joueur suivant pour la prochaine manche
    :param nb_de_joueurs:
    :param joueur_de_depart:
    :return:
    """

    if joueur_de_depart == nb_de_joueurs - 1:  # Si le joueur de départ de la manche est le dernier joueur

        # Lors de la prochaine manche, c'est au joueur 1 de commencer
        return 0

    else:  # Si le joueur de départ n'est pas le dernier joueur

        # Le joueur qui commencera sera le joueur suivant
        return joueur_de_depart + 1


def remise_a_zero(table_de_jeux):

    """
    Fonction remettant à 0 les composantes des joueurs lors d'une nouvelle manche
    :param table_de_jeux:
    :return:
    """

    # On supprime toutes les cartes permettant de passer un tour
    table_de_jeux.cartes_qui_pass.clear()
    table_de_jeux.numero_du_tour = 0

    # On parcourt tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # On remet à 0 tous les attributs d'un joueur à la fin d'une manche
        table_de_jeux.liste_joueurs[i].cartes_possede.clear()
        table_de_jeux.liste_joueurs[i].cartes_posees.clear()
        table_de_jeux.liste_joueurs[i].nb_de_cartes_posees = 0
        table_de_jeux.liste_joueurs[i].nombre_de_fois_pass = 0

        # Si joueur est une IA
        if table_de_jeux.liste_joueurs[i].mode_de_jeu == 2:

            # On réinitialise les variables d'une IA
            table_de_jeux.liste_joueurs[i].historique_strategie.clear()
            table_de_jeux.liste_joueurs[i].historique_strategie_argent.clear()
            table_de_jeux.liste_joueurs[i].numero_decision = 0
            table_de_jeux.liste_joueurs[i].argent_manche = 0
