


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Consul Backend
  Consul is a centralized service for providing a full featured control plane with service discovery, configuration, 
  and segmentation functionality. In some form of way, the services are used by other distributed applications. 
  Consul is used as a Confo backend for abstraction of the Consul API.

The following code snippets will showcase how to use `Confo` utilizing Consul backend.
Start by importing the `Confo` into your project

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
```python
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
```
Create a new `Confo` object `config` and load the credentials of your Consul Server. Provide a name for your backend.

```python
# Instantiate Consul Backend
cr = {"default_host": "127.0.0.1",
      "default_port": 8500,
      "default_scheme": 'http',
      "api_version": 'v1'}
config.load_backend(credentials=cr, name="ConsulBackend", backend_type=BE.CONSUL_BACKEND)
```
The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type.
