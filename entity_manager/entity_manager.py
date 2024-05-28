import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from the .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=dotenv_path)


# Get MongoDB credentials from environment variables
db = os.getenv("DATABASE_NAME")
mongo_uri = os.getenv("MONGO_URI")
CONNECTION_STRING = mongo_uri

# Create a MongoDB client
client = MongoClient(CONNECTION_STRING)

# Create the entity manager
class EntityManager:
    def __init__(self, client, database):
        self.client = client
        self.db = database

    def get_collection(self, collection_name):
        return self.client.get_database(self.db).get_collection(collection_name)

# Instantiate the entity manager
entity_manager = EntityManager(client, db)
