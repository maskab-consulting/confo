


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Etcd Backend
The Etcd backend  uses <a href="https://etcd.io/" > Etcd</a> as a storage mechanism.
Etcd is a strongly consistent, distributed key-value store that provides a reliable way to store data that needs to be
accessed by a distributed system or cluster of machines. It gracefully handles leader elections
during network partitions and can tolerate machine failure, even in the leader node. `Confo` uses etcd as one of its backends allowing developers
to build modern applications in the distributed context with ease, Confo abstracts away the details of Etcd's API in favour for a robust consistent API.

Every instance of `BE.ETCD_BACKEND` has these 4 components:

- **Backend** :  A `etcd` server connection. When a `BE.ETCD_BACKEND` instance is created a `confo` key  is created automatically
   which holds this value ```json {"namespaces":[]}```, so every Confo managed etcd cluster must have this `confo` KV pair.
- **Namespace**: In the `etcd` backend all namespaces are listed in the `confo` key; if we have a namespace called `HR_dept` it is stored in
 `confo` -> ```json {"namespaces":["HR_dept"]}```, then a new key called `HR_dept` which holds this value ```json {"configurations":[]}```. 
 All keys that are listed in the `confo` key as namespaces they will be used to query the location of `configurations`
- **Configuration**: Every namespace key lists all its configurations. If you have a configuration called `database` in the `HR_dept` namespace ,
 it is registered as:  `HR_dept` -> ```json {"configurations":["database"]}```,then a key called `HR_dept-database` is generated and holds a json representation 
 of the database configurations. 
- **Field**: A field is simply a key/value pair stored in the json object, e.g `host:10.222.194.106` , `port: 3306`.
 A field can have a value which is an object. e.g to store a list of `admin email addresses` one can use 
 `admins: ["kabelo.masemola@sambe.co.za","bhavesh.lala@sambe.co.za"]`.

```
 
 KEYS   =       confo                    ->    HR_dept                      -> HR_dept-database ->              e.g host 
 
 VALUES =     {"namespaces":["HR_dept"]} ->  {"configurations":["database"]}  -> {                           -> 127.0.0.1
                                                                                      "driver": "pgsql",
                                                                                      "host": "127.0.0.1",
                                                                                      "database": "portal",
                                                                                      "user": "gemuser",
                                                                                      "password": "gempass",
                                                                                      "prefix": ""
                                                                                    }

```


### The credentials dictionary

```python
from confo.Confo import Confo
import confo.Backends as BE
#create the singleton configuration manager object 
config = Confo()
# Instantiate a ETCD_BACKEND backend 
cred = {"host":"127.0.0.1",  
        "port":"2181",   # 
        #If you want to register pre- existing namespaces during backend loading 
        "namespaces":["HR_dept","sales"]
        }
config.load_backend(credentials=cred,name="ecommerce_configs",backend_type=BE.ETCD_BACKEND )
```

For the `BE.ETCD_BACKEND` the credentials dictionary has the following properties:
- **host**: The address of the etcd server 
- **port**: The port of the etcd server
- **namespace**: This property is optional and allows the registration of pre-existing namespaces.

**Note:**
You can use the  `BE.FILE_BACKEND` to store the credentials for etcd. Then use Confo itself to create the etcd backend.

