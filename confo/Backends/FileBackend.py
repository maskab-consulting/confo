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
from singleton_decorator import singleton


@singleton
class FileBackend(AbstractBackend):
    configuration_files = []
    configurations = {}
    system_name = 'all'
    systems = []
    credentials = None

    def parse_credentials(self, credentials):
        if "config_path" in credentials:
            self.systems = os.listdir(credentials["config_path"])
            if self.system_name == 'all':
                for system in self.systems:
                    for file in os.listdir(credentials["config_path"] + "/" + system):
                        self.configuration_files.append(system + "/" + file)
            else:
                if os.path.exists(credentials["config_path"] + "/" + self.system_name):
                    for file in os.listdir(credentials["config_path"] + "/" + self.system_name):
                        self.configuration_files.append(self.system_name + "/" + file)
                else:
                    print("System "+str(self.system_name)+" is not found in configuration directory")

        else:
            print('Dictionary must contain key "config_path"')

    def load_credentials(self, credentials):
        self.parse_credentials(credentials=credentials)
        self.credentials = credentials
        config_path = credentials["config_path"]
        for conf in self.configuration_files:
            cfg = open(config_path + conf, 'r')
            try:
                name = conf.split('/')[1].split('.')[0]
                self.configurations[name] = json.loads(cfg.read())
                # print(self.configurations)
            except:
                print("Configuration File %s does not have the proper format" , str(conf))

    def set_system(self, system_name):
        self.system_name = system_name

    def get_all(self):
        return self.configurations

    def get(self, name, field=None):
        if field != None:
            try:
                return self.configurations[name][field]
            except:
                print("configuration %s or field %s are not set" %(name, field))
        else:
            try:
                return self.configurations[name]
            except:
                print("configuration %s is not set" %(name))

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