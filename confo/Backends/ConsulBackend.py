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
        self.main_namespace = "confo/"
        self.current_namespace = None
        self.namespaces: dict = {"all_namespaces": []}

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
        self.namespaces["all_namespaces"] = self.get_children(self.cons_client)
        # saving children of client into namespaces dictionary

    def use_namespace(self, system_name: str):  # WORKS
        """
        For activating the namespace you want to use
        :param system_name:
        :return:
        """
        if system_name.startswith(self.main_namespace):  # check if system name starts with "confo/"
            namespace = system_name  # if true, then the namespace is in the system
        else:
            namespace = self.main_namespace + system_name  # if false, set namespace to "confo/{system_name}"

        if namespace in self.get_namespaces()["all_namespaces"]:  # checks if namespace is in
            self.namespaces["current_namespace"] = namespace
        else:
            print("Namespace: '{}' does not exist".format(system_name))

    def get_namespaces(self) -> dict:  # WORKS
        """
        :return: dictionary of all the namespaces
        """
        return self.namespaces  # Return namespaces

    def create_namespace(self, namespace) -> None:  # WORKS
        """
        Create a namespace for the configurations
        :param namespace:
        :return:
        """
        self.cons_client.kv.put(self.main_namespace + namespace, self.main_namespace + namespace)  # Putting Key & Value
        self.configurations[self.main_namespace + namespace] = {}  # Entry of namespace in configurations
        self.namespaces["all_namespaces"] = self.get_children(self.cons_client)  # Update list of namespaces

    def get_all(self) -> dict:  # WORKS
        """
        NamespaceNotLoadedException raised when namespace does not exist or is not activated
        :return: all configurations of the activated namespace - dictionary related to the current activated namespace
        """
        if self.find_curr_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.find_curr_namespace()]
        else:
            raise NamespaceNotLoadedException("Namespace not loaded")

    def get(self, name, field=None):  # WORKS
        """
        Gets configuration of namespaces in use, and prints
        :param name:
        :param field:
        :return:
        """
        if field is not None:
            try:
                return self.configurations[self.find_curr_namespace()][name][field]
            except:
                print("Config '{}' or field '{}' is not set".format(name, field))
        else:
            try:
                return self.configurations[self.find_curr_namespace()][name]
            except:
                print("Config '{}' is not set".format(name))

    def set(self, config, field, value):  # WORKS
        """
        Creates new configuration in the current namespace
        :param config:
        :param field:
        :param value:
        :return:
        """
        if type(field) == str:
            try:
                self.configurations[self.find_curr_namespace()][config][field] = value
            except:
                self.configurations[self.find_curr_namespace()][config] = {}
                self.configurations[self.find_curr_namespace()][config][field] = value
        elif (type(field) == dict or type(field) == list) and value is None:
            try:
                self.configurations[self.find_curr_namespace()][config] = field
            except:
                pass

    def get_count(self) -> int:  # WORKS
        """
        :return: count of configurations in the activated namespace
        """
        return len(self.return_all())

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

    def get_children(self, client) -> list:  # WORKS
        """
        :param client:
        :return: list of of namespaces - returns all namespaces save in the Consul Cache
        """
        children = []
        x, y = client.kv.get(key='', recurse=True)
        if y is None:
            return []
        for key in y:
            k = key["Key"]
            if len(str(k).split("/")) == 2:  # confo/redis/sql - config  confo/redis - namespace
                children.append(key["Key"])
        return children

    def return_all(self):  # WORKS
        """
        NamespaceNotLoadedException raised when namespace does not exist or is not activated
        :return: all configurations of the activated namespace - dictionary related to the current activated namespace
        """
        if self.find_curr_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.find_curr_namespace()]
        else:
            raise NamespaceNotLoadedException("Namespace Not Found")

    def find_curr_namespace(self):  # WORKS
        """
        current working namespace as a string
        :return:
        """
        return self.namespaces["current_namespace"]

    def get_config_keys(self, client):
        """
        Finds and returns configuration keys
        :param client:
        :return:
        """
        children = []
        x, y = client.kv.get(key='', recurse=True)
        for key in y:
            k = key["Key"]
            if len(str(k).split("/")) == 3:  # confo/redis/sql - config  confo/redis - namespace
                children.append(key["Key"])
        return children

    def reload(self):
        """
        Reloads configurations from consul client into a new confo object
        :return:
        """
        config = self.get_config_keys(self.cons_client)
        for k in config:
            x, y = self.cons_client.kv.get(k)
            config_name = str(k).split("/").pop()
            try:
                self.configurations[self.find_curr_namespace()][config_name] = json.loads(x)
            except ValueError as e:
                self.configurations[self.find_curr_namespace()][config_name] = json.loads("{}")

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
        for namespace in self.namespaces["all_namespaces"]:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace) -> None:
        """
        In a namespace, we persist each configuration
        :param namespace:
        :raises NamespaceNotLoadedException - when namespace is not found in namespace list
        :return:
        """
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")

        self.namespace_config = self.configurations[namespace]
        if self.cons_client.kv.get(self.main_namespace + "/" + namespace):
            pass
        else:
            self.cons_client.kv.put(self.main_namespace + "/" + namespace, self.main_namespace + "/" + namespace)

        self.use_namespace(namespace)
        for configuration in self.namespace_config:
            self.persist_configuration(namespace, configuration)
        self.use_namespace(namespace)

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
        self.cons_client.kv.put(path, str.encode(json.dumps(data)))
