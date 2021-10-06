


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Etcd Backend
##### Reload

Now that we have our configurations pushed to the etcd, we can retrieve them by using the `config.reload()` method. The method will reload all the configurations to the new instance of `confo`.

```python
# Pull configurations from ETCD
print(config.reload())
```

Below is how we reload the configurations from etcd to the new `confo` instance.We still use the same processes of creating confo instance, connecting to the etcd client, loading and getting of backends.

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

We now activate and get the backends of the new `confo` instance.

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

If we now use `config2.get_all()`, we will be able to get configurations that we have only set on the first instance of `confo`. The method has reloaded our configurations from etcd to new `confo` instance.
