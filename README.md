# Mini-projet SupDeVinci Travel Hub : Intégration de bases NoSQL (Redis, MongoDB, Neo4j)

## Étudiants

Souria Ranjinie VINGADASSAMY
Marine DENIS
Mathieu MORGAT

## Spécifications

//choix du langage etc

## Installation

### Les bases de données

#### Mongodb

Pour installer mongodb : https://www.mongodb.com/docs/manual/installation/

Une fois mongodb installé, on va créer la base de données nécessaire au projet :

```bash
mongosh
use sth
db.createCollection("offers")
db.offers.createIndex({ from: 1, to: 1, price: 1 })
db.offers.createIndex({ provider: "text" })
```

#### Neo4j cloud

Pour utiliser neo4j, on va se servir de sa version cloud. Pour simplifier les choses, nous allons utiliser une instance déjà créée. Vous n'avez donc rien à faire. Si vous souhaitez obtenir plus d'informations, voici le site utilisé :
https://neo4j.com/

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

### Lancer l'API

Commençons par les bases, vous avez besoin d'avoir python (ou python3) d'installé sur votre machine.
//DOC INSTALLER PYTHON

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

Lancez ensuite cette commande, elle permet de n'installer les dépendances que pour ce projet-ci :

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

Pour finir, lançons l'API avec la commande suivante :

```bash
uvicorn main:app --reload
```
