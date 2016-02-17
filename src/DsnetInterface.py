import requests


class StorageError:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CleversafeInterface:

    def __init__(self, config):
        self.dsnet_host = config.dsnet_host
        self.dsnet_vault_type = config.dsnet_vault_type
        self.dsnet_vault_name = config.dsnet_vault_name
        self.dsnet_vault_user = config.dsnet_vault_user
        self.password = config.dsnet_vault_password

    @property
    def basic_uri(self):
        return 'http://{0}/{1}/{2}'.format(self.dsnet_host, self.dsnet_vault_type, self.dsnet_vault_name)

    def insert_into_dsnet(self, file_to_store):
        payload = file_to_store.read()

        uri = self.basic_uri

        response = requests.put(uri, data=payload, auth=(self.dsnet_vault_user, self.password),
                                headers={'content-type': 'binary'}, stream=True)

        if 'Response [201]' in str(response):
            object_id = response.content
            object_id = object_id.strip()
        else:
            raise StorageError('DSnet Insertion Failure')

        return object_id

    def get_object_from_dsnet(self, dsnet_id):
        uri = '{0}/{1}'.format(self.basic_uri, dsnet_id)

        response = requests.get(uri, auth=(self.dsnet_vault_user, self.password))

        if 'Response [200]' in str(response):
            data_object = response.content
        else:
            raise StorageError('dsNet Retrieval Failure')

        return data_object

    def remove_object_from_dsnet(self, dsnet_id):
        uri = '{0}/{1}'.format(self.basic_uri, dsnet_id)

        response = requests.delete(uri, auth=(self.dsnet_vault_user, self.password))

        if 'Response [204]' in str(response):
            return True
        else:
            return False
