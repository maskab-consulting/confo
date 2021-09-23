2.3 ETCD backend

The etcd backend saves the configurations to etcd.Imagine you have a sales database with credentials you want to expose to your application, and you want to use a sales forecasting model which is exposed via REST api.
Confo uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the
`sales` namespace and every configuration concerned with systems from the `anlytics team` can be store in a namespace called `analytics`.

An example of how configurations can be set and retrieved is shown below.

In order to use etcd, you must first import confo and create a singleton configuration object. You then define etcd credentials to connect to the etcd client.

The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type.
The etcd backend accepts a dictionary of credentials  `cred` to connect.

```python
from confo.Confo import Confo
from confo import Backends as BE
from confo.Backends.EtcdBackend import EtcdBackend

# Create the singleton configuration manager object
config = Confo()

# Instantiate a ETCD_BACKEND backend 
cred = {"host":"127.0.0.1",  
        "port":2379}
config.load_backend(credentials=cred,name="ETCD_backend",backend_type=BE.ETCD_BACKEND)

```
#### backed operations 

To list all backends loaded 


```python
# Gets all backends

print(config.get_backends())

#RESULTS

{'all_backends': ['ETCD_backend'], 'active_backend': None}
```

This return a dictionary with two keys: `all_backends` holds  list of all backends registered in this application; and `active_backend` holds the 
name of the currently active backend.Note that activate_backend is None meaning the manager cannot access any configuration.If any of the configuration 
level methods are invoked a `BackendsActivationException` error is raised.Now to make sure a backend is active,


```python
# Activates the backend

config.activate_backend("ETCD_backend")
print(config.get_backends()) 

#RESULTS

{'all_backends': ['ETCD_backend'], 'active_backend': 'ETCD_backend'}

```

Now the `config.get_backends()` returns all backends and the backend that we just activated.

#### Namespace operations

As mentioned above namespaces create a logical partition between groups of configuration, this becomes more 
useful when dealing with distributed configurations, where multiple microservices are accessing and sharing configuration and data through Confo.


```python
# This method creates a namespace
config.create_namespace("database")

# Activate the namespace
config.use_namespace("database")

# Returns all namespaces and shows the active namespace
print(config.get_namespaces())

#RESULTS:

{'all_namespaces': ['/confo/database'], 'current_namespace': '/confo/database'}
```

Please note we need to choose a namespace to use before we can access any configuration. If no namespace is chosen 
a `NamespaceNotLoadedException` error will be raised.


```python
# Returns all the namespaces
print(config.get_count())

#RESULTS

1
```
The method above returns the count of all namespaces,since we have only created a single namespace.


#### configuration level operations

Now lets get all configurations in the current namespace.


```python
# Define configurations 

postgress = {'driver': 'postgress',
            'host': '127.0.0.1',
             'port':5678,
            }

# Save configuration 
config.set("postgress", postgress,None)
```

Above we set our first configuration to connect to a postgres database.

```python
# Define another configurations 
mysql = {'driver': 'mysql',
        'host': 'localhost',
          'port':1234,
        }
# Save configuration 
config.set("mysql", mysql,None)
```
Since Confo is designed to store different types of configurations, above we set our second configurations that connects to mysql database.

```python
# Get only the host
print(config.get("mysql","host"))

#RESULTS

localhost
```
Since we have set 2 different configurations, we can now get a single key of each configuration by specifying the name of the configuration and the key in the configuration.
    

```python
# Returns all the configurations
print(config.get_all())

#RESULTS

{
    'postgress': {'driver': 'postgress', 'host': '127.0.0.1', 'port': 5678}, 
    'mysql': {'driver': 'mysql', 'host': '1123356', 'port': 1234}
 }

```
Now that we have set multiple configurations, using `config.get_all()` will return all configurations that we have set.


```python
# Push configurations from Confo instance to ETCD 
print(config.persist())
```
Since the configurations are store inside the confo instance, `config.persist()` method will push all configurations from confo to the etcd.

```python
# Pull configurations from ETCD
print(config.reload())
```

Now that we have our configurations pushed to the etcd, we can retrieve them by using the `config.reload()` method. 
The method will reload all the configurations to the new instance of confo.

Below is how we reload the configurations from etcd to the new confo instance.We still use the same processes of creating confo instance, connecting to the etcd client, loading and getting of backends. 


```python
# Created a new instance of Confo to use the Reload method, and used reload to pull configurations from ETCD to the new Confo instance. 

config2 = Confo()

# Instantiate a ETCD_BACKEND backend 
cred = {"host":"127.0.0.1",  
        "port":2379}
config2.load_backend(credentials=cred,name="ETCD_backend2",backend_type=BE.ETCD_BACKEND)

```
Above we create a new instance and load the backend.

```python
config2.activate_backend("ETCD_backend2")
print(config2.get_backends()) 

#RESULTS 

{'all_backends': ['ETCD_backend2', 'ETCD_backend'], 'active_backend': 'ETCD_backend2'}

```

We now activate and get the backends of the new confo instance.


```python
config2.get_namespaces()
config2.create_namespace("database")
config2.use_namespace("database")
print(config2.get_namespaces())

#RESULTS 

{'all_namespaces': ['/confo/database'], 'current_namespace': '/confo/database'}

# Reloads the configurations from ETCD to the new ETCD
config2.reload()
```

As you can see, above we use the `config2.reload()` method to load the configuration.

```python
# New Confo instance had no configurations but reload method pushed the configutions into it.

config2.get_all()

#RESULTS 

{
    'mysql': {'driver': 'mysql', 'host': '1123356', 'port': 1234},
    'postgress': {'driver': 'postgress', 'host': '127.0.0.1', 'port': 5678}
}
```

If we now use `config2.get_all()`, we will be able to get configurations that we have only set on the first instance of confo. The method has realoaded our configurations from etcd to new confo instance.
