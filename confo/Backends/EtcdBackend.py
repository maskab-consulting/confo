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
from ..Exceptions.EtcdExceptions import *


class EtcdBackend(AbstractBackend):
    def __init__(self):
        self.recover_config = None
        self.configurations = {}
        self.etcd_host = None
        self.etcd_port = None
        self.etcd_user = None
        self.etcd_passwd = None
        self.etcd_client: Type[Etcd3Client] = None
        self.namespace_name = '*'
        self.main_namespace = "/confo/"
        self.namespaces = None

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
        self.namespaces = self.get_children(self.etcd_client.get_all())

    def use_namespace(self, system_name):
        super().use_namespace(system_name)

    def get_namespaces(self):
        return super().get_namespaces()

    def create_namespace(self, namespace):
        self.etcd_client.put(self.main_namespace + namespace,"")
        self.configurations[self.main_namespace + namespace]={}
        self.namespaces = self.get_children(self.etcd_client.get_all())

    def get_all(self):
        pass

    def get(self, name, field=None):
        return super().get(name, field)

    def set(self, config, field, value):
        if type(field) == str:
            try:
                self.configurations[self.namespace_name][config][field] = value
            except:
                self.configurations[self.namespace_name][config] = {}
                self.configurations[self.namespace_name][config][field] = value
        elif (type(field) == dict or type(field) == list) and value == None:
            try:
                self.configurations[self.namespace_name][config] = field

            except:
                print("hello")

    def persist(self, namespace, config):
        return super().persist(namespace, config)

    def get_count(self):
        return super().get_count()

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
