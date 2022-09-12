# -*-coding:utf-8 -*

# Importation de la fonction uniform pour les probabilités
from random import uniform


def calcul_strategie(tablea_des_proba, table_de_jeux):

    """
    Fonction déterminant quelle stratégie choisir selon le tableau des probabilités et le numéro du tour
    :param tablea_des_proba:
    :param table_de_jeux:
    :return:
    """

    # On charge la probabilité de finir
    proba_finir = tablea_des_proba[table_de_jeux.numero_du_tour][0]

    # On tire au "hasard" un nombre entre 0 et 1
    proba = uniform(0.0, 1.0)

    # Si la probabilité est dans l'intervalle de celle de finir
    if 0.0 <= proba <= proba_finir:

        # La stratégie sera de minimiser
        return "m"

    # Si la probabilité n'est pas dans l'intervalle de celle de finir donc dans celle de minimiser
    elif proba_finir < proba <= 1.0:

        # La stratégie sera de finir
        return "f"

    # Signalement d'erreur
    else:

        print("Erreur de probabilité")
