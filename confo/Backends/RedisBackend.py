# ******************************************************************************#
# Title:                    RedisBackend                                        #
# Description:              This backend is used to handle  Redis               #
#                           configurations                                      #
# Author:                   Tshepang Maila <tshepang.maila@sambeconsulting.com> #
# Original Date:            01 September 2021                                   #
# Update Date:              01 September 2021                                   #
# Version:                  0.1.0                                               #
# ******************************************************************************#


from .AbstractBackend import AbstractBackend
from typing import Type
import os
import json
from json.decoder import JSONDecodeError
from redis import Redis

from ..Exceptions import *

class RedisBackend(AbstractBackend):

    def __init__(self) -> None:
        self.redis_host: str = None
        self.redis_port: int = 0
        self.redis_db: int = 0
        self.redis_user: str = None
        self.redis_password: str = None

        self.rs_client: Type[Redis] = None

        self.main_namespace: str = "/confo/"
        self.current_namespace = None
        self.namespaces: dict = {
            "all_namespaces" : []
        }

        self.configurations: dict = {}
        self.namespace_configs: dict = {}

    def load_credentials(self, credentials):

        self.parse_credentials(credentials)
        if (self.redis_user is None) and (self.redis_password is None):
            self.rs_client = Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        else:
            pass

        self.namespaces["all_namespaces"] = self.get_children()

    def create_namespace(self, namespace) -> None:
        """
        Create top level namespace for the configurations

        Args:
            namespace ([str]): The name of the namespace
        """

        root_namespace = self.main_namespace + namespace                            # create the namespace with combination of the main namespace e.g /confo/{namespace} 

        self.rs_client.set(root_namespace, "null")                                  # Since redis takes Key-Value, the namespace value is set to Null
        self.configurations[root_namespace] = {}                                    # Create an entry of the namespace in configurations
        self.namespaces["all_namespaces"] = self.get_children()                     # Get updated list of namespaces after creating a new space 

    def persist(self, namespace=False, config=False) -> None:
        """
        Save all configurations in this instance to Redis cache itself

        Args:
            namespace (bool, str): The name of the namespace you want to persist
            config (bool, str): The name of the config you want to persist
        """

        if namespace == False:
            '''
                So if the namespace to persist is not specified, all namespaces with be persisted...
                meaning that all their configurations also will be persisted
            '''
            self.persist_everything()

        elif config == False:
            '''
                If namespace is specified without the configuration name, all configurations of this namespace will persisted
            '''
            self.persist_namespace(namespace)

        else:
            '''
                Only the configuration in the specified namespace will be persisted
            '''
            self.persist_configuration(namespace, config)

    def get_namespaces(self) -> dict:
        """
        Returns a dictionary of all the namespaces this instance and also the currently used namespace

        Returns:
            dict: The namespaces in the instance
        """
        return self.namespaces

    def use_namespace(self, system_name: str):
        """
        For all methods related to the Confo, you have to activate the namespace you want to use,
        This methods activates the namespace you want to use

        Args:
            system_name (str): [description]
        """

        if system_name.startswith(self.main_namespace):                                 # checks if the system_name starts with '/confo/'
            '''
                If the system_name starts with '/confo/' then the namespace is the system_name
            '''
            namespace = system_name
        else:
            '''
                If not then create the namespace as the combination of main namespace and the system_name e.g /confo/{system_name}
            '''
            namespace = self.main_namespace + system_name
        
        if namespace in self.get_namespaces()["all_namespaces"]:                        # Checks if the namespace already exists in the list of all namespaces
            '''
                Since the specified namespace to use exists, activate it by setting it as the current in-use namespace
            '''
            self.namespaces["current_namespace"] = self.current_namespace
        else:
            '''
                Since it doesn't exists, it cannot be activated
            '''
            print("Namespace: {} does not exist".format(system_name))

    def get_all(self) -> dict:
        """
        Shows all the configurations of the namespace that was activated

        Raises:
            NamespaceNotLoadedException: Is raised when the namespace was not activated or the namespace does not exist

        Returns:
            dict: All dictionaries related to the current namespace
        """
        if self.get_current_namespace() in self.namespaces["all_namespaces"]:
            return self.configurations[self.get_current_namespace()]
        else:
            raise NamespaceNotLoadedException("Please select a namespace")

    def get(self, name, field=None):
        if field != None:
            try:
                return self.configurations[self.get_current_namespace()][name][field]
            except:
                print("configuration {} or field {} are not set".format(name, field))
        else:
            try:
                return self.configurations[self.get_current_namespace()][name]
            except:
                print("configuration {} is not set".format(name))

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
                print("hello world")

    def persist(self, namespace=False, config=False):
        if namespace == False:
            self.persist_everything()
        elif config == False:
            self.persist_namespace(namespace)
        else:
            self.persist_configuration(namespace, config)

    def get_count(self):
        return len(self.get_all())

    def reload(self):
        print("hello world")

    def parse_credentials(self, credentials: dict) -> None:
        
        cred_keys: list = credentials.keys()

        if 'redis_user' in cred_keys:
            self.redis_user = credentials['redis_user']
        if 'redis_password' in cred_keys:
            self.redis_password = credentials['redis_password']
        if 'redis_host' in cred_keys:
            self.redis_host = credentials['redis_host']
        else:
            raise RedisHostNotFoundException("Please set 'redis_host' in your credentials")
        if 'redis_port' in cred_keys:
            self.redis_port = credentials['redis_port']
        else:
            raise RedisPortNotFoundException("Please set 'redis_post' in your credentials")

    def get_children(self) -> list:
        children = []
        for namespace in self.rs_client.keys("*{}*".format(self.main_namespace)):
            if len(str(namespace.decode("utf-8")).split("/")) == 3:
                children.append(namespace.decode("utf-8"))
        return children

    def get_configs(self) -> dict:
        """
        Will return all configurations this instance has

        Returns:
            dict: all configurations of the instance
        """
        return self.configurations
    
    def get_current_namespace(self) -> str:
        return self.namespaces["current_namespace"]

    def persist_everything(self) -> None:
        for namespace in self.namespaces["all_namespaces"]:
            self.persist_namespace(namespace)
    
    def persist_namespace(self, namespace) -> None:
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace {} is not loaded, Load namespace with obj.use_namespace({})".format(namespace, namespace)
            )
        self.namespace_configs = self.configurations[namespace]
        if (self.rs_client.exists(namespace) != 1) and (namespace in self.namespaces["all_namespaces"]):
            self.rs_client.set(namespace, "null")
        elif (self.rs_client.exists(namespace) != 1) and (namespace not in self.namespaces["all_namespaces"]):
            self.create_namespace(namespace)

        self.use_namespace(namespace)
        print(namespace)
        for nsp_config_name in self.namespace_configs.keys():
            self.persist_configuration(namespace, nsp_config_name)

    def persist_configuration(self, namespace, config_name) -> None:
        self.namespace_configs = self.configurations[namespace]
        dir = "{}/{}".format(namespace, config_name) # /confo/db/mysqli
        data = self.namespace_configs[config_name]
        self.rs_client.set(dir, str.encode(json.dumps(data)))

        # print("nsp : {}, data : {}".format(dir, self.rs_client.get(dir)))
        
