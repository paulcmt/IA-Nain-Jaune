# -*-coding:utf-8 -*

def parametres_partie():

    """
    Fonction qui définie les paramètres de la partie
    :return:
    """

    print("---------------------- Menu ----------------------")

    # On demande le nombre de joueurs
    nb_de_joueurs = input("Veuillez saisir le nombre de joueurs (3 à 8) : ")

    while True:

        if nb_de_joueurs.isdigit():  # Vérification qu'un entier a été saisi

            nb_de_joueurs = int(nb_de_joueurs)  # nb_de_joueurs devient un entier (transformation)

            if 3 <= nb_de_joueurs <= 8:  # Vérification du bon nombre de joueurs

                break

            else:  # On demande de saisir un nombre de joueurs entre 3 et 8

                print("Erreur de saisie, veuillez saisir un entier entre 3 et 8")
                nb_de_joueurs = input("Veuillez saisir le nombre de joueurs (3 à 8) : ")

        else:  # On demande de saisir un entier

            print("Erreur de saisie, veuillez saisir un entier entre 3 et 8")
            nb_de_joueurs = input("Veuillez saisir le nombre de joueurs (3 à 8) : ")

    argent_de_depart = 120  # 5*10 + 10*5 + 20*1

    print("Argent attribué à chaque joueur :", argent_de_depart)  # Affichage de l'argent de départ
    print("--------------------------------------------------\n")

    return nb_de_joueurs, argent_de_depart  # On retourne les paramètres de la partie
