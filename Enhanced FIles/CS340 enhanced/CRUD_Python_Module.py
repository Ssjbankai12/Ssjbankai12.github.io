# CRUD_Python_Module.py
#
# CS 499 Milestone Four enhancement: this module adds three database-focused
# capabilities on top of the original Create/Read operations:
#   1. create_indexes()          - compound index matching the dashboard's
#                                    actual filter query pattern
#   2. get_breed_outcome_stats()  - an aggregation pipeline that computes
#                                    per-breed counts, average age, and
#                                    adoption rate
#   3. apply_schema_validation()  - enforces required fields and basic type
#                                    constraints at the database level
#
from pymongo import MongoClient, ASCENDING
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
            self.db_name = DB
            self.col_name = COL

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

    # -----------------------------------------------------
    # Enhancement: Indexing
    # -----------------------------------------------------
    def create_indexes(self):
        """
        Creates a compound index on the fields the dashboard actually
        filters on for every rescue-type query (breed, sex_upon_outcome,
        and age_upon_outcome_in_weeks). Without this index, each filtered
        query forces MongoDB to scan every document in the collection;
        with it, MongoDB can use the index to jump directly to matching
        documents instead.

        Returns the name of the created index.
        """
        try:
            index_name = self.collection.create_index(
                [
                    ("breed", ASCENDING),
                    ("sex_upon_outcome", ASCENDING),
                    ("age_upon_outcome_in_weeks", ASCENDING),
                ],
                name="breed_sex_age_idx"
            )
            print(f"Created index: {index_name}")
            return index_name

        except PyMongoError as e:
            print("Index creation error:", str(e))
            return None

    # -----------------------------------------------------
    # Enhancement: Aggregation pipeline
    # -----------------------------------------------------
    def get_breed_outcome_stats(self, query=None):
        """
        Runs an aggregation pipeline that groups the (optionally filtered)
        animal records by breed and computes, for each breed:
          - count:          number of matching records
          - avg_age_weeks:  average age at outcome, in weeks
          - adoptions:      number of records with outcome_type "Adoption"
          - adoption_rate:  adoptions / count

        This surfaces analytics the dashboard's table and pie chart do not
        provide on their own - the underlying question a shelter worker
        would ask is not just "how many of each breed matched this rescue
        type" but "which of those breeds are actually getting adopted."

        `query` is an optional filter dict, using the same shape as the
        queries already built in the dashboard's update_dashboard callback
        (e.g. limiting to the water-rescue breed list). Passing None
        aggregates over the full collection.

        Returns a list of dicts, one per breed, sorted by count descending.
        """
        pipeline = [
            {"$match": query or {}},
            {"$group": {
                "_id": "$breed",
                "count": {"$sum": 1},
                "avg_age_weeks": {"$avg": "$age_upon_outcome_in_weeks"},
                "adoptions": {
                    "$sum": {
                        "$cond": [{"$eq": ["$outcome_type", "Adoption"]}, 1, 0]
                    }
                }
            }},
            {"$addFields": {
                "breed": "$_id",
                "adoption_rate": {
                    "$cond": [
                        {"$eq": ["$count", 0]},
                        0,
                        {"$divide": ["$adoptions", "$count"]}
                    ]
                }
            }},
            {"$project": {"_id": 0}},
            {"$sort": {"count": -1}}
        ]

        try:
            return list(self.collection.aggregate(pipeline))
        except PyMongoError as e:
            print("Aggregation error:", str(e))
            return []

    # -----------------------------------------------------
    # Enhancement: Schema validation
    # -----------------------------------------------------
    def apply_schema_validation(self):
        """
        Applies a $jsonSchema validator to the animals collection so that
        MongoDB itself rejects documents missing the fields the dashboard
        depends on, instead of relying only on application code to catch
        bad data before it reaches the database.

        Uses collMod so this can be applied to the existing collection
        without needing to drop and recreate it. validationLevel is set
        to "moderate" so existing documents that predate the validator are
        not retroactively rejected, while new inserts and updates to
        matching documents are checked.
        """
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": [
                    "breed",
                    "sex_upon_outcome",
                    "age_upon_outcome_in_weeks",
                    "outcome_type",
                    "location_lat",
                    "location_long"
                ],
                "properties": {
                    "breed": {
                        "bsonType": "string",
                        "description": "breed must be a string and is required"
                    },
                    "sex_upon_outcome": {
                        "bsonType": "string",
                        "description": "sex_upon_outcome must be a string and is required"
                    },
                    "age_upon_outcome_in_weeks": {
                        "bsonType": ["double", "int"],
                        "minimum": 0,
                        "description": "age_upon_outcome_in_weeks must be a non-negative number and is required"
                    },
                    "outcome_type": {
                        "bsonType": "string",
                        "description": "outcome_type must be a string and is required"
                    },
                    "location_lat": {
                        "bsonType": ["double", "int"],
                        "description": "location_lat must be a number and is required"
                    },
                    "location_long": {
                        "bsonType": ["double", "int"],
                        "description": "location_long must be a number and is required"
                    }
                }
            }
        }

        try:
            self.database.command({
                "collMod": self.col_name,
                "validator": validator,
                "validationLevel": "moderate"
            })
            print(f"Schema validation applied to {self.db_name}.{self.col_name}")
            return True

        except PyMongoError as e:
            print("Schema validation error:", str(e))
            return False
