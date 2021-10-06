


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Filesystem Backend
#### Backend Operations 

To list all backends loaded 
```python
config.get_backends()
#RESULTS:

{'all_backends': ['example_backend'], 'active_backend': None}

```
This return a dictionary with two keys: `all_backends` holds  list of all backends registered in this application; and `active_backend` holds the 
name of the currently active backend.Note that activate_backend is None meaning the manager cannot access any configuration.If any of the configuration 
level methods are invoked a `BackendsActivationException` error is raised.Now to make sure a backend is active,

```python
#activate the example_backend
config.activate_backend("example_backend")
# List backends again to see if we have an active backend
print(config.get_backends())
#RESULTS
{'all_backends': ['example_backend'], 'active_backend': 'example_backend'}

```

Note that the `activate_backend` field has the backend we activated with `Confo.activate_backend`.

