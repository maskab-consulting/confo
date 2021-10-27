


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Etcd Backend
#### Namespace Operations

As mentioned above namespaces create a logical partition between groups of configuration, this becomes more 
useful when dealing with distributed configurations, where multiple microservices are accessing and sharing configuration and data through Confo.

Now in this backend that you activated, you create a new namespace.
```python
# This method creates a namespace
config.create_namespace("database")

# Activate the namespace
config.use_namespace("database")
```

Returns all created namespaces

```python

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
