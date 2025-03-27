#!/bin/bash

# Détermine le chemin absolu de la racine du projet, ici le répertoire contenant ce script
SPIRO_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=$PATH:"$SPIRO_PATH/executable/fmedia"
echo "La PATH a été mise à jour avec $SPIRO_PATH/executable/fmedia"
