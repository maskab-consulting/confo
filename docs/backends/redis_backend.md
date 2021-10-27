
<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Redis Backend
The redis backend simply works by reading data, in this case it will be `configurations` that are saved in the Redis Caching System. Both Saving and Retrieving of these configurations can be done using a `Confo` instance. `Confo` uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the `sales` namespace and every configuration concerned with systems from the `analytics team` can be store in a namespace called `analytics`.

Every instance of `BE.REDIS_BACKEND` has these 4 components:

 - **Backend**: A redis server connection. When a `BE.REDIS_BACKEND` instance is created a `confo` key is created automatically which holds this value `json {"namespaces":[]}`, so every Confo managed redis cluster must have this `confo` KV pair.
 - **Namespace**: In the redis backend all namespaces are listed in the `confo` key; if we have a namespace called `HR_dept` it is stored in `confo` -> `json {"namespaces":["HR_dept"]}`, then a new key called `HR_dept` which holds this value `json {"configurations":[]}`. All keys that are listed in the `confo` key as namespaces they will be used to query the location of `configurations`
 - **Configuration**: Every namespace key lists all its configurations. If you have a configuration called `database` in the `HR_dept` namespace , it is registered as: `HR_dept` -> `json {"configurations":["database"]}`,then a key called `HR_dept-database` is generated and holds a json representation of the database configurations.
 - **Field** : A field is simply a key/value pair stored in the json object, e.g `host: localhost` , `port: 6379`. A field can have a value which is an object. e.g to store a list of `admin email addresses` one can use `admins`: `["tshepang.maila@sambeconsulting.com","kabelo.masemola@sambe.co.za"]`.
<br>
### The credentials dictionary
 
```
# Import necessary modules
from confo.Confo import Confo
import confo.Backends as BE

# Create a confo Instance
config = Confo()

# define your redis credentials
cred = {
        "redis_host":"localhost",
        "redis_port":"6379"
       }

# Load the Redis backend, give it a name of your choosing, it has to be unique
config.load_backend(credentials=cred,name="redis_backend",backend_type=BE.REDIS_BACKEND )
```

For  `BE.REDIS_BACKEND` the credentials dictionary has the following properties:

- **redis_host** : This is the address of the redis cluster's master. 
- **redis_port** : This is the port needed to connect to the redis.

**Note:**
You can use the  `BE.FILE_BACKEND` to store the credentials for redis. Then use Confo itself to create the redis backend.


