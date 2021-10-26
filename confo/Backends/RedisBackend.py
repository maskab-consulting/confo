# ******************************************************************************#
# Title:                    RedisBackend                                        #
# Description:              This backend is used to handle  Redis               #
#                           configurations                                      #
# Author:                   Tshepang Maila <tshepang.maila@sambeconsulting.com> #
# Original Date:            01 September 2021                                   #
# Update Date:              06 September 2021                                   #
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

        '''
            Redis
        '''
        self.redis_host: str = None
        self.redis_port: int = 0
        self.redis_db: int = 0
        self.redis_user: str = None
        self.redis_password: str = None
        self.rs_client: Type[Redis] = None

        '''
            Namespaces
        '''
        self.main_namespace: str = "confo"
        self.namespace_name = None
        self.namespaces: list = []
        self.reg_namespaces: list = []
        '''
            Configurations
        '''
        self.configurations: dict = {}
        self.namespace_configs: dict = {}

    def load_credentials(self, credentials):
        """
        Load the credentials to connect to Redis,
        and also init the instance

        Args:
            credentials ([ict]): dict of credentials for Redis client Connection
        """

        self.parse_credentials(credentials)                                             # Parse the credentials and assign instance variables
        if (self.redis_user is None) and (self.redis_password is None):
            '''
                Connect to the Redis client
            '''
            self.rs_client = Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        else:
            self.rs_client = Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_password)

        self.ensure_main_namespace()
        self.namespaces = self.load_namespaces()
        self.register_namespaces(self.reg_namespaces)

    def create_namespace(self, namespace) -> None:
        """
        Create top level namespace for the configurations

        Args:
            namespace ([str]): The name of the namespace
        """
        self.register_namespaces(namespaces=[namespace]) 

    def key_exists(self, key_name) -> bool:
        if self.rs_client.exists(key_name) == 1:
            return True
        return False

    def ensure_main_namespace(self):

        if not self.key_exists(self.main_namespace):
            self.rs_client.set(self.main_namespace, json.dumps({"namespaces": []}))

    
    def register_namespaces(self, namespaces: list) -> None:

        self.namespaces = self.load_namespaces()

        for namespace in namespaces:
            if not self.key_exists(namespace):
                self.rs_client.set(namespace, json.dumps({"configurations": []}))

            self.namespaces.append(namespace)

        self.namespaces = list(set(self.namespaces))
        self.rs_client.set(self.main_namespace, json.dumps({"namespaces": self.namespaces}))

    def persist(self, namespace=False, config=False) -> None:
        """
        Save all configurations in this instance to Redis cache itself

        Args:
            namespace (bool, str): The name of the namespace you want to persist
            config (bool, str): The name of the config you want to persist
        """

        if namespace is False:
            '''
                So if the namespace to persist is not specified, all namespaces with be persisted...
                meaning that all their configurations also will be persisted
            '''
            self.persist_everything()

        elif config is False:
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
        return super().get_namespaces()

    def use_namespace(self, system_name: str):
        """
        For all methods related to the Confo, you have to activate the namespace you want to use,
        This methods activates the namespace you want to use

        Args:
            system_name (str): Namespace you want to use
        """
        super().use_namespace(system_name)

    def get_all(self) -> dict:
        """
        Shows all the configurations of the namespace that was activated

        Raises:
            NamespaceNotLoadedException: Is raised when the namespace was not activated or the namespace does not exist

        Returns:
            dict: All dictionaries related to the current namespace
        """
        return super().get_all()

    def get(self, name, field=None):
        """
        Get configurations from instance

        Args:
            name ([str]): Name of the configurations
            field ([str], optional): Field representing the field in the configurations

        Returns:
            [dict | str]: returns the speciefied value of the name | field
        """
        return super().get(name=name, field=field)

    def set(self, config, field, value):
        """
        Set configurations into the instace

        Args:
            config ([str]): Name of the Configuration 
            field ([str | dict | list]): Name of the field | the entire configuration
            value ([str]): Value that is being set
        """
        super().set(config=config, field=field, value=value)

    def get_count(self) -> int:
        """
        Returns the count of configurations in the activated namespace

        Returns:
            int: count of configurations
        """
        return super().get_count()

    def load_namespaces(self):

        try:
            nm_dict = json.loads(self.rs_client.get(self.main_namespace).decode('utf-8'))
            namespaces = nm_dict["namespaces"]

        except:
            raise UnknownFormatInMainNameSpace("The confo key has data with Unknown Format")

        return namespaces
            

    def reload(self):
        """
        Extracts configurations and namespaces already saved from Redis cache into this instance
        """
        self.configurations[self.get_current_namespace()] = {}

        '''
            Get keys stored in redis cache, but im looking for keys that are in a specific format,
            keys that have the namespace in them e.g /confo/database/* -> /confo/database/mysqli,
            then store them in a list
        '''
        config_paths = json.loads(self.rs_client.get(self.get_current_namespace()).decode('utf-8'))["configurations"]      # Extracts configuration namespaces
        
        '''
            Loop through the keys to use them to get the data stored in redis cache
        '''
        for c_path in config_paths:
            config_name = "{}-{}".format(self.get_current_namespace(), c_path)
            data = (self.rs_client.get(config_name)).decode("utf-8")                         # Fetch data in redis          
            if data == '':
                data = "{}"
            try:
                self.configurations[self.get_current_namespace()][config_name] = json.loads(data)
            except ValueError as e:
                self.configurations[self.get_current_namespace()][config_name] = json.loads("{}")        

    def parse_credentials(self, credentials: dict) -> None:
        """
        Assign instance variables to values use to connect to the Redis cache using this Redis Client

        Args:
            credentials (dict): hold credentials used to connect to Redis using this Redis Client

        Raises:
            RedisHostNotFoundException: Raised when the Host for Redis Connection is not specified
            RedisPortNotFoundException: Raised when Port for Redis Connection is not specified
        """
        
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

    def get_configs(self) -> dict:
        """
        Will return all configurations this instance has

        Returns:
            dict: all configurations of the instance
        """
        return self.configurations
    
    def get_current_namespace(self) -> str:
        """
        Returns the current working namespace

        Returns:
            str: the string that is the current namespace
        """
        return self.namespace_name

    def persist_everything(self) -> None:
        """
        Loop through all namespaces and persist each every namespace that is in the list of namespaces
        """
        for namespace in self.get_namespaces()["all_namespaces"]:
            '''
                Persist per namespace
            '''
            print(namespace)
            self.persist_namespace(namespace)
    
    def persist_namespace(self, namespace) -> None:
        """
        Now that we have a namespace to persist, we have to persist each & every configuration of that namespace 

        Args:
            namespace ([type]): The name of the namespace to persist

        Raises:
            NamespaceNotLoadedException: Raised when the namespace is not found in the list namespaces
        """
        recover_namespace = self.namespace_name
        if namespace not in self.configurations.keys():
             raise NamespaceNotLoadedException(
                "Namespace " + namespace + " not loaded. Load namespace with obj.use_namespace(" + namespace + ")")
        self.recover_config: dict = self.configurations[namespace]
        if self.key_exists(namespace):
            pass
        else:
            self.create_namespace(namespace)

        self.use_namespace(namespace)
        for configuration_key in self.recover_config.keys():
            self.persist_configuration(namespace,configuration_key)
        self.use_namespace(recover_namespace)

    def persist_configuration(self, namespace, configuration_key) -> None:
        """
        Will extract configurations of the specified namespace and save them in Redis cache

        Args:
            namespace ([str]):  Name of the namespace
            config_name ([str]): Name of the configuration
        """
        # self.recover_config = self.configurations[namespace]
        print(self.recover_config)
        path = namespace + "-" + configuration_key
        data = self.recover_config[configuration_key]
        print(data)
        self.rs_client.set(path,json.dumps(data))
        # print("nsp : {}, data : {}".format(dir, self.rs_client.get(dir)))
        
