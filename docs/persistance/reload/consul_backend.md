


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Consul Backend
##### Reload

`reload()` method pulls data from Consul Cache in the instance.

```python
# Pull all configurations saved in Consul into a Confo instance
config.reload()
```
To show how the `reload()` method really works, we'll have to create a new `Confo` instance then in this new instance only use the `reload` method to populate it with configurations saved in Consul Cache

```python
"""
###################################################################################################################

                                            NEW CONFO INSTANCE

###################################################################################################################
"""       

# Instantiate Consul Backend Instance 
config2 = Confo()
cr2 = {"default_host": "127.0.0.1",
      "default_port": 8500,
      "default_scheme": 'http',
      "api_version": 'v1'}
config2.load_backend(credentials=cr2, name="Consul2Backend", backend_type=BE.CONSUL_BACKEND)

# Get Backends
config2.get_backends()

# Result
{'all_backends': ['ConsulBackend', 'Consul2Backend'],
 'active_backend': 'ConsulBackend'}
```

Activate the backend you created above

```python
# Activate New Backend
config2.activate_backend("Consul2Backend")

# Get Backends
config2.get_backends()

# Result
{'all_backends': ['Consul2Backend', 'ConsulBackend'],
 'active_backend': 'Consul2Backend'}
```

Create and get available namespaces

```python
# Create New Namespace
config2.create_namespace("database")

# Get Namespaces
config.get_namespaces()

# Result
{'all_namespaces': ['confo/database']}
```

After checking all the available namespaces in the instance, You can just choose to use that namespace

```python
# Use Namespace Etcd
config2.use_namespace("database")
```

Now without saving any configurations in this `config2` instance, I will pull configurations of the activated namespace that are already saved in Consul Cache and save them in this `config2` instance.

```python
# Reload Configurations & Set New Credentials For SQL
config2.reload()
config2.set("sql","user","rad")
config2.set("sql","permissions","R,W,D,U")
```

Now that configurations and their namespaces have been pulled from Consul Cache they can be easily used

```python
# Get All Configurations
config.get_all()

# Result
{'postgres': {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root2'},
 'sql': {'host': 'localhost',
  'db_name': 'sambe_db',
  'usr': 'root',
  'user': 'rad',
  'permissions': 'R,W,D,U'}}
```

