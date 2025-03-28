```text
███████╗██████╗ ██╗██████╗  ██████╗ ██╗      █████╗ ██████╗ 
██╔════╝██╔══██╗██║██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗
███████╗██████╔╝██║██████╔╝██║   ██║██║     ███████║██████╔╝
╚════██║██╔═══╝ ██║██╔══██╗██║   ██║██║     ██╔══██║██╔══██╗
███████║██║     ██║██║  ██║╚██████╔╝███████╗██║  ██║██████╔╝
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ 
```

## Résumé

> SpiroLab allie art et informatique en animant des spirographes grâce au son.
> En modifiant six paramètres, l’application génère des tracés précis et élégants.
> Elle permet d’importer un fichier .wav ou d’enregistrer un son en direct pour créer une chorégraphie colorée via une interface intuitive.
> Réalisé par cinq élèves de 1ère NSI en un peu plus de 3 mois, le système offre une expérience interactive et artistique soignée.

## Installation

Le projet a été testé et fonctionne avec `Python 3.12`. Des versions de python plus anciennes ne sont pas forcément compatibles.

### Utilisation sous Windows

#### 1. Exécution du fichier compilé
Dans le répertoire `executable\SpiroLab-windows`, lancez `spirolab.exe` pour démarrer l'application.

#### 2. Exécution depuis les sources

Installez les dépendances avec la commande
```cmd
pip install -r requirements.txt
```

Lancez la commande `flet run` depuis le répertoire `sources` :
```cmd
cd sources
flet run
```

### Utilisation sous Linux

#### Prérequis
La librairie `zenity` est requise pour le bon fonctionnement de l'application (widget de sélection de fichier). Pour l'installer, exécutez la commande :

```bash
sudo apt-get install zenity
```

#### 1. Exécution du fichier compilé

Lancer ces commandes depuis la racine du projet:
```bash
export PATH=$PATH:"$(pwd)/executable/fmedia":"$(pwd)/../executable/fmedia":"$(pwd)/../../executable/fmedia"
cd executable/SpiroLab-linux
./SpiroLab
```

Remarque : la ligne `export` permet d'activer la capacité à enregistrer de l'audio. Sans cette ligne, l'application fonctionne correctement hormis l'enregistrement d'audio.

#### 2. Exécution depuis les sources

Installez les dépendances avec la commande
```bash
pip install -r requirements.txt
```

Lancez la commande `flet run` depuis le répertoire `sources` :
```bash
export PATH=$PATH:"$(pwd)/executable/fmedia":"$(pwd)/../executable/fmedia":"$(pwd)/../../executable/fmedia"
cd sources
flet run
```

### Dépendances
Notre projet dépend pour la plus grande partie des parties de la bibliothèque standard de python : pas besoin d'installation particulières pour ceux-là. Nous utilisons 3 autres bibliothèques :
- [Numpy](https://numpy.org/), pour faire des calculs plus rapides et complexes sur les longues listes extraites des fichiers audio.
- [Flet](https://flet.dev/) et [Flet-audio-recorder](https://pypi.org/project/flet-audio-recorder/), pour la gestion de l'interface graphique et de l'entrée d'audio au sein de cette bibliothèque d'interface graphique.

#### Pourquoi [Flet](https://flet.dev/) ?
Nous avons choisi d'utiliser Flet au lieu de bibliothèques plus classiques comme Tkinter afin de pouvoir construire facilement une application qui peut s'éxécuter sur toutes les plateformes (y compris possiblement le web), et qui est plus moderne par défaut dans son design.

## Licences
Le code dans le répertoire `sources` est sous licence GNU GPLv3 et la documentation est sous licence CC BY-SA.

Les fichiers dans `executable` sont sous leurs licences respectives.

### Musiques présentes dans `data`

Vivaldi - Violin Concerto in F minor - "Winter" - Op. 8, No. 4 - RV 297 - Arranged for Strings by GregorQuendel -- https://freesound.org/s/718662/ -- License: Attribution NonCommercial 4.0

Bach - Invention 8 in F Major, BWV 779 - Arranged for Music Box by GregorQuendel -- https://freesound.org/s/711512/ -- License: Attribution NonCommercial 4.0

Bach - Badinerie - BWV 1067 - Arranged for Flute by GregorQuendel -- https://freesound.org/s/744050/ -- License: Attribution NonCommercial 4.0