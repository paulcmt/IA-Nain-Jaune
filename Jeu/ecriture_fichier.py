# -*-coding:utf-8 -*

# Importation de pickle pour modifier ou lire les probabilités
import pickle

# Importation du module lecture_fichier pour charger des fichiers
from Jeu.lecture_fichier import *


def initialisation_des_proba():

    """
    Fonction permettant d'initialiser les probabilités d'une intelligence artificielle
    :return:
    """

    # Initialisation du tableau des probabilités
    tableau_des_proba = []

    # 35 itérations, car nombre de tours max sur 10 000 itérations était de 17
    for i in range(20):

        # Les probabilités initiales sont de 50% pour chaque stratégie
        tableau_des_proba.append([0.0, 0.0])

    # Une fois le tableau créé on l'écrit dans un fichier
    with open('tableau_des_proba', 'wb') as fichier:

        # On sauvegarde l'objet lui-même dans le fichier des probabilités
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(tableau_des_proba)


def ecriture_des_proba(table_de_jeux):

    """
    Fonction écrivant les probabilités dans un fichier
    :param table_de_jeux:
    :return:
    """

    i = 0

    # On parcourt tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # On cherche l'indice d'une intelligence artificielle
        if table_de_jeux.liste_joueurs[i].mode_de_jeu == 2:

            break  # On sort de la boucle

    # On charge le tableau des probabilités du joueur IA dans une liste
    tableau_des_proba = table_de_jeux.liste_joueurs[i].tableau_des_proba

    # Ouverture du fichier en W binaire
    with open('tableau_des_proba', 'wb') as fichier:

        # On sauvegarde l'objet dans le fichier des probabilités
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(tableau_des_proba)


def ecriture_strategie_to_fichier(table_de_jeux, mode='w'):

    """
    Fonction écrivant les stratégies d'une table dans un fichier
    :param table_de_jeux:
    :param mode:
    :return:
    """

    # On parcourt tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # Si joueur IA
        if table_de_jeux.liste_joueurs[i].mode_de_jeu == 2:

            # On crée les éléments à enregistrer
            toprint1 = "".join(table_de_jeux.liste_joueurs[i].historique_strategie_argent[-1][0])
            toprint2 = str(table_de_jeux.liste_joueurs[i].historique_strategie_argent[-1][1])

            # On ouvre le fichier des stratégies avec le mode souhaité
            with open('strategie' + str(table_de_jeux.liste_joueurs[i].nom), mode) as fichier:

                fichier.write(toprint1 + '\n')  # On écrit la stratégie

            # On ouvre le fichier des stratégies avec le mode souhaité
            with open('argent' + str(table_de_jeux.liste_joueurs[i].nom), mode) as fichier:

                fichier.write(toprint2 + '\n')  # On écrit l'argent du regret


def verification_vide_fichier(fichier_strategie, fichier_argent):

    """
    Fonction éliminant les vides dans des fichiers donnés
    :param fichier_strategie:
    :param fichier_argent:
    :return:
    """

    # On charge le fichier stratégie
    strategie_liste = chargement_fichier(fichier_strategie)

    # On compte le nombre de vides présent dans le fichier
    nb_de_vide = strategie_liste.count('')

    # Si il y a au moins un vide
    if nb_de_vide != 0:

        # On charge le fichier argent
        argent_liste = chargement_fichier(fichier_argent)

        # On parcourt tous les vides
        for i in range(nb_de_vide):

            # On enlève un vide dans les 2 fichiers
            argent_liste.pop(strategie_liste.index(''))
            strategie_liste.remove('')

        with open(fichier_argent, 'w') as fichier:

            # On parcourt tous les regrets
            for a in range(len(argent_liste)):

                # On réécrit le regret
                fichier.write(str(argent_liste[a]) + '\n')

        with open(fichier_strategie, 'w') as fichier:

            # On parcourt toutes les stratégies
            for a in range(len(strategie_liste)):

                # On réécrit la stratégie
                fichier.write(str(strategie_liste[a]) + '\n')


def sauvegarde_strategie_argent(table_de_jeux):

    """
    Fonction permettant d'améliorer les regrets et stratégies
    :param table_de_jeux:
    :return:
    """

    # On parcourt tous les joueurs
    for i in range(table_de_jeux.nb_de_joueurs):

        # Si joueur IA
        if table_de_jeux.liste_joueurs[i].mode_de_jeu == 2:

            # On crée les éléments à enregistrer
            toprint1 = "".join(table_de_jeux.liste_joueurs[i].historique_strategie_argent[-1][0])

            # On charge les fichiers de sauvegarde dans des listes
            save_strategie = chargement_fichier('save_strategie' + str(table_de_jeux.liste_joueurs[i].nom))
            save_argent = chargement_fichier('save_argent' + str(table_de_jeux.liste_joueurs[i].nom))

            # Si la stratégie est déjà enregistrée
            if toprint1 in save_strategie:

                # Initialisation de l'indice
                j = 0

                # On parcourt toutes les stratégies enregistrées
                for j in range(len(save_strategie)):

                    # On cherche l'indice de la stratégie correspondant à l'argent associé
                    if toprint1 == save_strategie[j]:

                        break
                try:

                    # On incrémente le regret de la stratégie
                    save_argent[j] += int(table_de_jeux.liste_joueurs[i].historique_strategie_argent[-1][1])

                except IndexError:

                    continue

                # On réécrit les regrets dans le fichier de sauvegarde
                with open('save_argent' + str(table_de_jeux.liste_joueurs[i].nom), 'w') as fichier:

                    # On parcourt tous les regrets
                    for a in range(len(save_argent)):

                        # On écrit le regret
                        fichier.write(str(save_argent[a]) + '\n')

            # Si la stratégie est nouvelle, donc pas enregistrée dans le fichier
            if not (toprint1 in save_strategie):

                # On écrit la stratégie et le regret associé
                ecriture_strategie_to_fichier(table_de_jeux, mode='a')

                # On crée le regret à enregistrer
                toprint2 = str(table_de_jeux.liste_joueurs[i].historique_strategie_argent[-1][1])

                # On écrit la stratégie
                with open('save_strategie' + str(table_de_jeux.liste_joueurs[i].nom), 'a') as fichier:

                    fichier.write(toprint1 + '\n')

                # On écrit le regret associé à la stratégie
                with open('save_argent' + str(table_de_jeux.liste_joueurs[i].nom), 'a') as fichier:

                    fichier.write(toprint2 + '\n')


def rogner_proba():

    """
    Fonction arrondissant les probabilités à 3 décimales
    :return:
    """

    # On charge le tableau des probabilités permettant de choisir une stratégie
    with open('tableau_des_proba', 'rb') as fichier:

        mon_depickler = pickle.Unpickler(fichier)
        tableau_des_proba = mon_depickler.load()

    # On parcourt tout le tableau
    for i in range(20):

        # On arrondit les probabilités du tour
        tableau_des_proba[i][0] = round(tableau_des_proba[i][0], 3)
        tableau_des_proba[i][1] = round(tableau_des_proba[i][1], 3)

    # Une fois le tableau créé on l'écrit dans un fichier
    with open('tableau_des_proba', 'wb') as fichier:

        # On sauvegarde l'objet lui-même dans le fichier des probabilités
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(tableau_des_proba)
