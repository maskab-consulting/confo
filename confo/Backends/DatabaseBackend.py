# **************************************************************************#
# Title:                    DatabaseBackend                                 #
# Description:              This backend is used to handle database         #
#                           configurations                                  #
# Author:                   Kabelo Masemola <kn3rdydad@gmail.com>           #
# Original Date:            06 March 2021                                   #
# Update Date:              14 March 2021                                   #
# Version:                  0.1.0                                           #
# **************************************************************************#


from .AbstractBackend import AbstractBackend
import os
import json
from json.decoder import JSONDecodeError

from ..Exceptions import *

class DatabaseBackend(AbstractBackend):
    def load_credentials(self, credentials):
        return super().load_credentials(credentials)

    def use_namespace(self, system_name):
        super().use_namespace(system_name)

    def get_namespaces(self):
        return super().get_namespaces()

    def create_namespace(self, namespace):
        return super().create_namespace(namespace)

    def get_all(self):
        return super().get_all()

    def get(self, name, field=None):
        return super().get(name, field)

    def set(self, config, field, value):
        super().set(config, field, value)

    def persist(self, namespace, config):
        return super().persist(namespace, config)

    def get_count(self):
        return super().get_count()

    def reload(self):
        return super().reload()
