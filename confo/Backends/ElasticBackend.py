# **************************************************************************#
# Title:                    ConsulBackend                                     #
# Description:              This backend is used to handle  consul            #
#                            configurations                                 #
# Author:                   The Dream Team                                  #
# Original Date:            06 March 2021                                   #
# Update Date:              14 March 2021                                   #
# Version:                  0.1.0                                           #
# **************************************************************************#


from typing import Type
from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError
from elasticsearch import Elasticsearch

from ..Exceptions import *

class ElasticBackend(AbstractBackend):

    def __init__(self) -> None:
        '''
            Elastic Search
        '''
        self.elastic_search_client: Type[Elasticsearch] = None
        self.es_host: str = None
        self.es_port: str = None
        self.es_user: str = None
        self.es_password: str = None

        '''
            Namespaces
        '''
        self.main_namespace: str = "confo"
        self.namespace_name = None
        self.namespaces: list = []
        self.reg_namespaces: list = []

        '''
            Configurations
        '''
        self.configurations: dict = {}
        self.namespace_configs: dict = {}
        self.recover_config: dict = {}

    def load_credentials(self, credentials: dict) -> None:

        self.parse_credentials(credentials)
        
        if (self.es_user is None) or (self.es_port is None):
            raise ElasticSearchAuthError("Please supply authentication credentials")
        else:
            self.elastic_search_client = Elasticsearch(
                                                [self.es_host],
                                                http_auth=(self.es_user, self.es_password),
                                                scheme="http",
                                                port=self.es_port,
                                            )

        self.ensure_main_namespace()
        self.namespaces = self.load_namespaces()
        self.register_namespaces(self.reg_namespaces)

    def create_index(self, index, data) -> None:
        self.elastic_search_client.index(index=index, id=1, document=data)

    def namespace_exists(self, namespace) -> bool:
        return self.elastic_search_client.exists(index=namespace, id=1)

    def ensure_main_namespace(self) -> None:
        if not self.elastic_search_client.exists(index=self.main_namespace, id=1):
            self.create_index(index=self.main_namespace, data={"namespaces": []})

    def create_namespace(self, namespace: str) -> None:
        self.register_namespaces(namespaces=[namespace])

    def register_namespaces(self, namespaces) -> None:
        
        self.namespaces = self.load_namespaces()

        for namespace in namespaces:
            if not self.namespace_exists(namespace):
                self.create_index(index=namespace, data={"configurations": []})
            
            self.configurations[namespace] = {}

            print(self.configurations)
            self.namespaces.append(namespace)
            self.namespaces = list(set(self.namespaces))
            print(self.namespaces)
            
            self.create_index(index=self.main_namespace, data={"namespaces": self.namespaces})

    def load_namespaces(self) -> list:
        try:
            namespaces_from_es: dict = self.elastic_search_client.get_source(index=self.main_namespace, id=1)
            namespaces: list = namespaces_from_es['namespaces']
        except:
            raise UnknownFormatInMainNameSpace("Confo key has data with unknown format")

        return namespaces


    def parse_credentials(self, credentials: dict) -> None:

        credential_keys: list = credentials.keys()

        if 'es_user' in credential_keys:
            self.es_user = credentials['es_user']

        if 'es_password' in credential_keys:
            self.es_password = credentials['es_password']

        if 'es_host' in credential_keys:
            self.es_host = credentials['es_host']
        else:
            raise ElasticSearchHostNotFoundException('Please set "es_host" in your credentials')

        if 'es_port' in credential_keys:
            self.es_port = credentials['es_port']
        else:
            raise ElasticSearchPortNotFoundException('Please set "es_port" in your credentials')

    def use_namespace(self, system_name):
        super().use_namespace(system_name)

    def get_namespaces(self):
        return super().get_namespaces()

    def get_all(self):
        return super().get_all()

    def get(self, name, field=None):
        return super().get(name, field)

    def set(self, config, field, value):
        super().set(config, field, value)

        if (type(field) == dict or type(field) == list) and value == None:
            config_keys: list = list(self.configurations[self.namespace_name].keys())
            self.create_index(index=self.namespace_name, data={"configurations": config_keys})

    def get_count(self):
        return super().get_count()

    def persist(self, namespace, config) -> None:
        if namespace is False:
             self.persist_everything()
        elif config is False:
            self.persist_namespace(namespace=namespace)
        else:
            self.persist_configuration(namespace=namespace, configuration=config)

    def persist_everything(self) -> None:
        
        for namespace in self.get_namespaces()['all_namespaces']:
            self.persist_namespace(namespace=namespace)

    def persist_namespace(self, namespace) -> None:
        
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace {} not loaded. Load namespace with obj.use_namespace('{}')".format(namespace)
            )

        self.recover_config = self.configurations[namespace]
        
        if self.namespace_exists(namespace=namespace):
            pass
        else:
            self.create_namespace(namespace=namespace)
        
        self.use_namespace(namespace)

        for configuration_key in self.recover_config.keys():
            self.persist_configuration(namespace, configuration_key)
        self.use_namespace(recover_namespace)
        
    def persist_configuration(self, namespace, configuration_key) -> None:
        
        path = "{}-{}".format(namespace, configuration_key)
        data = self.recover_config[configuration_key]
        print(data)
        self.create_index(index=path, data=data)

    def reload(self) -> None:
        
        if not self.namespace_exists(self.main_namespace):
            raise NamespaceExistsException("Main namespace does not exist")
        
        namespaces_from_es = self.load_namespaces()

        for namespace in namespaces_from_es:

            if not self.namespace_exists(namespace=namespace):
                self.create_namespace(namespace)
            
            config_keys_from_es = self.elastic_search_client.get_source(index=namespace, id=1)['configurations']

            for config_key in config_keys_from_es:
                
                namespace_config_key = "{}-{}".format(namespace, config_key)

                if not self.namespace_exists(namespace=namespace_config_key):
                    self.create_index(index=namespace_config_key, data={})
                self.configurations[namespace] = {}
                self.configurations[namespace][config_key] = self.elastic_search_client.get_source(index=namespace_config_key, id=1)


