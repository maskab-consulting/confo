# *******************************************************************************#
# Title:                    ETCD Backend                                         #
# Description:              This backend is used to handle distributed           #
#                            configuration                                       #
# Author:                   Karabo <karabo.maleka@sambeconsulting.co.za>         #
# Original Date:            27 August 2021                                       #
# Update Date:              30 August 2021                                       #
# Version:                  0.1.0                                                #
# *******************************************************************************#

# Import modules
from typing import Type

from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError
from etcd3 import *

from ..Exceptions import NamespaceNotLoadedException
from ..Exceptions.EtcdExceptions import *


class EtcdBackend(AbstractBackend):
    def __init__(self):
        self.namespace_config = {}
        self.configurations = {}
        self.etcd_host = None
        self.etcd_port = None
        self.etcd_user = None
        self.etcd_passwd = None
        self.etcd_client: Type[Etcd3Client] = None
        self.namespace_name = '*'
        self.main_namespace = "/confo/"
        self.namespaces = {
            "all_namespaces": [],
            "current_namespace": ""
        }

    def load_credentials(self, credentials):
        self.parse_credentials(credentials)
        if (self.etcd_user is None) and (self.etcd_passwd is None):
            # connect to the Etcd3Client without password and username
            self.etcd_client = Etcd3Client(host=self.etcd_host, port=self.etcd_port)
        else:
            # connect to the Etcd3Client with password and username
            self.etcd_client = Etcd3Client(host=self.etcd_host,
                                           port=self.etcd_port,
                                           user=self.etcd_user,
                                           password=self.etcd_passwd)
        self.namespaces["all_namespaces"] = self.get_children(self.etcd_client.get_all())

    def use_namespace(self, system_name):
        if system_name in self.get_namespaces()["all_namespaces"]:
            self.namespaces["current_namespace"] = system_name
            self.configurations[self.main_namespace + system_name] = {}
            # self.reload()
        else:
            print("Namespace: " + system_name + " does not exist")

    def get_namespaces(self):
        return self.namespaces

    def create_namespace(self, namespace):
        self.etcd_client.put(self.main_namespace + namespace, "")
        self.configurations[self.main_namespace + namespace] = {}
        self.namespaces["all_namespaces"] = self.get_children(self.etcd_client.get_all())

    def get_all(self):
        if self.get_current_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.get_current_namespace()]
        else:
            raise NamespaceNotLoadedException("Please select namespace")

    def get(self, name, field=None):
        if field != None:
            try:
                return self.configurations[self.get_current_namespace()][name][field]
            except:
                print("configuration %s or field %s are not set" % (name, field))
        else:
            try:
                return self.configurations[self.get_current_namespace()][name]
            except:
                print("configuration %s is not set" % (name))

    def set(self, config, field, value):
        if type(field) == str:
            try:
                self.configurations[self.get_current_namespace()][config][field] = value
            except:
                self.configurations[self.get_current_namespace()][config] = {}
                self.configurations[self.get_current_namespace()][config][field] = value
        elif (type(field) == dict or type(field) == list) and value == None:
            try:
                self.configurations[self.get_current_namespace()][config] = field
            except:
                print("Did not set Configuration")

    def get_current_namespace(self):
        return self.main_namespace + self.namespaces["current_namespace"]

    def persist(self, namespace, config):
        return super().persist(namespace, config)

    def get_count(self):
        return len(self.get_children(self.etcd_client.get_all()))

    def reload(self):
        return super().reload()

    def parse_credentials(self, credentials):
        if "user" in credentials.keys():
            self.etcd_user = credentials["user"]
        if "password" in credentials.keys():
            self.etcd_passwd = credentials["password"]
        if "host" in credentials.keys():
            self.etcd_host = credentials["host"]
        else:
            raise Etcd3Exception("Please set 'etcd_host' in credentials")
        if "port" in credentials.keys():
            self.etcd_port = credentials["port"]
        else:
            raise Etcd3HostNotFoundException("Please set 'etcd_port' in credentials")

    def get_children(self, myclient):
        v = []
        for x in myclient:
            y, _ = x
            v.append(y.decode('utf-8'))
        return v

    def get_all(self):
        if self.get_current_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.get_current_namespace()]
        else:
            raise NamespaceNotLoadedException("Please select a namespace")

    def persist_configuration(self, namespace, config_name) -> None:
        self.namespace_config = self.configurations[namespace]
        path = "{}/{}".format(namespace, config_name)
        data = self.namespace_config[config_name]
        self.etcd_client.put(path, str.encode(json.dumps(data)))

    def persist(self, namespace=False, config=False):
        if namespace == False:
            self.persist_everything()
        elif config == False:
            self.persist_namespace(namespace)
        else:
            self.persist_configuration(namespace, config)

    def persist_everything(self):
        for namespace in self.namespaces["all_namespaces"]:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace):
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace {} is not loaded, Load namespace with obj.use_namespace({})".format(namespace, namespace)
            )
        self.namespace_config = self.configurations[namespace]
        if self.etcd_client.get(namespace) != 1:
            self.etcd_client.set(namespace, "null")

        self.use_namespace(namespace)
        for nsp_config_name in self.namespace_configs.keys():
            self.persist_configuration(namespace, nsp_config_name)
