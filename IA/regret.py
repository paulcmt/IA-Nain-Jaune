# -*-coding:utf-8 -*

# Importation des modules nécessaires
from Jeu.argent import grand_opera_realise_belles_cartes, grand_opera_payement, payement, mise_double
from Jeu.cartes import *
from Jeu.lecture_fichier import *
from Jeu.manche import manche

# Importation de deepcopy pour la table de jeux, pickle pour sauvegarder les probabilités
from copy import deepcopy
import pickle


def autre_strategie(strategie):

    """
    Fonction retournant la stratégie inverse de la stratégie entrée
    :param strategie:
    :return:
    """

    # Si la stratégie entrée est de finir
    if strategie == 'f':

        # On retourne la stratégie de minimiser
        return 'm'

    # Si la stratégie entrée est de minimiser
    elif strategie == 'm':

        # On retourne la stratégie de finir
        return 'f'

    # Sinon
    else:

        # Signalement d'une erreur
        print("Erreur de strategie")


def manche_calcul_regret_autre_strategie(table_de_jeux, joueur_de_depart, strategie_a_changer, indice_decision):

    """
    Fonction jouant une manche avec une autre stratégie que celle jouée précédemment
    :param table_de_jeux:
    :param joueur_de_depart:
    :param strategie_a_changer:
    :param indice_decision:
    :return:
    """

    # On copie la table de jeux originale pour ne pas la modifier
    table_de_jeux_copie = deepcopy(table_de_jeux)

    # On parcourt tous les joueurs
    for a in range(table_de_jeux_copie.nb_de_joueurs):

        # Si le joueur est une IA
        if table_de_jeux_copie.liste_joueurs[a].mode_de_jeu == 2:

            # On charge les stratégies déjà exécutées
            liste_strategie = chargement_fichier('strategie' + str(table_de_jeux.liste_joueurs[a].nom))

            # On choisit la stratégie à analyser
            strategie_a_analyser = liste_strategie[strategie_a_changer]

            # Initialisation de la variable
            strategie = []

            # On calcule le nombre de stratégies contenu dans la stratégie à analyser
            longueur = len(strategie_a_analyser)

            # On parcourt toute la stratégie à analyser
            for i in range(longueur):

                # Quand on tombe sur une lettre
                if strategie_a_analyser[i].isalpha():

                    # On l'incrémente à la stratégie que l'on va tester
                    strategie.append(strategie_a_analyser[i])

            # On change la stratégie que l'on veut
            strategie[indice_decision] = autre_strategie(strategie[indice_decision])

            # On exécute une manche avec la stratégie calculée précédemment
            # On récupère le joueur gagnant
            joueur_gagnant = manche(
                table_de_jeux_copie, 0, joueur_de_depart, strategie=strategie, affichage=False, regret=True)

            # On vérifie que la manche ne soit pas un grand opéra
            grand_opera = verification_grand_opera(table_de_jeux_copie)

            # Si un grand opéra a été réalisé
            if grand_opera:

                # On calcule le joueur l'ayant réalisé
                joueur_realise_grand_opera = grand_opera_realise_belles_cartes(table_de_jeux_copie)

                # On effectue les transferts d'argent
                grand_opera_payement(table_de_jeux_copie, joueur_realise_grand_opera)

            # Si ce n'est pas un grand opéra, on effectue les payements et les mises de façon classique
            else:

                # On calcule les comptes destinés au joueur gagnant
                payement(table_de_jeux_copie, joueur_gagnant)

                # On effectue les mises des belles cartes restantes dans les jeux des joueurs si le cas échéant
                mise_double(table_de_jeux_copie)

            # On parcourt tous les joueurs
            for k in range(table_de_jeux_copie.nb_de_joueurs):

                # Si le joueur est une intelligence artificielle
                if table_de_jeux_copie.liste_joueurs[k].mode_de_jeu == 2:
                    # On calcule le regret de la manche
                    table_de_jeux_copie.liste_joueurs[k].argent_strategie = \
                        table_de_jeux_copie.liste_joueurs[k].argent \
                        - table_de_jeux_copie.liste_joueurs[k].argent_strategie

                    # On ajoute la stratégie de la manche à la liste historique
                    table_de_jeux_copie.liste_joueurs[k].historique_strategie_argent.append(
                        [table_de_jeux_copie.liste_joueurs[k].historique_strategie.copy(),
                         table_de_jeux_copie.liste_joueurs[k].argent_strategie])

            # On retourne la table de jeux pour effectuer les payements
            return table_de_jeux_copie


def calcul_augmentation_proba(num, deno):

    """
    Fonction retournant la valeur de la probabilité à augmenter
    :param num:
    :param deno:
    :return:
    """

    return float(num / deno)


def up_strategie(value, table_de_jeux, numero_du_joueur, numero_du_tour, strategie_up):

    """
    Fonction augmentant la probabilité d'une stratégie
    :param value:
    :param table_de_jeux:
    :param numero_du_joueur:
    :param numero_du_tour:
    :param strategie_up:
    :return:
    """

    # Détermination de la stratégie à diminuer
    if strategie_up == 0:  # Si la stratégie à augmenter est de finir

        strategie_down = 1  # La stratégie à diminuer est de minimiser

    elif strategie_up == 1:  # Si la stratégie à augmenter est de minimiser

        strategie_down = 0  # La stratégie à diminuer est de finir

    # Sinon, signalement d'une erreur
    else:

        strategie_down = None
        print("Erreur augmentation probabilité")

    # Si la probabilité est strictement négative
    if value < 0:

        # On augmente la probabilité de la stratégie inverse
        table_de_jeux.liste_joueurs[numero_du_joueur].tableau_des_proba[numero_du_tour][strategie_down] -= value

    # Si la probabilité est positive
    else:

        # On augmente la stratégie voulue et diminue l'autre
        table_de_jeux.liste_joueurs[numero_du_joueur].tableau_des_proba[numero_du_tour][strategie_up] += value


