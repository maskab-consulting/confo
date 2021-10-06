


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Consul Backend
#### Configuration Level Operations

With a namespace activated, you can now perform operations related to configurations like `set() & get()` on the `config` instance

```python
# Instantiate SQL & Postgress Configurations
sql = {
    "host": "localhost",
    "db_name": "sambe_db",
    "usr": "root"
}
connect_name = "sql"

# Creating New Configuration & Store Credentials
config.set(connect_name,sql, None)

postgres = {
    "host": "localhost",
    "db_name": "sambe_db",
    "usr": "root2"
}
connect_name = "postgres"

# Creating New Configuration & Store Credentials
config.set(connect_name,postgres, None)
```

Retrieving saved configurations in a particular namespace is as just a calling `get_all()` method on a `Confo` instance. But you can get specific with the data you want by specifying the name of the configuration you want with just `get("config_name")` or by being super specific by supplying both the config name & field key, `get("config_name", "key")` on a `Confo` instance

```python
# Get SQL Configurations
config.get("sql")
# Result:
    {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root'}

# Get Postgrss Configurations
config.get("postgres")
# Result:
    {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root2'}

# Get Postgres Database Name
config.get("postgres","db_name")
# Result:
    'sambe_db'
    
# Get SQL Host
config.get("sql","host")
# Result:
    'localhost'

# Get All Configurations In The Current Namespace
config.get_all()
# Result
    {'sql': {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root'},
     'postgres': {'host': 'localhost', 'db_name': 'sambe_db', 'usr': 'root2'}}
```

