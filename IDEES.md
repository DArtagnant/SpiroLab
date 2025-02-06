# Idées

On a décidé après un consortium de rester dans le thème **art**, l'idée est donc de générer des jolies images à partir de sons, qui pourront par la suite être choisis par l'utilisateur.
Etapes :

- Prendre un son (Musique ? Extrait de voix ? En temps réel ?)
- Récupérer la liste avec plein de de valeurs qui correspondent à cette musique (infos auprès de @DArtagnant)
- Pour chaque spirographe que l'on souhaite tracer :
  - Passer dans la transformée de Fourier pour récupérer plein de valeurs
  - Choisir les 5 valeurs (dans des intervalles cohérents et intéressants) qui permettront de le générer
  - Le générer
- **But :** Mettre plein de dessins de spirographes, les uns sur les autres, avec comme paramètres (i.e vitesse, rayon du cercle extérieur et intérieur) les nombres issus de la transformée de Fourier

- Peut-être imposer (à partir d'un certain nombre de spirographes) **une couleur par spirographe** ?
