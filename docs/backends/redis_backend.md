
<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Redis Backend
The redis backend simply works by reading data, in this case it will be `configurations` that are saved in the Redis Caching System. Both Saving and Retrieving of these configurations can be done using a `Confo` instance. `Confo` uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the `sales` namespace and every configuration concerned with systems from the `analytics team` can be store in a namespace called `analytics`.

The following code snippets will showcase how to use `Confo` utilizing Redis backend.

Start by importing the `Confo` into your project
```python
# Import necessary modules

from confo.Confo import Confo
import confo.Backends as BE
```
Create a new `Confo` object `config` and load the credentials of your Redis Server. Provide a name for your backend.

```python
# Create a confo Instance
config = Confo()

# define your redis credentials
cred = {
        "redis_host":"localhost",
        "redis_port":"6379"
       }

# Load the Redis backend, give it a name of your choosing, it has to be unique
config.load_backend(credentials=cred,name="redis_backend",backend_type=BE.REDIS_BACKEND )
```
The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type.

