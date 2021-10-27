


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
  
Every instance of `BE.CONSUL_BACKEND` has these 4 components:

 - **Backend**: A consul server connection. When a `BE.CONSUL_BACKEND` instance is created a `confo` key is created automatically which holds this value `json {"namespaces":[]}`, so every Confo managed consul cluster must have this `confo` KV pair.
 - **Namespace**: In the consul backend all namespaces are listed in the `confo` key; if we have a namespace called `HR_dept` it is stored in `confo` -> `json {"namespaces":["HR_dept"]}`, then a new key called `HR_dept` which holds this value `json {"configurations":[]}`. All keys that are listed in the `confo` key as namespaces they will be used to query the location of `configurations`
 - **Configuration**: Every namespace key lists all its configurations. If you have a configuration called `database` in the `HR_dept` namespace , it is registered as: `HR_dept` -> `json {"configurations":["database"]}`,then a key called `HR_dept-database` is generated and holds a json representation of the database configurations.
 - **Field** : A field is simply a key/value pair stored in the json object, e.g `host:127.0.0.1` , `port: 8500`. A field can have a value which is an object. e.g to store a list of `admin email addresses` one can use `admins`: `["mahlatsi.mokwele@sambeconsulting.com","kabelo.masemola@sambe.co.za"]`.
<br>
### The credentials dictionary
 
```python
from confo.Confo import Confo
from confo import Backends as BE
from confo.Backends.ConsulBackend import ConsulBackend
import consul

# Create Configuration Manager Object
config = Confo()
cons = ConsulBackend()
cons_client = consul.Consul()
dir(cons_client)
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

# Instantiate Consul Backend
cr = {"default_host": "127.0.0.1",
      "default_port": 8500,
      "default_scheme": 'http',
      "api_version": 'v1'}
config.load_backend(credentials=cr, name="ConsulBackend", backend_type=BE.CONSUL_BACKEND)
```

For  `BE.CONSUL_BACKEND` the credentials dictionary has the following properties:

- **default_host** : This is the address of the consul cluster's master. 
- **default_port** : This is the port needed to connect to the consul.

**Note:**
You can use the  `BE.FILE_BACKEND` to store the credentials for consul. Then use Confo itself to create the consul backend.
