


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Filesystem Backend

The filesystem backend simply works by reading json files from the filesystem. An example configuration can be setup like below. Imagine you have a 
sales database with credentials you want to expose to your application, and you want to use a sales forecasting model which is exposed via REST api.
Confo uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the
`sales` namespace and every configuration concerned with systems from the `anlytics team` can be store in a namespace called `analytics`.

```
mkdir Configurations
mkdir Configurations/sales
mkdir Configurations/analytics
echo '{"host":"127.0.0.1", "port":5432,"username":"kabelo","password":"confoRocks"}' > Configurations/sales/database.json
echo '{"host":"127.0.0.1", "port":5432,"token":"2df228d6-890b-11eb-8dcd-0242ac130003","secret":"d51a8a7a-3286-4deb-8805-85f4528920ae 
dcfb49c0-a251-4657-87df-44996ea308ee"}' > Configurations/analytics/api_one.json
```
In the setup above both namespaces only have one configuration,but each namespace can have infinite configurations. `Confo` uses a json files to store each configuration.
```
backend 
   |______namespace
             |_______configuration
                          |__________fields
                          
e.g

filesystem 
  |________sales
             |___________database 
                             |_________host : 127.0.0.1 
                             |_________port : 5432
                             |_________user : kabelo 
                             |_________password :confoRocks 
```

```python
from confo.Confo import Confo
import confo.Backends as BE

#create the singleton configuration manager object 
config = Confo()


```


The `Confo` object is a singleton, meaning you can instantiate it multiple time through the code base, but you will always have
up to date configurations loaded. 

```python
# Instantiate a FILE_BACKEND backend 
cred = {"config_path":"Configurations/"}
config.load_backend(credentials=cred,name="example_backend",backend_type=BE.FILE_BACKEND)


```
