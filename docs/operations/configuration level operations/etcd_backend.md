


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Etcd Backend
#### Configuration Level Operations

lets get all configurations in the current namespace

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
Since `Confo` is designed to store different types of configurations, above we set our second configurations that connects to mysql database.

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

Now that we have set multiple configurations, using config.get_all() will return all configurations that we have set.
