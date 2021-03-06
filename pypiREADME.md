

![Logo](https://raw.githubusercontent.com/n3rdydad/confo/master/assets/logo.png?style=centerme)



<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">

<a href="#"><img src="https://travis-ci.org/laravel/framework.svg" alt="Build Status"></a>

<a href="#"><img src="https://poser.pugx.org/laravel/framework/v/stable.svg" alt="Latest Stable Version"></a>

</p>

## About the platform

The Strats analytics platform is a system that manages analytics workloads whether as:

<ol>

<li>realtime analytics</li>

<li>ETL</li>

<li>Ad-hoc analysis of streaming events</li>

<li>Batch processing of data</li>

<li>Archiving</li>

<li>Replay</li>

<li>metric logging and auditing</li>

</ol>

The system takes the pain out of data science/engineering/streaming related projects  by facilitating common tasks

used in most data science/streaming projects, such as:

- High performance event stream processing.

    - <a href="https://kafka.apache.org/"> Apache Kafka </a>

    - <a href="https://kafka.apache.org/documentation/streams/">Apache Kafka streaming API</a>

    - <a href="https://ksqldb.io/quickstart.html">ksqlDB</a>

    - <a href="https://docs.confluent.io/platform/current/schema-registry/schema_registry_tutorial.html">Schema Registry</a>

    - <a href="https://kafka.apache.org/documentation/#connect">Kafka Connect</a>

    - <a hre="workflow.md">Custom Strats workflow manager (stream functions)</a>

- Distributed Storage system

    - [Full block replication](docs/storage.md)

    - [Built on GlusterFS ](https://www.gluster.org/)

    - [Automatic Archiving ](docs/storage.md)

    - [Posix Compliant FS](https://www.novell.com/documentation/open-enterprise-server-2018/bkup_sms_lx/data/bvapnj6.html?view=print#:~:text=POSIX%2Dcompliant%20means%20file%20systems,enabled%20user%20performing%20the%20backup.)

    - Petabyte Scale capability

    - Quota management

    - Geo-replication support

    - Snapshot and versioning

    - [Bitrot detection](https://en.wikipedia.org/wiki/Data_degradation)

- Distributed compute engine

    - Uses [Zookeeper](https://zookeeper.apache.org/) for distributed state

    - Runs scalable functions

    - Runtime Catalog

    - self healing

    - Horizontally scalable.

    - Built dev/ops tooling

- Distributed container orchestration engine

    - Manage OCI image life cycle

    - Manage OCI runtime

    - All other components of the platform are deployed in here.

    - Integrate with storage system

    -

- Platform portal

    - [Notebook server management ](notebook_server.md).

    - Multiple back-ends for artifact [persistance](persistance.md).

    - [Managed collaborations](collaboration_RBAC.md).

    - [Project]() and [Team](docs/collaboration_RBAC.md) level [RBAC](docs/collaboration_RBAC.md)

    - [API gateway](docs/production.md)

    - [Data virtualization Layer](docs/virtualization.md).

    - Multiple processing [back-ends](docs/processing_backends.md).

    - CI / CD management

    - The portal is accessible, powerful, and provides tools required for large, robust data streaming applications.

## System Overview

[comment]: <> (<img src="./docs/Assets/system_overview.png"/>)

![System overview](docs/Assets/system_overview.png "System overview")


## Users section

Please check [User Manual](docs/usermanual.md)

## Developer getting started

- **[Tech stack break down](docs/developer/tech_stack.md)**

- **[Installation](docs/developer/installation.md)**
