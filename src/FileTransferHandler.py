import os
import time


class FileTransferHandler:
    def __init__(self, dsnet, mongodb, file_polling_time=30):
        self.dsnet = dsnet
        self.mongodb = mongodb
        self.poll_time = file_polling_time

    @staticmethod
    def remove_file(source_file):
        os.remove(source_file)

    def file_is_ready(self, source_file):
        initial_size = os.stat(source_file).st_size
        time.sleep(self.poll_time)
        post_size = os.stat(source_file).st_size
        if initial_size == post_size:
            return True
        else:
            return False

    def transfer(self, source_file):
        if not self.file_is_ready(source_file):
            print '[Skipping] Still Being Written: {0}'.format(os.path.basename(source_file))
            return

        print "[Indexing] Initializing '{0}' Mongo Entry".format(os.path.basename(source_file))
        mongo_id = self.mongodb.initialize_mongo_entry(source_file)
        print "[Indexing] Mongo Entry Initialized With Object ID: '{0}'".format(mongo_id)

        print "[Storing] Inserting '{0}' Into DsNet".format(os.path.basename(source_file))
        dsnet_id = self.dsnet.insert_into_dsnet(source_file)
        print "[Storing] Insertion Complete: DsNet ID: '{0}'".format(dsnet_id)

        print '[Indexing] Finalizing Mongo Entry'
        self.mongodb.finalize_mongo_entry(mongo_id, dsnet_id)
        print '[Indexing] Mongo Entry Finalized'

        print '[Removing] {0}'.format(os.path.basename(source_file))
        self.remove_file(source_file)
