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
        # self.namespaces: dict = {"all_namespaces": [], "current_namespace": ""}

    def load_credentials(self, credentials):  # WORKS
        """

        :param credentials:
        :return:

        Load credentials to connect to consul client. Parameter is a dictionary of credentials
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
        :argument system_name of type string
        For activating the namespace you want to use
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
        :argument
        Returns dictionary of all the namespaces
        """
        return self.namespaces  # Return namespaces

    def create_namespace(self, namespace) -> None:  # WORKS
        """
        :argument namespace:
        Create a namespace for the configurations
        """
        print(self.main_namespace + namespace)  # /confo/consul - for debug
        print(self.main_namespace)  # /confo/ - for debug
        print(namespace)  # consul - for debug
        self.cons_client.kv.put(self.main_namespace + namespace, self.main_namespace + namespace)  # Putting Key & Value
        self.configurations[self.main_namespace + namespace] = {}  # Entry of namespace in configurations
        self.namespaces["all_namespaces"] = self.get_children(self.cons_client)  # Update list of namespaces
        print(self.namespaces["all_namespaces"]) # - for debug

    def get_all(self) -> dict:
        if self.find_curr_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.find_curr_namespace()]
        else:
            raise NamespaceNotLoadedException("Namespace not loaded")

    def get(self, name, field=None):
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

    def set(self, config, field, value):
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


    def get_count(self) -> int:
        return len(self.return_all())
        # return len(self.get_children(self.cons_client.return_all()))
        # get children from

    def reload(self):
        return super().reload()

    def parse_credentials(self, credentials):
        # print(credentials)
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

    def get_children(self, client):
        children = []
        x, y = client.kv.get(key='', recurse=True)
        for key in y:
            children.append(key["Key"])
        return children

    def return_all(self):
        if self.find_curr_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.find_curr_namespace()]
        else:
            raise NamespaceNotLoadedException("Namespace Not Found")

    def find_curr_namespace(self) -> str:
        return self.namespaces["current_namespace"]

    def persist(self, namespace, config):
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
        for namespace in self.namespaces["all_namespaces"]:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace) -> None:
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")

        self.namespace_config = self.configurations[namespace]
        if self.cons_client.exists(self.main_namespace + "/" + namespace):
            pass
        else:
            self.cons_client.ensure_path(self.main_namespace + "/" + namespace)

        self.use_namespace(namespace)
        for configuration in self.namespace_config:
            self.persist_configuration(namespace, configuration)
        self.use_namespace(recover_namespace)

    def persist_configuration(self, namespace, configuration) -> None:
        self.namespace_config = self.configurations[namespace]
        path = self.main_namespace + "/" + namespace + "/" + configuration
        self.cons_client.ensure_path(path)
        data = self.namespace_config[configuration]
        self.cons_client.set(path, str.encode(json.dumps(data)))
