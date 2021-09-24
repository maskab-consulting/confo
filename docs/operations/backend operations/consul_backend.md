


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Consul Backend
#### Backend Operations 

To get all backends loaded 
```python
# Get Backends
config.get_backends()
# Results:
    {'all_backends': ['ConsulBackend'], 'active_backend': None}
```
This return a dictionary with two keys: `all_backends` holds  list of all backends registered in this application; and `active_backend` holds the 
name of the currently active backend.Note that activate_backend is None meaning the manager cannot access any configuration.If any of the configuration 
level methods are invoked a `BackendsActivationException` error is raised.Now to make sure a backend is active,

Now, activate the backend your created above using the name you provided.
```python
# Activate ConsulBackend
config.activate_backend("ConsulBackend")

# List Backends To See Active Backend
config.get_backends()
    {'all_backends': ['ConsulBackend'], 'active_backend': 'ConsulBackend'}
```

Note that the `activate_backend` field has the backend we activated with `Confo.activate_backend`.
