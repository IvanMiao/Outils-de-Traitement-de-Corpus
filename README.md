# Outils-de-Traitement-de-Corpus

Ce projet s'inscrit dans le cadre du cours "Outils de Traitement de Corpus" du Master 1 Plurital.

## Gestion de l'environnement

Ce projet utilise `uv` pour la gestion de l'environnement.

Pour exécuter les scripts (assurez-vous d'avoir installé `uv`):
```bash
uv run chemin/vers/le/script.py
```

## Objectif du projet

L'objectif de ce projet est d'effectuer une classification textuelle sur un corpus de poèmes chinois classiques (à l'exclusion des formes *ci(词)* et *qu(曲)*). Le but est de prédire la dynastie à laquelle un poème donné appartient.

Bien que les formes de la poésie chinoise classique soient restées relativement stables après la dynastie Tang, ce projet s'inspire de deux observations principales :

1.  **Linguistique** : Les caractéristiques linguistiques et l'usage des mots présentent des variations distinctes d'une dynastie à l'autre.

2.  **Stylistique et théorie littéraire** : En stylistique et selon la théorie littéraire chinoise ancienne, la poésie de chaque dynastie possède un style distinctif, souvent décrit comme un "zeitgeist".


## Norme

Le code de ce projet a été révisé avec `pycodestyle` pour assurer sa conformité au PEP 8.