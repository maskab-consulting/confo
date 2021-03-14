# ************************************************************************#
# Title:                    AbstractBackend                               #
# Description:              This class defines a backend interface        #
# Author:                   Kabelo Masemola <kn3rdydad@gmail.com>         #
# Original Date:            06 March 2021                                 #
# Update Date:              06 March 2021                                 #
# Version:                  0.1.0                                         #
# ************************************************************************#

# Import modules
from abc import ABC, abstractmethod


class AbstractBackend(ABC):
    @abstractmethod
    def load_credentials(self, credentials):
        pass

    @abstractmethod
    def use_namespace(self, system_name):
        pass

    @abstractmethod
    def get_namespaces(self):
        pass

    @abstractmethod
    def create_namespace(self,namespace):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get(self, name, field=None):
        pass

    @abstractmethod
    def set(self, config, field, value):
        pass

    @abstractmethod
    def persist(self,namespace,config):
        pass

