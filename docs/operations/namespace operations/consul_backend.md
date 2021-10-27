


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Consul Backend
#### Namespace Operations

As mentioned above namespaces create a logical partition between groups of configuration, this becomes more 
useful when dealing with distributed configurations, where multiple microservices are accessing and sharing configuration and data through Confo.

Now in this backend that you activated, you create a new namespace.
```python
# Create Namespace "database"
config.create_namespace("database")
config.create_namespace("GraphQL")
config.create_namespace("KivyMD")

```

List all created namespaces
```python
# List Namespaces
config.get_namespaces()
# Results:
     {'all_namespaces': ['confo/GraphQL', 'confo/KivyMD', 'confo/database']}

```

To save configurations or perform other operations related to configurations, you will have to activate the namespace you want to use.
```python
# Use Namespace "GraphQL"
config.use_namespace("database")

# List Namespaces To See Active/Current Namespace
config.get_namespaces()
# Results:
    {'all_namespaces': ['confo/GraphQL', 'confo/KivyMD', 'confo/database'],
     'current_namespace': 'confo/database'}

```
