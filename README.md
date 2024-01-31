# Web Crawler Project

## Description
Ce projet comprend un web crawler simple et un web crawler multithread, tous deux conçus pour explorer le web en partant d'une URL spécifique. Le crawler simple effectue des requêtes séquentielles, tandis que la version multithread utilise le multithreading pour améliorer l'efficacité du processus de crawling.

## Installation

### Prérequis
- Python 3
- BeautifulSoup4
- SQLite3 (inclus dans la bibliothèque standard de Python)
- urllib (inclus dans la bibliothèque standard de Python et ne nécessite pas d'installation séparée)

### Installation des Dépendances
Pour installer BeautifulSoup4, exécutez la commande suivante :
```bash
pip install beautifulsoup4
```

### Initialisation de la Base de Données
Si la base de données `database/crawler.db` n'a pas été créée préalablement, exécutez le script `database/create_database.py` pour initialiser la table nécessaire au fonctionnement du crawler :
```bash
python database/create_database.py
```

## Utilisation

### Crawler Simple
Pour exécuter le crawler simple, utilisez le fichier `main.py` :
```bash
python main.py
```

### Crawler Multithread
Pour exécuter le crawler multithread, utilisez le fichier `main_multithreading.py` :
```bash
python main_multithreading.py
```

## Fonctionnalités

- **Crawler Simple** : Parcourt le web en téléchargeant les pages de manière séquentielle, en respectant les règles de politesse et les fichiers `robots.txt`.

- **Crawler Multithread** : Utilise plusieurs threads pour crawler simultanément, augmentant ainsi l'efficacité du processus.

- **Respect des Normes** : Tous deux respectent un temps de courtoisie entre les requêtes et suivent les directives des fichiers `robots.txt` des sites web.

- **Stockage des Données** : Les URLs explorées sont stockées dans une base de données SQLite pour un suivi efficace.

## Structure du Projet

- `crawler/` : Contient le code du crawler simple et multithread.
- `database/` : Contient les scripts pour créer et modifier la base de données SQLite.
- `main.py` : Point d'entrée pour exécuter le crawler simple.
- `main_multithreading.py` : Point d'entrée pour exécuter le crawler multithread.

## Auteur

Ce projet a été réalisé par Sven BARRAY dans le cadre d'un cours d'Indexation Web, lors de sa troisième année du cursus ingénieur à l'ENSAI
