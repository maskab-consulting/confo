# ************************************************************************#
# Title:                    FileBackend                                   #
# Description:              This backend is used to handle local          #
#                           file configurations                           #
# Author:                   Kabelo Masemola <kn3rdydad@gmail.com>         #
# Original Date:            06 March 2021                                 #
# Update Date:              06 March 2021                                 #
# Version:                  0.1.0                                         #
# ************************************************************************#

# Import modules

from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError
from singleton_decorator import singleton


class FileNotFoundException(Exception):
    pass


@singleton
class FileBackend(AbstractBackend):
    configuration_files = []
    configurations = {}
    namespace_name = '*'
    namespaces = []
    credentials = None
    config_path = None

    def load_credentials(self, credentials):
        def get_conf_name(file):
            if "." in file:
                return file.split('.')[0]
            else:
                return file
            
        def get_conf_values(namespace,file):
            data = None
            try:
                with open(self.config_path+"/"+namespace+"/"+file,"r") as f:
                      data = json.loads(f.read())
            except FileNotFoundError:
                print("Configuration file: "+file+" does not exist in namespace: "+namespace)
            except JSONDecodeError:
                print("Configuration file: "+file+" in namespace: "+namespace+" has unknown format")

            return data
            
        self.credentials = credentials
        self.config_path = credentials["config_path"]
        self.namespaces = os.listdir(self.config_path)
        for namespace in self.namespaces:
            self.configurations[namespace] = []
            for conf_file in os.listdir(self.config_path+"/"+namespace):
                 self.configurations[namespace].append({"name":get_conf_name(conf_file),\
                      "values":get_conf_values(namespace,conf_file)})

    def use_namespace(self, namespace_name):
        self.namespace_name = namespace_name
        self.reload()

    def get_namespaces(self):
        namespaces = {"all_namespaces": self.namespaces, "current_namespace": self.namespace_name}
        return namespaces

    def set_namespace(self, namespace):
        try:
            os.mkdir(self.config_path + "/" + namespace)
        except FileExistsError:
            print("namespace " + namespace + " already exists")

    def get_all(self):
        if self.namespace_name in self.namespaces:
            return self.configurations[self.namespace_name]
        else:
            raise Exception("Please select namespace")

    def get(self, name, field=None):
        if field != None:
            try:
                return self.configurations[name][field]
            except:
                print("configuration %s or field %s are not set" % (name, field))
        else:
            try:
                return self.configurations[name]
            except:
                print("configuration %s is not set" % (name))

    def set(self, config, field, value):
        try:
            self.configurations[config][field] = value
        except:
            self.configurations[config] = {}
            self.configurations[config][field] = value

    def reload(self):
        self.configurations = {}
        self.configuration_files = []
        self.load_credentials(credentials=self.credentials)

    def get_count(self):
        return len(self.configurations)

