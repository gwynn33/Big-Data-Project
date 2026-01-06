# Pipeline d'Analyse des Ventes Automobiles en Temps Réel
### Kafka (Docker) | PySpark Structured Streaming | ClickHouse

## 1. Présentation du Projet
Ce projet implémente un cycle complet d'ingénierie des données (End-to-End). Il simule un flux de données réelles en utilisant un Producteur Python qui envoie des messages vers un cluster Kafka conteneurisé, et un Consommateur PySpark qui transforme ces données en un Schéma en Étoile (Star Schema) stocké dans MariaDB.

L'objectif est de démontrer comment traiter des flux massifs de données tout en garantissant une structure optimisée pour l'analyse décisionnelle (BI).

## 2. Architecture du Système
Le projet est divisé en trois couches distinctes :

A. Génération des Données (Le Producteur)
- Fichier : producer.py
- Rôle : Lit les données brutes et les envoie sous format JSON vers le topic Kafka 'sales'.
- Environnement : Exécuté localement, connecté au broker Kafka tournant sur Docker.

B. Infrastructure & Messagerie (Le "Middleman")
- Technologie : Docker & Docker Compose.
- Conteneurs : Zookeeper & Kafka (Gestion des flux) et MariaDB (Entrepôt de données).
- Avantage : Environnement isolé, reproductible et scalable.

C. Traitement des Données (Le Consommateur)
- Fichier : spark_processor.py
- Rôle : S'abonne au topic Kafka, effectue des jointures, nettoie les données et applique la modélisation dimensionnelle.
- Sortie : Écrit les tables de Faits et de Dimensions dans MariaDB via JDBC.

## 3. Modélisation des Données (Schéma en Étoile)
Le flux de données est transformé pour optimiser le stockage et la rapidité des requêtes.

Dimensions :
- dim_car : Caractéristiques techniques (Modèle, Année, Couleur, etc.). Utilise un Hash MD5 de toutes les colonnes pour créer une clé unique (car_key).
- dim_junk : Regroupe les métadonnées (Région, Classification). Utilise un Hash MD5 (junk_key).

Table de Faits :
- fact_sales : Table centrale contenant les mesures (Prix, Volume, Kilométrage) et les clés étrangères vers les dimensions.

## 4. Points Forts Techniques
- Clés de Substitution Déterministes : Utilisation de MD5 pour garantir que la même config de voiture a toujours la même clé.
- Structured Streaming : Traitement des données à faible latence avec Spark.
- Tolérance aux Pannes : Implémentation de Checkpoints pour reprendre le flux sans perte de données.
- Idempotence : La conception évite les doublons dans MariaDB même en cas de réexécution.

