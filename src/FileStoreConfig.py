import ConfigParser


class FileStoreConfig():

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.read_config(config_path)

    @staticmethod
    def read_config(config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        return config

    @property
    def source_directory(self):
        return self.config.get('SourceInfo', 'Source_Directory')

    @property
    def source_polling_time(self):
        return self.config.get('PollingInfo', 'Source_Polling_Time')

    @property
    def file_polling_time(self):
        return self.config.get('PollingInfo', 'File_Polling_Time')

    @property
    def dsnet_host(self):
        return self.config.get('DsNetInfo', 'Hostname')

    @property
    def dsnet_vault_type(self):
        return self.config.get('DsNetInfo', 'Vault_Type')

    @property
    def dsnet_vault_name(self):
        return self.config.get('DsNetInfo', 'Vault_Name')

    @property
    def dsnet_vault_user(self):
        return self.config.get('DsNetInfo', 'Vault_User')

    @property
    def dsnet_vault_password(self):
        return self.config.get('DsNetInfo', 'Vault_Password')

    @property
    def mongo_host(self):
        return self.config.get('MongoInfo', 'Hostname')

    @property
    def mongo_port(self):
        return self.config.get('MongoInfo', 'Port')

    @property
    def mongo_database(self):
        return self.config.get('MongoInfo', 'Database_Name')

    @property
    def mongo_collection(self):
        return self.config.get('MongoInfo', 'Collection_Name')
