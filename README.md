# IA_Nain_Jaune
Intelligence artificielle estimant les probabilités au tour pour le jeu du Nain Jaune. 

L'objectif prinicpal de ce programme est d'estimer les probabilités à partir d'une banque de données. Cette banque de données est construite par le programme au cours de son fonctionnement. Les commentaires inscrits dans la totalité du code aident à la compréhension de ce dernier, n'hésitez pas à vous y repporter.

## Statut du projet
Le projet est toujours en cours de développement. La majorité du code a été écrit et commenté. Actuellement, le projet tourne sous une machine distante pour augmenter la banque de données.
Les modifications prévues sont :
- Une banque de données plus grande (200 000 regrets)
- Une optimisation du code

## Installation & utilisation
Les étapes pour éxécuter le projet :
- Télécharger le code dans sa totalité
- Ouvrir le fichier ``main.py` dans un éditeur de texte
- Modifier les différents paramètres de la fonction ``lancement_jeu`` (paramètres détaillés plus loin)

### Paramètres
Les paramètres de la fonction ``lancement_jeu`` sont de l'ordre de 5. Pour modifier encore plus de choses, il faudra se rendre directement au coeur de la fonction et mettre en commentaire les lignes voulues.

Les paramètres de la fonction sont :
- ``nb_iterations`` : nombre de parties à éxécuter (type int)
- ``initialisation`` : initialisation des probabilités (type boolean)
- ``affichage`` : affichage du déroulement d'une partie (type boolean)
- ``amelioration_continue`` : amélioration des probabilités en continue (type boolean) 
- ``augmentation_data_bank`` : augmentation de la banque de données (type boolean)

### Code modifiable
Pour plus d'options, il faudra modifier le code de la fonction ``lancement_jeu``. Pour changer les modes de jeu des joueurs, il faut modifier la liste ``mode_de_jeu``. Les différents modes des joueurs sont expliqués en commentaires dans le code.

Il est aussi possible de mettre un # devant certaines lignes pour ne pas les éxécuter (mise en commentaire). _Exemple_ : si vous ne voulez pas un affichage concernant l'avancé des itérations lancées, il suffit de mettre en commentaire les lignes 55 à 58 incluses.

## Principe de fonctionnement
Le projet est basé sur un fonctionnement similaire au CFR (Counter Factual Regret) de [Poker][https://github.com/iciamyplant/Poker_CFR].
Lors d'une manche, le joueur IA effectue une certaine combinaison de stratégie. A cette stratégie est associée un regret (l'argent gagné par cette stratégie). A la fin de cette manche, le programme va refaire la manche avec le même jeu mais en testant une stratégie différente et calcule aussi le regret associé.
Toutes les stratégies sont stockées dans le fichier ``save_strategie`` et les regrets associés dans le fichier ``save_argent``. _Exemple_ : La ligne 58 de ``save_strategie`` contient la stratégie ``f0f5m6`` donc la ligne 58 de ``save_argent`` contient le regret de cette stratégie exactement.


### Calcul des probabilités
Pour calculer les probabilités, le programme fait un total des regrets de ``save_argent`` et attribue un pourcentage à chaque stratégie de ``save_strategie``. Ensuite, les probabilités sont modifiées et écrites dans ``tableau_des_proba`` à l'aide du module _pickle_.

## Problèmes rencontrés & solutions apportées
Plusieurs problèmes étaient présents et des corrections ont été codé pour y remédier.
Voici quelques soucis :
- Un bug était présent dans les fichiers de stockage des stratégies et regrets. Quelques fois, de manière aléatoire, des lignes vides apparaissaient. Pour corriger ce problème, la fonction ``verification_vide_fichier`` a été écrite et permet d'enlever des lignes vides si elles sont présentes.
- Un problème face auquel j'ai été confronté est celui du stockage des stratégies et des regrets. Le modèle présent n'est pas le premier. En effet, plusieurs solutions ont été explorées comme celle de stocker tout dans un seul fichier en mettant une séparation pour distinguer stratégie et regret. La meilleure solution retenue face à ce problème est celle présente.
- Un autre problème a été celui de calculer les probabilités. Au tout début, le programme était basé sur l'augmentation de la meilleure stratégie. Des conditions ont du être mis en place pour avoir toujours des probabilités entre 0 et 1. Ce modèle là n'était pas un modèle proche d'un CFR. Ainsi tout à dû être repensé pour avoir le plus possible un modèle proche d'un CFR.