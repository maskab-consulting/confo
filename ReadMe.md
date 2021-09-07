


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## About Confo
Confo is a flexible multi backend configuration manager for python. Built to provide a unified configuration management
interface in different environments.Confo supports both local configuration with json files and distributed configurations,
best suited for micro-service and distributed systems development.
## Getting started
1.Installation
```
pip install confo

```

2.Setup Backends 

Confo currently supports seven backends, a `filesystem` backend and a `ZooKeeper` backend.

2.1 <a href="docs/backends/filesystem_backend.md">Filesystem backend</a>

2.2 <a href="docs/backends/zookeeper_backend.md">Zookeeper Backend</a>


2.3 <a href="docs/backends/etcd_backend.md">Etcd Backend</a>


2.4 <a href="docs/backends/consul_backend.md">Consul Backend</a>


2.5 <a href="docs/backends/redis_backend.md">Redis Backend</a>


2.6 <a href="docs/backends/database_backend.md">Database Backend</a>


2.7 <a href="docs/backends/elasticsearch_backend.md">Elastic Search Backend</a>

