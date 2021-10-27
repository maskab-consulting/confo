<<<<<<< HEAD
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
=======
# ****************************************************************************#
# Title:                    EtcdBackend                                       #
# Description:              This backend is used to handle  etcd              #
#                           configurations                                    #
# Author:                   Neo Thamela <neo.thamela@sambeconsulting.com>     #
# Author:                   Karabo Maleka <karabo.maleka@sambeconsulting.com> #
# Original Date:            06 March 2021                                     #
# Update Date:              14 March 2021                                     #
# Version:                  3.2.26                                            #
# ****************************************************************************#

>>>>>>> ff285f8d20c5c9a5d535900e8797e0a5a4989384

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
        self.main_namespace = "confo"
        self.namespaces = []
        self.reg_namespaces = []

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
        # check ensure that main namespace exists:
        self.ensure_main_namespace()
        self.namespaces = self.load_namespaces()
        self.register_namespaces(self.reg_namespaces)

    def create_namespace(self, namespace):
        """
         Create a new namespaces
        :param namespace:
        :return:
        """
        self.register_namespaces(namespaces=[namespace])

    def persist(self, namespace, config):
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
        self.configurations[self.namespace_name] = {}
        try:
            configs = json.loads(self.etcd_client.get(self.namespace_name)[0])["configurations"]
            for config in configs:
                path=self.namespace_name+"-"+config
                data = self.etcd_client.get(path)[0]
                if data.decode('utf-8').strip() == '':
                   data = "{}"
                try:
                    self.configurations[self.namespace_name][config] = json.loads(data)
                except ValueError as e:
                   self.configurations[self.namespace_name][config] = json.loads("{}")
        except:
            raise Exception("Unknow format in namespace '%s' key"%self.namespace_name)
    def check_key(self, key_name):
        """
         This utility checks if a key exists in a given ETCD instance
        :param key_name:
        :return:
        """

        if self.etcd_client.get(key_name) == (None, None):
            return False
        else:
            return True

    def ensure_main_namespace(self):
        """
          This method checks if the main namespace (confo) exists;
          if not it creates the namespaces with an empty list of child namespaces.
        :return:
        """
        if not self.check_key(self.main_namespace):
            self.etcd_client.put(self.main_namespace, json.dumps({"namespaces": []}))

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
        if "namespaces" in credentials.keys():
            self.reg_namespaces = credentials["namespaces"]

    def load_namespaces(self):
        """
         This method loads a list of namespaces from the main namespace list
        :return:
        """
        try:
            mn_values = json.loads( self.etcd_client.get(self.main_namespace)[0])
            namespaces = mn_values["namespaces"]
        except:
            raise UnknownFormatInMainNameSpace("The confo key has data with unknown format")

        return namespaces

    def register_namespaces(self,namespaces):
        self.namespaces = self.load_namespaces()
        for namespace in namespaces:
            if not self.check_key(namespace):
                self.etcd_client.put(namespace,json.dumps({"configurations":[]}))
                print(namespace)
            self.namespaces.append(namespace)

        self.namespaces = list(set(self.namespaces))
        self.etcd_client.put(self.main_namespace,json.dumps({"namespaces":self.namespaces}))

    def persist_everything(self):
        for namespace in self.namespaces:
            self.persist_namespace(namespace)

    def persist_namespace(self,namespace):
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
             raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")
        self.recover_config = self.configurations[namespace]
        if self.check_key(namespace):
            pass
        else:
            self.create_namespace(namespace)

        self.use_namespace(namespace)
        for configuration in self.recover_config:
            self.persist_configuration(namespace,configuration)
        self.use_namespace(recover_namespace)

    def persist_configuration(self,namespace,configuration):
        self.recover_config = self.configurations[namespace]
        path = namespace + "-" + configuration
        data = self.recover_config[configuration]
        self.etcd_client.put(path,json.dumps(data))

