


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Zookeeper Backend
The zookeeper backend uses <a href="https://zookeeper.apache.org/">Apache Zookeeper</a> as a storage mechanism.ZooKeeper is a centralized service for maintaining configuration information, naming,
providing distributed synchronization, and providing group services. Zookeeper is a one of the popular systems used in building distributed applications.We use zookeeper as a backend
for `Confo` essentially abstracting away the complex zookeeper API. The advantage of using Confo in this environment is that you get the same API 
when testing locally and when deploying on production

##### Zookeeper Quick Overview
ZooKeeper allows distributed processes to coordinate with each other through a shared hierarchical 
name space of data registers (we call these registers znodes), much like a file system.
Unlike normal file systems ZooKeeper provides its clients with high throughput, low latency,
highly available, strictly ordered access to the znodes.
The performance aspects of ZooKeeper allow it to be used in large distributed systems.
The reliability aspects prevent it from becoming the single point of failure in big systems. 
Its strict ordering allows sophisticated synchronization primitives to be implemented at the client.
Znodes are analogous to files and directory at the same time. Because a Znode can have children Znodes like a 
directory can have subdirectories and files.Also every znode can store data just like a file.  


Every instance of `BE.ZOOKEEPER_BACKEND` has these 4 components:

- **Backend**:  A zookeeper server connection. When a `BE.ZOOKEEPER_BACKEND` instance is created a `confo` znode is created automatically under the 
  root znode `/`, so every Confo managed zookeeper cluster must have this `/confo` znode.
- **Namespace**: Every child Znode of `/confo` is considered a namespace and will not be queried for data. 
- **Configuration**: Every child of a `namespace znode` is considered a configuration znode and are expected to have json object stored within
- **Field** : A field is simply a key/value pair stored in the json object, e.g `host`:`10.222.194.106` , `port`: `3306`. A field can have a value which is an object. e.g to store a list of 
   `admin email addresses` one can use `admins`: ["kabelo.masemola@sambe.co.za","bhavesh.lala@sambe.co.za"].

### The credentials dictionary

```python
from confo.Confo import Confo
import confo.Backends as BE
#create the singleton configuration manager object 
config = Confo()
# Instantiate a ZOOKEEPER_BACKEND backend 
cred = {"zookeeper_host":"127.0.0.1","zookeeper_port":"2181",
        #if your zookeeper instance has password authentication we can also send 

        "zookeeper_user":"kabelo",
        "zookeeper_passwd":"confoRocks"
        }
config.load_backend(credentials=cred,name="zookeeper_backend",backend_type=BE.ZOOKEEPER_BACKEND )
```


For  `BE.ZOOKEEPER_BACKEND` the credentials dictionary has the following properties:

- **zookeeper_host** : This is address of the zookeeper cluster's master. 
- **zookeeper_port** : This is the port needed to connect to the zookeeper.
- **zookeeper_user** : This is the zookeeper username
- **zookeeper_passwd** :This is the zookeeper password. 

**Note:**
You can use the  `BE.FILE_BACKEND` to store the credentials for zookeeper. Then use Confo itself to create the zookeeper backend.

### Usage


 Now imagine we have znodes `systemA` and `systemB` under the `confo` znode:

``` 
"/"                                                                          ->zookeeper root 
  |________"confo"                                                           -> confo root ("/confo")
            |_________"systemA"                                              -> namespace called "systemA" ("/confo/systemA")
            |             |__________"database"                              -> a configuration called "database" ("/confo/systemA/database")
            |                           |______________host: 127.0.0.1       -> a configuration field called "host"
            |                           |______________port: 3306 
            |                           |______________user: root 
            |                           |______________password: newpassword
            |                           |______________vendor: postgres 
            |
            |_____________"systemB"                                          -> namespace called "systemB" ("/confo/systemB")  
                            |__________"email"                               -> a configuration called "email" ("/confo/systemB/email")
                                           |___________ "port":587           -> a configuration field called "port"
                                           |___________ "smtp_server": "smtp.gmail.com"
                                           |___________ "sender_email":"confo@sambe.co.za"
                                           |___________ "password" :"ThisIsAStrongPasswordTrustMeItIs"            
                                        

```


```python
from confo.Confo import Confo
import confo.Backends as BE
import smtplib, ssl
from sqlalchemy import create_engine

config = Confo()
cred = {"zookeeper_host":"127.0.0.1","zookeeper_port":"2181",

        }

config.load_backend(credentials=cred,name="zookeeper_backend",backend_type=BE.ZOOKEEPER_BACKEND )

    

```
