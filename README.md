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
Dans le répertoire `executable\SpiroLab-windows`, lancez `SpiroLab.exe` pour démarrer l'application.

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

### 2. Exécution depuis les sources

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

## Licence des exemples audio

Vivaldi - Violin Concerto in F minor - "Winter" - Op. 8, No. 4 - RV 297 - Arranged for Strings by GregorQuendel -- https://freesound.org/s/718662/ -- License: Attribution NonCommercial 4.0

Bach - Invention 8 in F Major, BWV 779 - Arranged for Music Box by GregorQuendel -- https://freesound.org/s/711512/ -- License: Attribution NonCommercial 4.0

Bach - Badinerie - BWV 1067 - Arranged for Flute by GregorQuendel -- https://freesound.org/s/744050/ -- License: Attribution NonCommercial 4.0