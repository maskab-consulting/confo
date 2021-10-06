


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## About Confo
Confo is a flexible multi backend configuration manager for python. Built to provide a unified configuration management
interface in different environments.Confo supports both local configuration with json files and distributed configurations,
best suited for micro-service and distributed systems development. Confo defines 4 core objects:
- **Backend** : A backend object represents a storage system where the configurations are loaded; e.g `BE.FILE_BACKEND` uses a filesystem as a storage mechanism.
- **Namespace** : A namespace represents a virtual grouping of configurations, this can be used to map configurations by department,SaaS tenant, application etc.
- **Configuration** : This is a named object that represents the configurations of a specific system e.g `database`,`task_manager`
- **Field** : This represents the individual fields and their respective values in each configuration e.g in the `database` configuration 
          there are `host`,`port`,`password` and `username` fields.


Now to summarize  Confo is a **multi backend** configuration management system, meaning it manages configurations from multiple storage backends,and each Confo instance can manage **multiple backend instances**,
which means you can have `BE.FILE_BACKEND 1` which reads from `directory1` and `BE.FILE_BACKEND 2` which reads from `directory 2`, or `BE.ZOOKEEPER_BACKEND 1` which 
is connected to `first.zookeeper.server` and `BE.ZOOKEEPER_BACKEND 2` which is connected to `second.zookeeper.server`. This allows an application to pull configuration data from 
multiple sources with a consistent and intuitive python API.


## Getting started
1.Installation and Getting Started
```
pip install confo

```
Confo uses a singleton object as the main interface into all your configurations; meaning it can safely be used in multiple 
parts of an application. To start lets import Confo then create the Confo configuration manager object. Then

```python
from confo.Confo import Confo
import confo.Backends as BE # load all backend definitions

#create the singleton configuration manager object 
config = Confo()

```

<br>
2. Setup Backends<br><br>

Confo currently supports seven backends, a `filesystem` backend, a `ZooKeeper` backend,  `Etcd` backend,  `Consul` backend,  `Redis` backend, 
 `Database` backend and  `Elastic Search` backend.
To setup a backend we use the `load_backend` method:

```python
cred = {} # a dictionary definition of the needed access credentials, of the given backend_type
name = "" # a unique string for the backend instance 
type  = BE.FILE_BACKEND # a backend type 
config.load_backend(credentials=cred,name=name,backend_type=type)

```


2.1 <a href="docs/backends/filesystem_backend.md">Filesystem backend</a>

2.2 <a href="docs/backends/zookeeper_backend.md">Zookeeper Backend</a>

2.3 <a href="docs/backends/etcd_backend.md">Etcd Backend</a>

2.4 <a href="docs/backends/consul_backend.md">Consul Backend</a>

2.5 <a href="docs/backends/redis_backend.md">Redis Backend</a>

2.6 <a href="docs/backends/database_backend.md">Database Backend</a>

2.7 <a href="docs/backends/elasticsearch_backend.md">Elastic Search Backend</a><br><br>

3. Operations

3.1 <a href="docs/operations/backend operations">Backend Operations</a>

3.2 <a href="docs/operations/namespace operations">Namespace Operations</a>

3.3 <a href="docs/operations/configuration level operations">Configuration Level Operations</a><br><br>

4. Persistance

4.1 <a href="docs/persistance/backend level">Backend Level</a>

4.2 <a href="docs/persistance/namespace level">Namespace Level</a>

4.3 <a href="docs/persistance/configuration level">Configuration Level</a>

4.4 <a href="docs/persistance/reload">Reload</a>



