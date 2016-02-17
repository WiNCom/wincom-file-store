import os.path
from pymongo import *
from filename_parser_fns import *


class MongoInterface:

    def __init__(self, config):
        self.hostname = config.mongo_hostname
        self.port = config.mongo_port
        self.database_name = config.mongo_database
        self.collection_name = config.mongo_collection
        self.mongo_collection = self._connect_to_mongo()

    def initialize_mongo_entry(self, file_to_store):
        path, filename = os.path.split(file_to_store.name)
        entry = {
            'filename': filename,
            'site': site_from_name(filename),
            'date': date_from_name(filename),
            'format': format_from_name(filename),
            'sensor': sensor_from_name(filename),
            'inserted_at': None,
            'dsnet_id': None,
        }

        if format_from_name(filename) == 'RFEye':
            if 'full_res' in path:
                entry['resolution'] = 'Full'
            elif 'low_res' in path:
                entry['resolution'] = 'Low'
            else:
                entry['resolution'] = 'Default'

        entry_id = self.mongo_collection.insert(entry)
        return entry_id

    def finalize_mongo_entry(self, mongo_id, dsnet_id):
        entry = self.mongo_collection.find_one({"_id": mongo_id})

        # You must pop the _id so mongo doesn't think you're trying to update it
        entry.pop('_id')
        entry['dsnet_id'] = dsnet_id
        entry['inserted_at'] = datetime.utcnow()

        self.mongo_collection.update({'_id': mongo_id}, {'$set': entry}, upsert=False)

        return mongo_id

    def get_dsnet_id_for_filename(self, filename):
        entry = self.mongo_collection.find_one({"filename": filename})
        if entry is not None:
            return entry['dsnet_id']
        else:
            return None

    def remove_entry_by_dsnet_id(self, dsnet_id):
        self.mongo_collection.remove({'dsnet_id': dsnet_id})

    def _connect_to_mongo(self):
        mongo = MongoClient(self.hostname, self.port)
        db_connection = mongo[self.database_name]
        collection_connection = db_connection[self.collection_name]
        return collection_connection
