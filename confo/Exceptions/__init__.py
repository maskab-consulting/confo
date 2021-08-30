from .ZooKeeperExceptions import *
from .FileExceptions import *
from .EtcdExceptions import *
from .RedisExceptions import *
from .ConsulExceptions import *
from .DataBaseException import *
from .ElasticSearchException import *
from .NamespaceException import  *

# Exceptions

class BackendsActivationException(Exception):
    pass

class BackendNotFoundException(Exception):
    pass


