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
        self.main_namespace: str = "/confo/"
        self.current_namespace = None
        self.namespaces: dict = {
            "all_namespaces" : []
        }

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
            pass

        '''
            Get all namespaces in Redis cache
        '''
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
            self.namespaces["current_namespace"] = namespace
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
        if field is not None:
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
        """


        Args:
            config ([str]): Name of the Configuration 
            field ([str | dict | list]): Name of the field | the entire configuration
            value ([str]): Value that is being set
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
            except:
                print("hello world")

    def get_count(self) -> int:
        """
        Returns the count of configurations in the activated namespace

        Returns:
            int: count of configurations
        """
        return len(self.get_all())

    def reload(self):
        """
        Extracts configurations and namespaces already saved from Redis cache into this instance
        """

        if self.get_current_namespace() not in self.get_namespaces()["all_namespaces"]:
            raise NamespaceNotLoadedException("Namespace : {} does not exist".format(self.get_current_namespace()))

        if len(self.configurations) == 0:
            self.configurations[self.get_current_namespace()] = {}

        '''
            Get keys stored in redis cache, but im looking for keys that are in a specific format,
            keys that have the namespace in them e.g /confo/database/* -> /confo/database/mysqli,
            then store them in a list
        '''
        config_paths = [config_namespace.decode("utf-8") for config_namespace in self.rs_client.keys("*{}/*".format(self.get_current_namespace()))]      # Extracts configuration namespaces
        
        '''
            Loop through the keys to use them to get the data stored in redis cache
        '''
        for c_path in config_paths:
            data = (self.rs_client.get(c_path)).decode("utf-8")                         # Fetch data in redis          
            if data == '':
                data = "{}"

            '''
                Since the keys are in this format /confo/database/mysqli ... and mysqli is our config name,
                Split the string to create an array ["", "confo", "database", "mysqli"] then return the last item - thats the config name
            '''    
            config_name = str(c_path).split("/").pop()

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

    def get_children(self) -> list:
        """
        Returns all namespaces saved in Redis cache

        Returns:
            list: list of namespaces
        """
        children = []
        
        '''
            Loops all keys of the format '/confo/' that are saved in Redis, then push them in a list and returns them as namespaces
        '''
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
        """
        Returns the current working namespace

        Returns:
            str: the string that is the current namespace
        """
        return self.namespaces["current_namespace"]

    def persist_everything(self) -> None:
        """
        Loop through all namespaces and persist each every namespace that is in the list of namespaces
        """
        for namespace in self.namespaces["all_namespaces"]:
            '''
                Persist per namespace
            '''
            self.persist_namespace(namespace)
    
    def persist_namespace(self, namespace) -> None:
        """
        Now that we have a namespace to persist, we have to persist each & every configuration of that namespace 

        Args:
            namespace ([type]): The name of the namespace to persist

        Raises:
            NamespaceNotLoadedException: Raised when the namespace is not found in the list namespaces
        """
        if namespace not in self.configurations.keys():
            raise NamespaceNotLoadedException(
                "Namespace {} is not loaded, Load namespace with obj.use_namespace({})".format(namespace, namespace)
            )
        
        if (self.rs_client.exists(namespace) != 1) and (namespace in self.namespaces["all_namespaces"]):
            '''
                Check if the namespace exists in the list of namespaces but not in the Redis cache, create it in the redis cache
            '''
            self.rs_client.set(namespace, "null")

        elif (self.rs_client.exists(namespace) != 1) and (namespace not in self.namespaces["all_namespaces"]):

            '''
                Else if does not exists in both the Redis cache and the list of namespaces,
                we just create that namespace... The above Raised Exception will excute, so the code wont reach this part
            '''
            self.create_namespace(namespace)

        
        self.use_namespace(namespace)                                                   # Activate the namespace for usage
        
        '''
            Save all configurations of the namespace in it's own dict
        '''
        self.namespace_configs = self.configurations[namespace]

        '''
            Now Loop through all configurations of the namespace to persist them
        '''
        for nsp_config_name in self.namespace_configs.keys():
            '''
                Persist per configuration
            '''
            self.persist_configuration(namespace, nsp_config_name)

    def persist_configuration(self, namespace, config_name) -> None:
        """
        Will extract configurations of the specified namespace and save them in Redis cache

        Args:
            namespace ([str]):  Name of the namespace
            config_name ([str]): Name of the configuration
        """
        self.namespace_configs = self.configurations[namespace]
        dir = "{}/{}".format(namespace, config_name)                                    # /confo/db/mysqli
        data = self.namespace_configs[config_name]                                      # extract dict of configs
        self.rs_client.set(dir, str.encode(json.dumps(data)))                           # save them in Redis

        # print("nsp : {}, data : {}".format(dir, self.rs_client.get(dir)))
        
