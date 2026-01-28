## Projet d’intelligence artificielle Finance
## Sujet 16 : Coloration de graphe et de carte (Graph/Map Coloring)

## Description de l’équipe :
Notre binôme est composé d’Elsa Bodenan et de Shaili Tuil. Dans ce projet, nous avons travaillé sur la coloration de graphes et de cartes : attribuer une couleur à chaque nœud (ou région) en évitant que deux voisins aient la même couleur, tout en cherchant à utiliser le moins de couleurs possible. Notre objectif a été de construire une solution claire et robuste, avec plusieurs méthodes de résolution (heuristiques et programmation par contraintes), et de pouvoir comparer leurs résultats et leurs performances. Dans la suite, nous expliquons le déroulement du projet, nos choix techniques et les tests réalisés.

## Objectif du projet : 
L’objectif de ce projet est de résoudre le problème de coloration de graphe (et de carte) : attribuer une couleur à chaque nœud de façon à ce que deux nœuds adjacents n’aient jamais la même couleur. 
Nous avons traité deux versions du problème : 
-Vérifier si un graphe est coloriable avec un nombre de couleurs fixé k
-Trouver le nombre minimal de couleurs nécessaire k*
En plus d’obtenir une solution correcte, nous voulions proposer un programme facile à utiliser, capable de générer des visualisations “avant/après”, d’exporter des résultats (JSON/CSV) et de comparer différentes approches en termes de qualité et de performance.

## Utilisation du programme
Notre programme peut être lancé de deux façons :
en mode interactif 
en mode non interactif 
Il génère ensuite des résultats sous forme de texte terminal, fichiers JSON, images before/after, et éventuellement un CSV de benchmark.

## Mode interactif

![Figure 9  : Lancement du programme en mode interactif : sélection de l’instance et de la méthode via l’interface terminal.](images/figure9.png)

Le programme affiche une liste d’instances possibles, puis demande :
- l’instance (map_like, erdos, grid, cycle, triangle)
- ses paramètres éventuels (n, p, seed, w, h)
- la méthode (greedy, dsatur, cp_k, cp_min, compare, benchmark)
- les options d’export (images, JSON)

## Mode non interactif

![Figure 10  : Lancement du programme en mode non interactif](images/figure10.png)
Tous les paramètres (instance, méthode, exports) sont fournis directement dans la commande. Le programme renvoie une solution valide (valid=True) et génère automatiquement les fichiers de sortie (image .png et résultat .json), ce qui garantit une exécution reproductible.


## Méthodes disponibles
- greedy
- dsatur
- cp_k
- cp_min
- compare
- benchmark

## Installation
Le projet utilise Python 3.12.
```bash
pip install -r requirements.txt
