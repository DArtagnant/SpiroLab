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
> Réalisé par cinq étudiants de NSI en un peu plus de 3 mois, le système offre une expérience interactive et artistique soignée.

## Installation

### 1. Installation avec les fichiers compilés

Pour faciliter le lancement de l'application, des fichiers compilés pour Windows et Linux sont disponibles dans le répertoire `executable`. Il suffit de lancer l'exécutable approprié pour démarrer l'application.

**Note :** Pour Linux, il est nécessaire d'installer certaines dépendances, détaillées dans la section **Linux** ci-dessous.

### 2. Installation depuis les sources

Si vous préférez exécuter l'application depuis la source, commencez par installer les dépendances en exécutant la commande suivante :

```bash
pip install -r requirements.txt
```

Ensuite, pour lancer l'application, utilisez les commandes suivantes :

```bash
cd sources
flet run
```

### 3. Installation spécifique pour Linux

Quel que soit le mode d'installation choisi, certaines étapes supplémentaires doivent être effectuées sous Linux :

- **Installation de la librairie `zenity`** : Cette librairie est requise pour le bon fonctionnement de l'application. Pour l'installer, exécutez la commande suivante :

```bash
sudo apt-get install zenity
```

- **Enregistrement audio avec `fmedia`** : Pour enregistrer de l'audio, la bibliothèque `fmedia` est requise. Pour l'inclure, exécutez le script `link_fmedia.bash` à la racine du projet, avant de lancer l'application avec la commande flet run ou en exécutant l'exécutable depuis le même terminal.

Les commandes nécessaires pour lancer l'application depuis la source sous Linux sont donc :

```bash
bash ./link_fmedia.bash
cd sources
flet run
```

**Remarque** : Si la dépendance `fmedia` n'est pas installée, l'application fonctionnera normalement, à l'exception de la fonctionnalité d'enregistrement audio.
