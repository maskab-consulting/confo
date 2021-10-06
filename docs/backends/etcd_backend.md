


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Etcd Backend
The etcd backend saves the configurations to etcd. Imagine you have a sales database with credentials you want to expose to your application, and you want to use a sales forecasting model which is exposed via REST api. `Confo` uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the `sales` namespace and every configuration concerned with systems from the `analytics` team can be store in a namespace called `analytics`.
An example of how configurations can be set and retrieved is shown below.

In order to use etcd, you must first import `confo` and create a singleton configuration object. You then define etcd credentials to connect to the etcd client.

```python
from confo.Confo import Confo
from confo import Backends as BE
from confo.Backends.EtcdBackend import EtcdBackend

# Create the singleton configuration manager object
config = Confo()
```

Create a new `Confo` object `config` and load the credentials of your ETCD Server. Provide a name for your backend.

```
# Instantiate a ETCD_BACKEND backend 
cred = {"host":"127.0.0.1",  
        "port":2379}
config.load_backend(credentials=cred,name="ETCD_backend",backend_type=BE.ETCD_BACKEND)
```


The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type. The etcd backend accepts a dictionary of credentials `cred` to connect.
