<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Redis Backend
#### Configuration Level Operations

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
Retrieving saved configurations in a particular namespace is as just a calling `get_all()` method on a `Confo` instance. But you can get specific with the data you want by specifying the name of the configuration you want with just `get("config_name")` or by being super specific by supplying both the config name & field key, `get("config_name", "key")` on a `Confo` instance

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

