SameGame
========

http://www.labri.fr/perso/schlick/prog2/pro2014.html

Ecrire un programme samegame qui implémente le jeu classique du même nom (cf. la page correspondante sur Wikipedia pour plus d'infos). Il existe plusieurs versions en ligne, telle que celle-ci permettant de tester le jeu directement dans un navigateur web, pour avoir une idée de l'interface utilisateur à mettre en oeuvre.

Dans un premier temps, l'objectif est de réaliser une classe qui implémente le concept du jeu de manière abstraite, sans se préoccuper de l'interface utilisateur. Dans un second temps, on implémentera deux versions qui proposeront deux interfaces de jeu: dans la version A, le jeu utilisera une interface en mode texte (cf. exemple d'exécution ci-dessous), alors que la version B utilisera une interface graphique basée sur le module tkinter, les deux versions devront évidemment s'appuyer sur la classe initiale.

Avant de commencer à jouer, l'utilisateur doit spécifier les paramètres du jeu, c'est-à-dire la taille de la grille, ainsi que le nombre de couleurs utilisées pour les cases. La grille initiale peut être créée soit entièrement au hasard (en choisissant une couleur aléatoire pour chaque case, avec le risque d'obtenir certaines configuration où il sera impossible de gagner), soit en assurant qu'il existe effectivement une solution pour la configuration proposée. Une fois la grille créée, se met en place une boucle d'interaction dans laquelle le joueur va sélectionner une case à chaque tour, pour tenter d'éliminer l'ensemble des couleurs de la grille. La fin du jeu doit être détectée par le programme: soit lorsque la grille a été entièrement vidée, soit lorsqu'il n'y a plus de coup jouable. Enfin, pour obtenir un historique des parties jouées, on implémentera une sauvegarde sur fichier des 10 meilleurs scores réalisés pour chacune des configurations de jeu (en fonction de la taille de la grille et du nombre de couleurs).
