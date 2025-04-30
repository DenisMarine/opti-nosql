# Mini-projet SupDeVinci Travel Hub : Intégration de bases NoSQL (Redis, MongoDB, Neo4j)

## Étudiants

Souria Ranjinie VINGADASSAMY
Marine DENIS
Mathieu MORGAT

## Spécifications

//choix du langage etc

## Installation

Il y aura deux méthdeds pour lancer le projet :

- Docker-compose
- Localement

### Docker

Assurez-vous d'avoir docker et docker-compose d'installé sur votre machine.

Ensuite veuillez créer un fichier `.env` à la racine du projet avec les variables d'environnement suivantes (pas besoin de setup les variables mongodb et redis, elles sont déjà configurées dans le docker-compose) :

```bash
# Connexion to neo4j cloud
NEO4J_URI=neo4j+s://94cab353.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=VANdBiMR24EfcF_BOHZ9N8GIsJ3RArR9KA2IpmccuMQ
```

Vous pouvez vous inspirer du fichier `.env.example` qui est présent dans le projet.

Pour lancer le projet, il vous suffit de lancer la commande suivante :

```bash
docker compose up --build
```

Cela va créer un conteneur avec tous les services nécessaires au bon fonctionnement de l'application (redis/mongo/api).

Vous pouvez ensuite accéder à l'application via l'url suivante : <http://localhost:8000>

### Localement

#### Prérequis

- Python 3.10.12
- pip
- MongoDB
- Redis
- Neo4j (cloud ou local)
- Postman (ou un autre client HTTP)
- Docker (si vous souhaitez utiliser docker pour mongodb et redis)

#### Setup environnement .env

Pour commencer, vous aurez besoin de variable d'environnements. Créer un .env comme suit à la racine du repo :

```bash
# Connexion to redis
REDIS_HOST={your-redis-host}
REDIS_PORT={your-redis-port}
REDIS_DB={id-base-redis}

# Connexion to mongodb
MONGODB_URI=mongodb://{your-mongodb-host}:{your-mongodb-port}
MONGODB_DB=sth

# Connexion to neo4j cloud
NEO4J_URI=neo4j+s://94cab353.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=VANdBiMR24EfcF_BOHZ9N8GIsJ3RArR9KA2IpmccuMQ
```

Vous pourrez utiliser le fichier `.env.example` comme exemple (les seules valeurs qui importent sont celles du neo4j en local).

#### Setup environnement Python

Il faut maintenant créer un environnement virtuel pour le projet, afin d'isoler les dépendances du projet des autres projets sur votre machine.

Il faut donc créer un environnement virtuel avec la commande suivante :

```bash
# Sous linux/macos
python3 -m venv venv

# Sous windows
python -m venv venv
```

Il faut ensuite activer cet environnement virtuel :

```bash
# Sous linux/macos
source venv/bin/activate

# Sous windows
venv\Scripts\activate
```

Installons maintenant les dépendances nécessaires à l'API. Elles sont toutes indiquées dans le fichier requirements.txt :

```bash
pip install -r requirements.txt
```

#### Mongodb

Pour installer mongodb : [documentation officielle](https://www.mongodb.com/docs/manual/installation/)

Une fois mongodb installé, on va créer la base de données nécessaire au projet :

```bash
mongosh

# Dans le terminal mongosh :

# - Créer la base de données
use sth

# - Créer la collection et la peupler avec le script
load("/chemin/du/projet/app/databases/populate/mongodb-init.js")
```

#### Redis

On va commencer par installer redis puis lancer le serveur :

```bash
# Sous windows ou si vous souhaitez le faire via docker
docker run --name redis -p 6379:6379 redis

# Sous linux
sudo apt install redis
sudo systemctl start redis

# Sous macos
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install redis
redis-server
```

#### Neo4j cloud

Pour utiliser neo4j, on va se servir de sa version cloud. Pour simplifier les choses, nous allons utiliser une instance déjà créée. Vous n'avez donc rien à faire. Si vous souhaitez obtenir plus d'informations, voici le site utilisé :
<https://neo4j.com/>

On va venir peupler la base qui est vide avec le script suivant (assurez vous d'avoir setup le .env et d'être dans l'environnement virtuel avec les requirements) :

```bash
# Sous linux/macos
python3 app/databases/populate/populate_neo4j.py

# Sous windows
python app/databases/populate/populate_neo4j.py
```

#### Lancer l'API

Pour lancer l'API, il vous suffit de lancer la commande suivante :

```bash
uvicorn app.main:app --reload
```

### Tester l'API

Vous pouvez tester l'API avec le client postman ou via le navigateur.

Veuillez également dans un autre terminal ouvrir un cli redis avec la commande suivante :

```bash
redis-cli SUBSCRIBE offers:new
```

Vous pourrez ainsi tester la question 5 : Notification temps réel (canal Redis Pub/Sub)

Pour tester cette route POST, vous pouvez utiliser le client postman :

```bash
# Avec Postman
(POST) http://127.0.0.1:8000/offers
```

Vous pourrez anisi utiliser le body suivant lors de votre requête :

```json
{
        "from": "PAR",
        "to": "TYO",
        "departDate": "2025-05-15T10:00:00Z",
        "returnDate": "2025-05-25T18:00:00Z",
        "provider": "AirZen",
        "price": 750.0,
        "currency": "EUR",
        "legs": [
            {
                "flightNum": "AZ123",
                "dep": "PAR",
                "arr": "TYO",
                "duration": "12h"
            },
            {
                "flightNum": "AZ124",
                "dep": "TYO",
                "arr": "PAR",
                "duration": "12h"
            }
        ],
        "hotel": null,
        "activity": null
    }
```
