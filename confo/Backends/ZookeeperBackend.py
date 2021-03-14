# ************************************************************************#
# Title:                    ZookeeperBackend                              #
# Description:              This backend is used to handle distributed    #
#                            configuration                                #
# Author:                   Kabelo Masemola <kn3rdydad@gmail.com>         #
# Original Date:            14 March 2021                                 #
# Update Date:              14 March 2021                                 #
# Version:                  0.1.0                                         #
# ************************************************************************#

# Import modules

from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError
from singleton_decorator import singleton
from kazoo.client import KazooClient


class FileNotFoundException(Exception):
    pass


@singleton
class ZookeeperBackend(AbstractBackend):
    configurations = {}
    zookeeper_host = None
    zookeeper_port = None
    zookeeper_user = None
    zookeeper_passwd = None
    zk_client = None
    namespace_name = '*'
    main_namespace = "/confo/"
    namespaces = None

    def load_credentials(self, credentials):
        self.parse_credentials(credentials)
        if (self.zookeeper_user == None) and (self.zookeeper_passwd == None):
            self.zk_client = KazooClient(hosts=self.zookeeper_host + ":" + self.zookeeper_port)
        else:
            auth_data = [("digest", self.zookeeper_user + ":" + self.zookeeper_passwd)]
            self.zk_client = KazooClient(hosts=self.zookeeper_host + ":" + self.zookeeper_port, auth_data=auth_data)
        self.zk_client.start()
        self.zk_client.ensure_path("/confo")
        self.namespaces = self.zk_client.get_children(self.main_namespace)

    def create_namespace(self, namespace):
        self.zk_client.ensure_path(self.main_namespace + namespace)
        self.namespaces = self.zk_client.get_children(self.main_namespace)

    def persist(self, namespace=False, config=False):
        if namespace == False:
            # Persist everything
            self.persist_everything()
        elif config == False:
            # persist the entire namespace if exists
            self.persist_namespace(namespace)
        else:
            # persist just one configuration file
            self.persist_configuration(namespace, config)

    def reload(self):
        self.configurations = {}
        self.configurations[self.namespace_name] = {}
        configs = self.zk_client.get_children(self.main_namespace + "/" + self.namespace_name)
        for config in configs:
            path = self.main_namespace + "/" + self.namespace_name + "/" + config
            data, stat = self.zk_client.get(path)
            self.configurations[self.namespace_name][config] = json.loads(data)

    def parse_credentials(self, credentials):
        if "zookeeper_user" in credentials.keys():
            self.zookeeper_user = credentials["zookeeper_user"]
        if "zookeeper_passwd" in credentials.keys():
            self.zookeeper_passwd = credentials["zookeeper_passwd"]
        if "zookeeper_host" in credentials.keys():
            self.zookeeper_host = credentials["zookeeper_host"]
        else:
            raise Exception("Please set 'zookeeper_host' in credentials")
        if "zookeeper_port" in credentials.keys():
            self.zookeeper_port = credentials["zookeeper_port"]
        else:
            raise Exception("Please set 'zookeeper_port' in credentials")

    def persist_everything(self):
        for namespace in self.namespaces:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace):
        if self.zk_client.exists(self.main_namespace + "/" + namespace):
            pass
        else:
            self.zk_client.ensure_path(self.main_namespace + "/" + namespace)
        for configuration in self.configurations[namespace]:
            self.persist_configuration(namespace, configuration)

    def persist_configuration(self, namespace, configuration):
        path = self.main_namespace + "/" + namespace + "/" + configuration
        self.zk_client.ensure_path(path)
        data = self.configurations[namespace][configuration]
        self.zk_client.set(path,json.dumps(data))
