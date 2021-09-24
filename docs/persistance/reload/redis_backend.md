
<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Redis Backend
##### Reload

`reload()` method pulls data from Redis Cache in the instance.

```python
# Pull all configurations saved in Redis into a Confo instance
config.reload()
```
To show how the `reload()` method really works, we'll have to create a new `Confo` instance then in this new instance only use the `reload` method to populate it with configurations saved in Redis Cache

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

Now without saving any configurations in this `config2` instance, I will pull configurations of the activated namespace that are already saved in Redis Cache and saved them in this `config2` instance for me to use.

```python
# Here after reloading, All configurations that are saved in Redis will be pulled into this instance

config2.reload()
```

Now that configurations and their namespaces have been pulled from Redis Cache they can be easily used

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
