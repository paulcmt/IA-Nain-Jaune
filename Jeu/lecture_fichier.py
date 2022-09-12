# -*-coding:utf-8 -*

def chargement_fichier(nom_du_fichier):

    """
    Fonction retournant une liste de stratégie ou d'argent
    :param nom_du_fichier:
    :return:
    """

    # Initialisation de la liste qui va être retournée
    liste = []

    # On ouvre le fichier
    fichier = open(str(nom_du_fichier), 'r')
    lines = fichier.readlines()
    fichier.close()  # On ferme le fichier

    # Chaque ligne devient un élément de la liste
    for line in lines:

        liste.append(line.strip())

    # Si le fichier à charger est un fichier d'argent
    if nom_du_fichier[0] == 'a' or nom_du_fichier[6] == 'r':

        # Pour toute la liste
        for i in range(len(liste)):

            # On veut des éléments du type entier
            liste[i] = int(liste[i])

    # On retourne la liste4
    return liste
