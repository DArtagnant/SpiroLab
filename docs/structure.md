# Structure du projet

Le code du projet est divisé en 4 parties, dans le dossier "sources/".
- Dossier "assets" : contient les fichiers nécéssaires au bon fonctionnement par défaut de l'application.

- Dossier "audio" : contient le code chargé de la gestion de l'audio pur.
    - Entrée de l'audio, enregistrement du fichier ainsi que récupération des données du fichier wav (getter.py)

- Dossier "formule" : contient le code chargé des aspects plus mathématiques du projet
    - Génération de couleurs en fonction de différents paramètres (colors_creator.py)
    - Fonctions mathématiques pour des transitions plus lisses (easing.py)
    - Gestion de quelques fonctions mathématiques et des calculs dans le plan (math.py)
    - Contient la code pour la **normalisation intelligente des données** : prend une partie des données du signal et renvoie ce même signal, ramené de manière intelligente dans un intervalles de valeurs autour de la valeur référence donnée (normalisation.py)
    - Export des spirographes à l'écran au format svg (svg_creator.py) 

- Dossier "gui" : contient tout le code relatif à l'interface graphique et à l'affichage.
    - Dossier components : les composantes graphiques les plus importantes du projet
        - Un canvas entièrement adapté à nos besoins pour les spirographes en réécrivant son système de coordonnées, et optimisé au maximum en modifiant (entre autres) la bibliothèque d'interface graphique que nous utilisons (centered_canvas.py)
        - Les fonctions chargées de l'affichage des spirographes, ainsi l'algorithme chargé de **l'interpolation des points** des spirographes affichées pour une expérience graphique plus agréable (spirograph.py)
    - Gestion et articulation complète de l'architecture de l'interface graphique de l'application (render.py)
    - Les différentes pages de l'interface graphique du projet, dans les fichiers se terminant par "_page.py"
        - La page de création des spirographes personnalisés (custom_spiro_page.py)
        - La page de garde du projet (home_page.py)
        - La page chargée de l'enregistrement de l'audio et de l'import des fichiers (recorder_page.py)
        - La page chargée de l'affichage de la vidéo générée par l'audio (showroom_page.py)