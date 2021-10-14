# ************************************************************************************#
# Title:                    ConsulBackend                                             #
# Description:              This backend is used to handle  consul                    #
#                           configurations                                            #
# Author:                   Mahlatsi Mokwele <mahlatsi.mokwele@sambeconsulting.com>   #
# Original Date:            30 August 2021                                            #
# Update Date:              30 August 2021                                            #
# Version:                  0.1.0                                                     #
# ************************************************************************************#
from typing import Type

import consul
import consulate
import consul_kv

from .AbstractBackend import AbstractBackend
from json.decoder import JSONDecodeError
from ..Exceptions import *
from consul import *
from consulate import *
from consul_kv import *
import os
import json
import socket


class ConsulBackend(AbstractBackend):
    def __init__(self):
        """
        Configurations
        """
        self.configurations: dict = {}
        self.namespace_config: dict = {}

        """
        Consul
        """
        self.cons_user = None
        self.cons_password = None
        self.DEFAULT_PORT = None
        self.DEFAULT_HOST = None
        self.DEFAULT_ADDRESS = None
        self.DEFAULT_SCHEME = None
        self.API_VERSION = None
        self.cons_client = None

        """
        Namespaces
        """
        self.namespace_name = '*'
        self.main_namespace = "confo"
        self.namespaces = []
        self.reg_namespaces = []

    def load_credentials(self, credentials):  # WORKS
        """
        Load credentials to connect to consul client. Parameter is a dictionary of credentials
        :param credentials:
        :return:
        """
        self.parse_credentials(credentials)
        if (self.cons_user is None) and (self.cons_password is None):
            self.cons_client = consul.Consul(host=self.DEFAULT_HOST,
                                             port=self.DEFAULT_PORT
                                             )  # Consul Connection
        else:
            raise ClientError("Unable to start client")
        self.ensure_main_namespace()
        self.namespaces = self.load_namespaces()
        self.register_namespaces(self.reg_namespaces)

    def create_namespace(self, namespace) -> None:  # WORKS
        """
        Create a namespace for the configurations
        :param namespace:
        :return:
        """
        self.register_namespaces(namespaces=[namespace])

    def parse_credentials(self, credentials):  # WORKS
        """
        Assign variables to values that are used to connect to the Consul client.
        :raises NotFound if host and port credentials are not defined & ConsulException if API version is not defined
        :param credentials:
        :return:
        """
        if 'default_host' in credentials.keys():
            self.DEFAULT_HOST = credentials['default_host']
        else:
            raise NotFound("Please set 'default_host' in credentials")

        if 'default_port' in credentials.keys():
            self.DEFAULT_PORT = credentials['default_port']
        else:
            raise NotFound("Please set 'default_port' in credentials")

        if 'api_version' in credentials.keys():
            self.API_VERSION = credentials['api_version']
        else:
            raise ConsulException("Please set 'api_version' in credentials")

        if 'default_scheme' in credentials.keys():
            self.DEFAULT_SCHEME = credentials['default_scheme']
        else:
            raise ConsulException("Please set 'default_scheme' in credentials")

    def reload(self):
        """
        Reloads configurations from consul client into a new confo object
        :return:
        """
        self.configurations[self.namespace_name] = {}
        try:
            config = json.loads(self.cons_client.kv.get(self.namespace_name)[0])["configurations"]
            for config in config:
                path = self.namespace_name + "/" + config
                data = self.cons_client.kv.get(path)[0]
                if data.decode('utf-8').strip() == '':
                    data = "{}"
                try:
                    self.configurations[self.namespace_name][config] = json.loads(data)
                except ValueError as e:
                    self.configurations[self.namespace_name][config] = json.loads("{}")
        except:
            raise Exception("Unknown Format In Namespace '%s' key" % self.namespace_name)

    def check_key(self, key_name):
        """
        Checks if a key exists in a given Consul instance.
        :param key_name:
        :return:
        """
        if self.cons_client.kv.get(key_name) == (None, None):
            return False
        else:
            return True

    def ensure_main_namespace(self):
        """
        Checks if the main namespace, Confo, exists. If not, it creates the namespace with an empty list of children
        :return:
        """
        if not self.check_key(self.main_namespace):
            self.cons_client.kv.put(self.main_namespace, json.dumps({"namespaces": []}))

    def load_namespaces(self):
        """
        Loads a list of namespaces from the main namespace list
        :return:
        """
        try:
            values = json.loads(self.cons_client.kv.get(self.main_namespace)[0])
            namespaces = values["namespaces"]
        except:
            raise UnknownFormatInMainNameSpace("Confo Key Has Data With Unknown Format")

        return namespaces

    def register_namespaces(self, namespaces):
        """

        :param namespaces:
        :return:
        """
        self.namespaces = self.load_namespaces()
        for namespace in namespaces:
            if not self.check_key(namespace):
                self.cons_client.kv.put(namespaces, json.dumps({"configurations": []}))
                print(namespace)
            self.namespaces.append(namespaces)

        self.namespaces = list(set(self.namespaces))
        self.cons_client.kv.put(self.main_namespace, json.dumps({"namespaces": self.namespaces}))

    def persist(self, namespace, config):  # WORKS
        """
        Saves all configurations to consul cache
        :param namespace:
        :param config:
        :return:
        """
        if not namespace:
            # Persist everything
            self.persist_everything()
        elif not config:
            # persist the entire namespace if exists
            self.persist_namespace(namespace)
        else:
            # persist just one configuration file
            self.persist_configuration(namespace, config)

    def persist_everything(self) -> None:
        """
        loops through all namespaces and persist all namespaces in the list of namespaces
        :return:
        """
        for namespace in self.namespaces:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace) -> None:
        """
        In a namespace, we persist each configuration
        :param namespace:
        :raises NamespaceNotLoadedException - when namespace is not found in namespace list
        :return:
        """
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")

        self.namespace_config = self.configurations[namespace]
        if self.check_key(namespace):
            pass
        else:
            self.create_namespace(namespace)

        self.use_namespace(namespace)
        for configuration in self.namespace_config:
            self.persist_configuration(namespace, configuration)
        self.use_namespace(recover_namespace)

    def persist_configuration(self, namespace, configuration) -> None:
        """
        Extracts configurations of a specified namespace and saves them in consul cache
        :param namespace:
        :param configuration:
        :return:
        """
        self.namespace_config = self.configurations[namespace]
        path = namespace + "/" + configuration
        data = self.namespace_config[configuration]
        self.cons_client.kv.put(path, json.dumps(data))
