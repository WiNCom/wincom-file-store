import time
import argparse

from os import listdir
from os.path import isfile, join

from FileTransferHandler import FileTransferHandler
from DsnetInterface import CleversafeInterface
from FileStoreConfig import FileStoreConfig


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', help='The path to the config file')
    return parser.parse_args()


def watch_source(source_directory, file_handler, polling_time):
    try:
        while True:
            print '\n Checking Directory {0}'.format(source_directory)

            files_found = [join(source_directory, filename) for filename in listdir(source_directory) if isfile(join(source_directory, filename))]
            if len(files_found) > 0:
                print 'Found {0} Files In Directory!'.format(len(files_found))
                for file_path in files_found:
                    file_handler.transfer(file_path)
            else:
                print 'No New Files In Directory, Sleeping...'

            time.sleep(polling_time)
    except KeyboardInterrupt:
        print 'Stopping Transfer Daemon...'


if __name__=='__main__':
    arguments = init()
    config = FileStoreConfig(arguments.config)
    cleversafe_store = CleversafeInterface(config)
    file_handler = FileTransferHandler(cleversafe_store, config)
    watch_source(config.source_directory, file_handler, config.source_polling_time)
