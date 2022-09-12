# -*-coding:utf-8 -*

# Importation de pickle pour sauvegarder les probabilités
import pickle


def affichage_proba():

    """
    Fonction affichant les probabilités de l'intelligence artificielle
    :return:
    """

    # On ouvre le fichier des probabilités
    with open('tableau_des_proba', 'rb') as fichier:

        # On charge le tableau des probabilités dans une liste
        mon_depickler = pickle.Unpickler(fichier)
        tableau_des_proba = mon_depickler.load()

    # On calcule la longueur du tableau des probabilités
    longueur = len(tableau_des_proba)

    # On parcourt tout le fichier
    for i in range(longueur):

        # On affiche le tableau des probabilités
        print(tableau_des_proba[i])


def afficher_fichier(nom_joueur, nom_fichier):

    """
    Fonction affichant les stratégies ou l'argent relativement à un joueur
    :param nom_joueur:
    :param nom_fichier:
    :return:
    """

    # Ouverture du fichier
    with open(nom_fichier + str(nom_joueur), 'r') as fichier:

        # On charge le contenu dans une variable
        contenu = fichier.read()

    # On affiche le contenu du fichier (les stratégies ou l'argent)
    print(contenu)
