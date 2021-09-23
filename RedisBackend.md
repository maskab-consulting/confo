2.5 Redis backend

The redis backend simply works by reading data, in this case it will be `configurations` that are saved in the Redis Caching System. Both Saving and Retrieving of these configurations can be done using a `Confo` instance.
Confo uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the
`sales` namespace and every configuration concerned with systems from the `anlytics team` can be store in a namespace called `analytics`.

The following code snippets will showcase how to use `Confo` utilizing Redis backend.

Start by importing the `Confo` into your project
```python
# Import necessary modules

from confo.Confo import Confo
import confo.Backends as BE
```
Create a new `Confo` object `config` and load the credentials of your Redis Server.
Provide a name for your backend.
```python
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
The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type.
#### Backed operations 

To list all backends loaded 

Now, activate the backend your created above using the name you provided.
```python
# Activate the backend you created
config.activate_backend("redis_backend")

# Preview the backends that are already in the instance and check if your backend is active
config.get_backends()

#RESULTS
{'all_backends': ['redis_backend'], 'active_backend': 'redis_backend'}

```

#### Namespace operations

As mentioned above namespaces create a logical partition between groups of configuration, this becomes more 
useful when dealing with distributed configurations, where multiple microservices are accessing and sharing configuration and data through Confo.


Now in this backend that you activated, you create a new namespace.
```python
# Create namespace
config.create_namespace("database")
```
Preview all created namespaces
```python
# Preview all the namespaces that are in the instance
config.get_namespaces()

#RESULTS
{'all_namespaces': ['/confo/database']}
```
To save configurations or perform other operations related to configurations, you will have to activate the namespace you want to use.
```python
# Choose to use the namespace that you created, this namespace will lead to your configurations files
config.use_namespace("database")

# Preview the currently activated namespace
config.get_namespaces()

#RESULTS
{'all_namespaces': ['/confo/database'], 'current_namespace': '/confo/database'}
```

#### Configuration level operations

lets get all configurations in the current namespace


With a namespace activated, you can now perform operations related to configurations like `set() & get()` on the `config` instance
```python
# Define your configuration credentials
mysqli = {
            "host": "localhost",
            "db_name": "sambe_db",
            "user": "root"
         }

# Configuration name
con_name = "mysqli"

# Save those configurations credentials
config.set(con_name, mysqli, None)

# Define another configuration credentials
postgres = {
            "host": "localhost",
            "db_name": "sambe_db",
            "user": "root123"
           }

# Configuration name
con_name = "postgres"

# Save those configuration credentials
config.set(con_name, postgres, None)
```
Retrieving saved configurations in a particular namespace is as just a calling `get_all()` method on a `Confo` instance.
But you can get specific with the data you want by specifying the name of the configuration you want with just `get("config_name")`
or by being super specific by supplying both the config name & field key, `get("config_name", "key")` on a `Confo` instance
```python
# Retrieve all configurations under an activated Namespace
config.get_all()

# Retrieve all configurations that are saved under "mysqli"
config.get("mysqli")

# Retrieve the value that is saved under the configuration "postgress" and has key of "db_name"
config.get("postgres", "db_name")

#RESULTS
{'host': 'localhost', 'db_name': 'sambe_db', 'user': 'root'}
```

#### persistence

`Confo` handles persistance at three levels :
```
backend level : This option persist the current state of all configuration in the current backend.
    |
    |namespace level: This option persist the current state of all configuration in the current namespace
         |
         | Configuration level: This option persists a specific configuration

```
##### backend level

```python
config.persist()
```
The code above will persist every configuration from all namespaces. 

##### namespace level

```python
config.persist(namespace="database")
```

The above code will persist every configuration in the `database` namespace

##### configuration level 

```python
config.persist(namespace="database",config="mysqli")
```
The above code will persist the `mysqli` configuration only.If the configurations already exists.


```python
# Now with this method, Push all configurations saved in this instance into Redis
config.persist()
```
`reload()` method pulls data from Redis Cache in the instance.
```python
# Pull all configurations saved in Redis into a Confo instance
config.reload()

```
To show how the `reload()` method really works, we'll have to create a new `Confo` instance then in this new instance only use the `reload` method to populate it with 
configurations saved in Redis Cache
```python
"""
###################################################################################################################

                                            NEW CONFO INSTANCE

###################################################################################################################
"""


# Recreate the same process as above, I want to show how the reload method works
# I will not set configurations for this instance but only pull them from Redis

config2 = Confo()

cred2 = {
        "redis_host":"localhost",
        "redis_port":"6379"
       }

config2.load_backend(credentials=cred,name="redis2_backend",backend_type=BE.REDIS_BACKEND )
```
Activate the backend you created above
```python
config2.activate_backend("redis2_backend")
config2.get_backends()

#RESULTS
{'all_backends': ['redis2_backend', 'redis_backend'], 'active_backend': 'redis2_backend'}
```
Preview available namespaces
```python
config.get_namespaces()

#RESULTS
{'all_namespaces': ['/confo/database']}
```
After checking all the available namespaces in the instance, You can just choose to use that namespace.
```python
config2.use_namespace("database") # /confo/database/mysqli, /confo/database/postgres
```
Now without saving any configurations in this `config2` instance,
I will pull configurations of the activated namespace that are already saved in Redis Cache and saved them
in this `config2` instance for me to use.
```python
# Here after reloading, All configurations that are saved in Redis will be pulled into this instance

config2.reload()
```
Now that configurations and their namespaces have been pulled from Redis Cache
they can be easily used.
```python
# Preview to show that for real they where  extracted

config2.get_all()

#RESULTS
{
        'postgres': {
            'host': 'localhost',
            'db_name': 'sambe_db',
            'user': 'root123'
        },
        'mysqli': {
            'host': 'localhost',
            'db_name': 'sambe_db',
            'user': 'maddox1',
            'permissions': 'read, write, delete, update'
        }
    }
```
```python
config2.get("mysqli", "host")

#RESULTS
'localhost'
```

