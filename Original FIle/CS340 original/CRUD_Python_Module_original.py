# CRUD_Python_Module.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER='aacuser', PASS='SNHU1234', HOST='localhost', PORT=27017, DB='aac', COL='animals'):
        """
        Initialize MongoClient and authenticate to MongoDB.
        Connects automatically to the aac.animals collection.
        """
        try:
            # Create the MongoDB client connection
            self.client = MongoClient(f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource={DB}")

            # Select database and collection
            self.database = self.client[DB]
            self.collection = self.database[COL]

            print("Connected to MongoDB successfully.")

        except PyMongoError as e:
            print("Error connecting to MongoDB:", str(e))
            raise e

    # -----------------------------------------------------
    # C — Create (INSERT)
    # -----------------------------------------------------
    def create(self, data):
        """
        Inserts a document into the animals collection.
        Returns True if successful, False otherwise.
        """
        if data is not None:
            try:
                result = self.collection.insert_one(data)
                return True if result.acknowledged else False

            except PyMongoError as e:
                print("Insert error:", str(e))
                return False

        else:
            raise Exception("Nothing to save, data parameter is empty")

    # -----------------------------------------------------
    # R — Read (FIND)
    # -----------------------------------------------------
    def read(self, query):
        """
        Queries documents from the animals collection.
        Returns a list of matching documents.
        Returns empty list on failure.
        """
        try:
            if query is None:
                query = {}  # return all documents if no query

            results = list(self.collection.find(query))
            return results

        except PyMongoError as e:
            print("Read error:", str(e))
            return []
