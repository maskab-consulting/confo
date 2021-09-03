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
        self.configurations = {}
        self.namespace_config = {}
        self.cons_user = None
        self.cons_password = None
        self.DEFAULT_ENDPOINT = None
        self.DEFAULT_KV_ENDPOINT = None
        self.DEFAULT_TXN_ENDPOINT = None
        self.DEFAULT_PORT = None
        self.DEFAULT_HOST = None
        self.DEFAULT_ADDRESS = None
        self.DEFAULT_TOKEN = None
        self.API_VERSION = None
        # self.DEFAULT_REQUEST_TIMEOUT = socket._GLOBAL_DEFAULT_TIMEOUT
        self.cons_client = None
        self.namespace_name = '*'
        self.main_namespace = "/confo/"
        self.namespaces = {"all_namespaces": [], "current_namespace": ""}
        self.curr_namespace = None

    def load_credentials(self, credentials):
        self.parse_credentials(credentials)
        if (self.cons_user is None) and (self.cons_password is None):
            self.cons_client = consul.Consul(host=self.DEFAULT_HOST, port=self.DEFAULT_PORT)
        else:
            raise ClientError("Unable to start client")

        self.namespaces["all_namespaces"] = self.get_children()

    def use_namespace(self, system_name):
        namespace = self.main_namespace + system_name
        if namespace in self.get_namespaces():
            self.curr_namespace = namespace
        else:
            return {'message': "Namespace '{}' not found".format(system_name)}

    def get_namespaces(self):
        return self.namespaces

    def create_namespace(self, namespace):
        root = self.main_namespace + namespace
        self.cons_client.set(root, "null")
        self.configurations[root] = {}
        self.namespaces["all_namespaces"] = self.cons_client.get(key='', recurse=True)

    def get_all(self):
        if self.find_curr_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.find_curr_namespace()]
        else:
            raise NamespaceNotLoadedException("Namespace not loaded")

    def get(self, name, field=None):
        return super().get(name, field)

    def set(self, config, field, value):
        super().set(config, field, value)

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

    def get_count(self):
        return super().get_count()

    def reload(self):
        return super().reload()

    def parse_credentials(self, credentials):
        if 'default_endpoint' in credentials.keys():
            self.DEFAULT_ENDPOINT = credentials['default_endpoint']
        else:
            raise NotFound("Please set 'default_endpoint' in credentials")

        if 'default_kv_endpoint' in credentials.keys():
            self.DEFAULT_KV_ENDPOINT = credentials['default_kv_endpoint']
        else:
            raise NotFound("Please set 'default_kv_endpoint' in credentials")

        if 'default_txn_endpoint' in credentials.keys():
            self.DEFAULT_TXN_ENDPOINT = credentials['default_txn_endpoint']
        else:
            raise NotFound("Please set 'default_txn_endpoint' in credentials")

        if 'api_version' in credentials.keys():
            self.API_VERSION = credentials['api_version']
        else:
            raise ConsulException("Please set 'api_version' in credentials")

        if 'default_host' in credentials.keys():
            self.DEFAULT_HOST = credentials['default_host']
        else:
            raise NotFound("Please set 'default_host' in credentials")

        if 'default_port' in credentials.keys():
            self.DEFAULT_PORT = credentials['default_port']
        else:
            raise NotFound("Please set 'default_port' in credentials")

        if 'default_add' in credentials.keys():
            self.DEFAULT_ADDRESS = credentials['default_add']
        else:
            raise NotFound("Please set 'default_port' in credentials")

        if 'default_token' in credentials.keys():
            self.DEFAULT_TOKEN = credentials['default_token']
        else:
            raise ConsulException("Please set 'default_port' in credentials")

    def get_children(self):
        return [namespace.decode('utf-8') for namespace in self.cons_client.keys("*{}*".format(self.main_namespace))]

    def return_all(self):
        if self.find_curr_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.find_curr_namespace()]
        else:
            raise NamespaceNotLoadedException("Namespace Not Found")

    def find_curr_namespace(self):
        return self.main_namespace + self.namespaces["current_namespace"]

    def persist_everything(self):
        for namespace in self.namespaces:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace):
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")

        self.recover_config = self.configurations[namespace]
        if self.cons_client.exists(self.main_namespace + "/" + namespace):
            pass
        else:
            self.cons_client.ensure_path(self.main_namespace + "/" + namespace)

        self.use_namespace(namespace)
        for configuration in self.recover_config:
            self.persist_configuration(namespace, configuration)
        self.use_namespace(recover_namespace)

    def persist_configuration(self, namespace, configuration):
        self.recover_config = self.configurations[namespace]
        path = self.main_namespace + "/" + namespace + "/" + configuration
        self.cons_client.ensure_path(path)
        data = self.recover_config[configuration]
        self.cons_client.set(path, str.encode(json.dumps(data)))
