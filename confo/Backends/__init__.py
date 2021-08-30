FILE_BACKEND = 1
ZOOKEEPER_BACKEND = 2
ETCD_BACKEND = 3
CONSUL_BACKEND = 4
REDIS_BACKEND = 5
DATABASE_BACKEND = 6
ELASTIC_BACKEND = 7

from .FileBackend import FileBackend
from .ZookeeperBackend import ZookeeperBackend


def backend_selector(backend_type):
    if backend_type == FILE_BACKEND:
        return FileBackend
    elif backend_type == ZOOKEEPER_BACKEND:
        return ZookeeperBackend
    elif backend_type == ETCD_BACKEND:
        return EtcdBackend
    elif backend_type == CONSUL_BACKEND:
        return ConsulBackend
    elif backend_class ==REDIS_BACKEND:
        return RedisBackend
    elif backend_type == DATABASE_BACKEND:
        return DatabaseBackend
    elif backend_type == ELASTIC_BACKEND:
        return ElasticBackend