def amelioration_des_probabilites(table_de_jeux):

    """
    Fonction modifiant les probabilités d'un joueur IA
    :param table_de_jeux:
    :return:
    """

    # On parcourt tous les joueurs
    for d in range(table_de_jeux.nb_de_joueurs):

        # Si le joueur est une IA
        if table_de_jeux.liste_joueurs[d].mode_de_jeu == 2:

            # Initialisation des variables
            somme = 0

            # On charge les fichiers correspondant au joueur
            liste_argent = chargement_fichier("save_argent" + str(table_de_jeux.liste_joueurs[d].nom))
            liste_strategie = chargement_fichier("save_strategie" + str(table_de_jeux.liste_joueurs[d].nom))

            # On calcule le nombre de stratégies essayées
            nombre_de_strategie = len(liste_strategie)

            # On parcourt toutes les stratégies
            for a in range(nombre_de_strategie):

                # On incrémente la future moyenne
                somme += int(liste_argent[a])

            # On parcourt toutes les stratégies enregistrées
            for c in range(len(liste_strategie)):

                # Initialisation des variables
                k = 0
                nombre_de_lettres = 0

                # On récupère la stratégie
                strategie = liste_strategie[c]

                # On calcule la valeur de la probabilité que l'on va augmenter
                proba = calcul_augmentation_proba(liste_argent[c], somme)

                # On calcule le nombre de décisions dans la stratégie effectuée
                for b in range(len(strategie)):

                    # Si c'est une lettre, donc une stratégie
                    if strategie[b].isalpha():

                        # On incrémente le compteur
                        nombre_de_lettres += 1

                # On parcourt toutes les décisions prises
                for indice_k in range(nombre_de_lettres):

                    # Présence d'un bloc try / except en cas d'erreur d'index
                    try:

                        # Si la stratégie a été exécutée à un nombre de tours à 2 chiffres
                        # Possibilité d'erreur d'index, car on peut demander la dernière stratégie est
                        # donc k + 2 ne peut pas forcément exister.
                        if strategie[k + 2].isdigit():

                            # On récupère le numéro du tour de la stratégie
                            numero_du_tour = int(strategie[k+1:k+3])

                        # Sinon la stratégie a été exécutée à un nombre de tours avec un chiffre
                        else:

                            # On récupère le numéro du tour de la stratégie
                            numero_du_tour = int(strategie[k + 1])

                    # Si erreur de type Index
                    except IndexError:

                        # On récupère le numéro du tour de la stratégie
                        numero_du_tour = int(strategie[k + 1])

                    # Si la stratégie est de finir
                    if strategie[k] == 'f':

                        # On augmente la stratégie de finir avec les paramètres calculés précédemment
                        up_strategie(proba, table_de_jeux, d, numero_du_tour, 0)

                    # Si la stratégie est de minimiser
                    elif strategie[k] == 'm':

                        # On augmente la stratégie de minimiser avec les paramètres calculés précédemment
                        up_strategie(proba, table_de_jeux, d, numero_du_tour, 1)

                    # Sinon, signalement d'une erreur
                    else:

                        print("Problème augmentation probabilité")

                    # Si le numéro du tour est à un seul chiffre
                    if numero_du_tour <= 9:

                        # On passe le numéro du tour de la stratégie pour avoir la prochaine stratégie
                        k += 2

                    # Si numéro du tour est à 2 chiffres
                    else:

                        # On passe le numéro du tour (correspondant à 2 indices)
                        # de la stratégie pour avoir la prochaine stratégie
                        k += 3


def fixer_proba():

    """
    Fonction fixant les probabilités si le total des 2 probabilités ne fait pas exactement 1
    :return:
    """

    # On charge le tableau des probabilités permettant de choisir une stratégie
    with open('tableau_des_proba', 'rb') as fichier:

        mon_depickler = pickle.Unpickler(fichier)
        tableau_des_proba = mon_depickler.load()

    # On calcule la longueur du tableau des probabilités
    longueur = len(tableau_des_proba)

    # On parcourt toutes les probabilités
    for i in range(longueur):

        # On calcule la somme des probabilités des 2 stratégies d'un même tour
        somme = 0
        somme += float(tableau_des_proba[i][0])
        somme += float(tableau_des_proba[i][1])

        if somme != 1 and somme != 0:  # Si le total des 2 probabilités n'est pas égale a 1

            # On réajuste les probabilités
            tableau_des_proba[i][0] = tableau_des_proba[i][0] * 100 / somme / 100
            tableau_des_proba[i][1] = tableau_des_proba[i][1] * 100 / somme / 100

        if tableau_des_proba[i][0] == 0 and tableau_des_proba[i][1] == 0:  # Si les 2 probabilités sont nulles

            # On réajuste les probabilités
            tableau_des_proba[i][0] = 0.5
            tableau_des_proba[i][1] = 0.5

    # On réécrit les probabilités dans le fichier
    with open('tableau_des_proba', 'wb') as fichier:

        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(tableau_des_proba)
