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
        """
        Load credentials and connects to the Etcd-Client.
        User parse_credentials to extract keys and values from credentials.
        It also create object 'namespaces'

        :param credentials: it gets credentials from user to connect to etcd client.
        :return:
        """

        self.parse_credentials(credentials)

        if (self.etcd_user is None) and (self.etcd_passwd is None):
            # Connect to the Etcd3Client without password and username
            self.etcd_client = Etcd3Client(host=self.etcd_host, port=self.etcd_port)
        else:
            # connect to the Etcd3Client with password and username
            self.etcd_client = Etcd3Client(host=self.etcd_host,
                                           port=self.etcd_port,
                                           user=self.etcd_user,
                                           password=self.etcd_passwd)
        # creates object namespaces
        self.namespaces["all_namespaces"] = self.get_children(self.etcd_client.get_all())

    def create_namespace(self, namespace):
        """
        It creates a namespace inside confo (e.g /Confo/{namespace})
        It initialize the configurations to an empty dict {}.
        It then passes the namespace to the array of namespaces.

        :param namespace: the new namespace to be created
        :return:
        """

        self.etcd_client.put(self.main_namespace + namespace, "")
        self.configurations[self.main_namespace + namespace] = {}
        self.namespaces["all_namespaces"] = self.get_children(self.etcd_client.get_all())

    def use_namespace(self, system_name):
        """
        it checks if the namespace already has /Confo/ when recieved from user
        It checks through all namespaces in the array,then set the specified namespace to current_namespace.

        :param system_name:
        :return:
        """
        if system_name.startswith(self.main_namespace):
            namespace = system_name
        else:
            namespace = self.main_namespace + system_name

        if namespace in self.get_namespaces()["all_namespaces"]:
            self.namespaces["current_namespace"] = namespace
        #    self.reload()
        else:
            print("Namespace: " + namespace + " does not exist")

    def config_keys(self, myclient):
        v = []
        for x in myclient:
            _, y = x
            key = y.key.decode("utf-8")
            if len(str(key).split("/")) == 4:
                v.append(y.key.decode("utf-8"))
        return v

    def reload(self):
        """
        It helps to reload configurations from etcd client into a new Confo object
        :return:
        """
        if self.get_current_namespace() not in self.get_namespaces()["all_namespaces"]:
            raise NamespaceNotLoadedException("Namespace : {} does not exist".format(self.get_current_namespace()))

        if len(self.configurations) == 0:
            self.configurations[self.get_current_namespace()] = {}

        configs = self.config_keys(self.etcd_client.get_all())  # /confo/database/{configname}*


        for configkey in configs:
            data,_ = self.etcd_client.get(configkey)
            configname = str(configkey).split("/").pop()

            try:
                self.configurations[self.get_current_namespace()][configname] = json.loads(data)
            except ValueError as e:
                self.configurations[self.get_current_namespace()][configname] = json.loads("{}")

    def get_namespaces(self):
        """

        :return: all namespaces in the array
        """
        return self.namespaces

    def get_all(self):
        """

        :return: all configurations for the namespace that is being used.
        """
        if self.get_current_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.get_current_namespace()]
        else:
            raise NamespaceNotLoadedException("Please select namespace")

    def get(self, name, field=None):
        """
        it gets the configuration of the namespace in use and prints them

        :param name: the name(key) of the configuration
        :param field: optional param:field of the configuration
        :return:
        """
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
        """
        method creates a new configuration in the current namespace

        :param config: holds the name of the configuration
        :param field: can either be a string or a dictionary
        :param value: holds the value if field is a string and None if field is a dictionary
        :return:
        """
        if type(field) == str:
            try:
                self.configurations[self.get_current_namespace()][config][field] = value
            except:
                self.configurations[self.get_current_namespace()][config] = {}
                self.configurations[self.get_current_namespace()][config][field] = value
        elif (type(field) == dict or type(field) == list) and value == None:
            try:
                self.configurations[self.get_current_namespace()][config] = field
                print(self.configurations)
            except:
                raise ConfigurationNotSetException("configuration not set")

    def get_current_namespace(self):
        """
        :return: returns the current namespace
        """
        return self.namespaces["current_namespace"]

    def get_count(self):
        """

        :return: total number of namespaces inside /Confo/*
        """
        return len(self.get_children(self.etcd_client.get_all()))

    def parse_credentials(self, credentials):
        """
        extract values from the credentials and passes them to the variables to connect to ETCD client.
        :param credentials: a dictionary of credentials to be used to connect
        :return:
        """
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
        """

        :param myclient: will hold a tuple from namespaces
        :return: returns decoded namespaces and append them to an array.
        """
        v = []
        for x in myclient:
            _, y = x
            key = y.key.decode("utf-8")
            if len(str(key).split("/")) == 3:
                v.append(y.key.decode("utf-8"))
        return v

    def persist_configuration(self, namespace, config_name):
        """
        It saves the configuration of the namespace in the etcd: /confo/{namespace}/{configuration}

        :param namespace: hold current namespace
        :param config_name: hold configuration name
        :return:
        """

        self.namespace_config = self.configurations[namespace]
        path = "{}/{}".format(namespace, config_name)
        data = self.namespace_config[config_name]
        self.etcd_client.put(path, str.encode(json.dumps(data)))

    def persist(self, namespace=False, config=False):
        """
        It only persist configuration of the specific namespace

        :param namespace: hold current namespace
        :param config_name: hold configuration name
        :return:
        """
        if namespace == False:
            self.persist_everything()
        elif config == False:
            self.persist_namespace(namespace)
        else:
            self.persist_configuration(namespace, config)

    def persist_everything(self):
        """
        it iterates through all namespaces and  persists all configuration to
        :return:
        """
        for namespace in self.namespaces["all_namespaces"]:
            self.persist_namespace(namespace)

    def persist_namespace(self, namespace):
        """
        it persist the configuration for the namespace and its children
        It also creates the namespace if its not created already

        :param namespace: holds the namespace that is being used.
        :return:
        """

        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace {} is not loaded, Load namespace with obj.use_namespace({})".format(namespace, namespace)
            )
        self.namespace_config = self.configurations[namespace]
        if self.etcd_client.get(namespace) != 1 and (namespace not in self.namespaces["all_namespaces"]):
            self.create_namespace(namespace)
        elif self.etcd_client.get(namespace) != 1 and (namespace in self.namespaces["all_namespaces"]):
            self.etcd_client.put(namespace, namespace)
        else:
            print("persist_namespace() not working")

        self.use_namespace(namespace)
        for namespace_config_name in self.namespace_config.keys():
            self.persist_configuration(namespace, namespace_config_name)
