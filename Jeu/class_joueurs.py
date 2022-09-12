# -*-coding:utf-8 -*

# Importation de pickle pour charger les probabilités
import pickle


class Joueur:

    """
    Classe définissant un joueur
    """

    def __init__(self, nom, argent, mode_de_jeu):

        self.nom = nom
        self.argent = argent
        self.mode_de_jeu = mode_de_jeu
        self.cartes_possede = []
        self.nombre_de_fois_pass = 0

        # Partie utilisée par l'intelligence artificielle
        self.cartes_posees = []
        self.nb_de_cartes_posees = 0

        # Si le joueur est une intelligence artificielle
        if self.mode_de_jeu == 2:

            # On définit des attributs nécessaires à la détermination de la stratégie à utiliser
            """ Probabilités des stratégies
            Indice 0 : finir
            Indice 1 : minimiser
            """

            self.historique_strategie_argent = []
            self.historique_strategie = []
            self.argent_strategie = 0
            self.numero_decision = 0

            # On charge le tableau des probabilités permettant de choisir une stratégie
            with open('tableau_des_proba', 'rb') as fichier:

                mon_depickler = pickle.Unpickler(fichier)
                self.tableau_des_proba = mon_depickler.load()

    def ajout_cartes(self, cartes_posees):

        """
        Méthode permettant d'ajouter une carte à un joueur
        :param cartes_posees:
        :return:
        """

        self.cartes_possede.append(cartes_posees)

    def afficher_cartes(self):

        """
        Méthode affichant les cartes d'un joueur
        :return:
        """

        print("Cartes de " + str(self.nom) + " :")

        for i in range(len(self.cartes_possede)):

            print(self.cartes_possede[i], end=' ')

        print("\n")


class TableDeJeux:

    """
    Classe définissant la table de jeux
    """

    def __init__(self, nb_de_joueurs, argent_de_depart, mode_de_jeu_complet):

        # 10 de carreaux, Valet de trèfle, Dame de pique, Roi de cœur, 7 de carreaux
        # Cette manière permet d'effectuer les mises plus simplement
        self.cartes = [0, 0, 0, 0, 0]
        self.paquet = None
        self.cartes_qui_pass = []

        self.nb_de_joueurs = nb_de_joueurs
        self.liste_joueurs = []

        self.numero_du_tour = 0

        # Ajout de l'argent de départ à tous les joueurs de la table
        for i in range(nb_de_joueurs):

            joueur = Joueur("J" + str(i+1), argent_de_depart, mode_de_jeu_complet[i])
            self.liste_joueurs.append(joueur)

    def afficher_table(self):

        """
        Méthode affichant la table de jeux
        :return:
        """

        # Affichage des belles cartes
        print("------- Table de jeux -------")
        print("7 de carreaux :", self.cartes[4])
        print("Roi de coeur :", self.cartes[3])
        print("Dame de pique :", self.cartes[2])
        print("Valet de trèfle :", self.cartes[1])
        print("10 de carreaux :", self.cartes[0])
        print("-----------------------------\n")

        # Affichage de l'argent des joueurs
        print("----- Argent des joueurs ----")

        for i in range(self.nb_de_joueurs):

            print("J" + str(i+1) + ":" + str(self.liste_joueurs[i].argent))

        print("-----------------------------\n")

    def afficher_cartes(self):

        """
        Méthode affichant les cartes des joueurs de la table
        :return:
        """

        print("-------- Cartes des joueurs --------")

        for i in range(self.nb_de_joueurs):

            print("J" + str(i+1) + " : ", end='')

            for j in range(len(self.liste_joueurs[i].cartes_possede)):

                print(self.liste_joueurs[i].cartes_possede[j], end='')

            print("\n")

        print("------------------------------------")

    def afficher_argent(self):

        """
        Méthode affichant l'argent des joueurs
        :return:
        """

        print("-------- Argent des joueurs --------")

        for i in range(self.nb_de_joueurs):

            print(self.liste_joueurs[i].nom, ":", self.liste_joueurs[i].argent)

        print("------------------------------------")
