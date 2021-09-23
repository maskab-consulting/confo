```python
from confo.Confo import Confo
from confo import Backends as BE
from confo.Backends.ConsulBackend import ConsulBackend
import consul
# Create Configuration Manager Object
config = Confo()
cons = ConsulBackend()
```


```python
cons_client = consul.Consul()
dir(cons_client)
```




    ['ACL',
     'Agent',
     'Catalog',
     'Config',
     'Connect',
     'Coordinate',
     'DiscoveryChain',
     'Event',
     'Health',
     'KV',
     'Operator',
     'Query',
     'Session',
     'Snapshot',
     'Status',
     'Txn',
     '__class__',
     '__delattr__',
     '__dict__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__le__',
     '__lt__',
     '__module__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     '__weakref__',
     'acl',
     'agent',
     'catalog',
     'config',
     'connect',
     'consistency',
     'coordinate',
     'dc',
     'discovery_chain',
     'event',
     'health',
     'http',
     'http_connect',
     'kv',
     'operator',
     'query',
     'scheme',
     'session',
     'snapshot',
     'status',
     'token',
     'txn']




```python
# Instantiate Consul Backend
cr = {"default_host": "127.0.0.1",
      "default_port": 8500,
      "default_scheme": 'http',
      "api_version": 'v1'}
config.load_backend(credentials=cr, name="ConsulBackend", backend_type=BE.CONSUL_BACKEND)
```


```python
# Get Backends
config.get_backends()
# Results:
```




    {'all_backends': ['ConsulBackend'], 'active_backend': None}




```python
# Activate ConsulBackend
config.activate_backend("ConsulBackend")
```


```python
# List Backends To See Active Backend
config.get_backends()
```




    {'all_backends': ['ConsulBackend'], 'active_backend': 'ConsulBackend'}




```python
# Create Namespace "database"
config.create_namespace("database")
```


```python
# List Namespaces
config.get_namespaces()
# Results:
```




    {'all_namespaces': ['confo/database']}




```python
# Use Namespace "database"
config.use_namespace("database")
```


```python
# List Namespaces To See Active/Current Namespace
config.get_namespaces()
```




    {'all_namespaces': ['confo/database'], 'current_namespace': 'confo/database'}




```python
# Instantiate SQL & Postgress Configurations
sql = {
    "host": "localhost",
    "db_name": "sambe_db",
    "usr": "root"
}
connect_name = "sql"
# Creating New Configuration & Store Credentials
config.set(connect_name,sql, None)

postgres = {
    "host": "localhost",
    "db_name": "sambe_db",
    "usr": "root2"
}
connect_name = "postgres"
# Creating New Configuration & Store Credentials
config.set(connect_name,postgres, None)
```


```python
# Get SQL Configurations
config.get("sql")
# Result:
```




    {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root'}




```python
# Get Postgrss Configurations
config.get("postgres")
# Result:
```




    {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root2'}




```python
# Get Postgres Database Name
config.get("postgres","db_name")
# Result
```




    'sambe_db'




```python
# Get SQL Host
config.get("sql","host")
# Result:
```




    'localhost'




```python
# Get All Configurations In The Current Namespace
config.get_all()
# Result
```




    {'sql': {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root'},
     'postgres': {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root2'}}




```python
# Persists Every Configuration From All Namespaces
config.persist()
```


```python
# Persists Configurations In The confo/database Namespace
config.persist(namespace="confo/database")
```


```python
# Persists Configuration In Namespace
config.persist(namespace="confo/database", config="sql")
config.persist(namespace="confo/database", config="postgres")
```


```python
# Gets The Number Of Configurations In The Namespace
config.get_count()
```




    2




```python
                                        """NEW INSTANCE"""
# Instantiate Consul Backend Instance 
config2 = Confo()
cr2 = {"default_host": "127.0.0.1",
      "default_port": 8500,
      "default_scheme": 'http',
      "api_version": 'v1'}
config2.load_backend(credentials=cr2, name="Consul2Backend", backend_type=BE.CONSUL_BACKEND)
```


```python
# Get Backends
config2.get_backends()
# Result
```




    {'all_backends': ['ConsulBackend', 'Consul2Backend'],
     'active_backend': 'ConsulBackend'}




```python
# Activate New Backend
config2.activate_backend("Consul2Backend")
```


```python
# Get Backends
config2.get_backends()
# Result
```




    {'all_backends': ['Consul2Backend', 'ConsulBackend'],
     'active_backend': 'Consul2Backend'}




```python
# Get Namespaces
config.get_namespaces()
# Result
```




    {'all_namespaces': ['confo/database']}




```python
# Create New Namespace
config2.create_namespace("database")
```


```python
# Get Namespaces
config.get_namespaces()
# Result
```




    {'all_namespaces': ['confo/database']}




```python
# Use Namespace Etcd
config2.use_namespace("database")
```


```python
# Reload Configurations & Set New Credentials For SQL
config2.reload()
config2.set("sql","user","rad")
config2.set("sql","permissions","R,W,D,U")
```


```python
# Get All Configurations
config.get_all()
# Result
```




    {'postgres': {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root2'},
     'sql': {'host': 'localhost',
      'db_name': 'sambe_db',
      'usr': 'root',
      'user': 'rad',
      'permissions': 'R,W,D,U'}}


