


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

Confo currently supports two backends, a `filesystem` backend and a `ZooKeeper` backend.

2.1 <a href="docs/backends/filesystem_backend.md">Filesystem backend</a>

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
The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type 
The filesystem backend accepts a dictionary of credentials which contains the `config_path` key, this is 
the path where the configurations are stored.
#### backend operations 

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

#### Namespace operations

As mentioned above namespaces create a logical partition between groups of configuration, this becomes more 
useful when dealing with distributed configurations, where multiple microservices are accessing and sharing configuration and data through Confo.

```python
#The method below is the namespace level analog to get_backends()
print(config.get_namespaces())
#RESULTS:
{'all_namespaces': ['sales', 'analytics'], 'current_namespace': '*'}

```

Please note we need to choose a namespace to use before we can access any configuration. If no namespace is chosen 
a `NamespaceNotLoadedException` error will be raised.

```python 

#choose namespace 
config.use_namespace("sales")
#check if a namespace is chosen
print(config.get_namespaces())

#RESULTS:
{'all_namespaces': ['sales', 'analytics'], 'current_namespace': 'sales'}

```

#### configuration level operations

lets get all configurations in the current namespace

```python
print(config.get_all())

#RESULTS: 
{'database': {'host': '127.0.0.1',
              'port': 5432,
              'username': 'kabelo',
              'password': 'confoRocks'}}
```

The sales department is exposing daily sales reports through a REST API, the report is read a json data 
which will be used by our application to build visualization. Lets create a new configuration programmatically, 
and store the credentials to this API. 

```python

config.set("sale_report","host","10.222.194.146")
config.set("sale_report","port","2389")
config.set("sale_report","token","01e947b6-8914-11eb-8dcd-0242ac130003")
config.set("sale_report","host","78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133")

#OR 

sales_report_data = {
    "host":"10.222.194.146",
    "port":"2389",
    "token":"01e947b6-8914-11eb-8dcd-0242ac130003",
    "secret":"78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133"
}
config.set("sale_report",sales_report_data,None)

```

The `Confo.set(config,field,value)` method creates a new configuration in the current namespace. This method 
can be used this way `Confo.set(config,field,value)`  or `Confo.set(config,dictionary,None)`, by replacing the value of `field` with a dictionary or list and replacing the last argument with None we can overload the default behaviour 
and set the configuration values directly. 

Now lets check all available configuration in the namespace:
```python
print(config.get_all())
#RESULTS: 
{'database': {'host': '127.0.0.1',
              'port': 5432,
              'username': 'kabelo',
              'password': 'confoRocks'},
 'sale_report': {'host': '10.222.194.146',
                 'port': '2389',
                 'token': '01e947b6-8914-11eb-8dcd-0242ac130003',
                 'secret': '78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133'}}
```

Perfect we can now consume configuration and metadata in a clean and decoupled way.Imagine if you have a 100 configurations and metadata
in a given namespace,the output dictionary from `Confo.get_all()` can be overwhelming to traverse. Lets find a more efficient way

```python
#Get the database host 
print(config.get("database","host"))

#RESULT
127.0.0.1

#get the database password 
print(config.get("database","confoRocks"))

#RESULTS:
confoRocks

#get the entire sale_report configuration
print(config.get("sale_report"))

#RESULT
{'host': '10.222.194.146',
 'port': '2389',
 'token': '01e947b6-8914-11eb-8dcd-0242ac130003',
 'secret': '78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133'}

#By ommiting the `field` argument `Confo.get()` returns the whole  configuration 

```
Lets assume we were able to programmatically retrieve a new secret and token for the sales report API. 
`Confo` allows us to update the configuration, by using `Confo.set()` to overwrite the old values. 

```python
new_token = "e9f2b59d-130d-4b61-b20c-94c73496655f"
new_secret = "cd58cb1d-22fc-4420-b5ab-6b67a565671d7d34f5e4-8916-11eb-8dcd"
config.set("sale_report","token",new_token)
config.set("sale_report","secret",new_secret)
print(config.get("sale_report"))

#RESULTS:
{'host': '10.222.194.146',
 'port': '2389',
 'token': 'e9f2b59d-130d-4b61-b20c-94c73496655f',
 'secret': 'cd58cb1d-22fc-4420-b5ab-6b67a565671d7d34f5e4-8916-11eb-8dcd'}

```
#### swapping namespaces
What if we now want to access the analytics's sales forecasting REST API. 

```python

#You can start by checking available namespaces 
print(config.get_namespaces())
#RESULTS: 
{'all_namespaces': ['sales', 'analytics'], 'current_namespace': 'sales'}

#Lets swap from sales to analytics.
config.use_namespaces("analytics")
print(config.get_namespaces())

#RESULTS: 

{'all_namespaces': ['sales', 'analytics'], 'current_namespace': 'analytics'}
```

After swapping namespaces check which configurations exist in analytics namespace

```python
config.get_all()

#RESULTS
{'api_one': {'host': '127.0.0.1',
             'port': 5782,
             'token': '2df228d6-890b-11eb-8dcd-0242ac130003',
             'secret': 'd51a8a7a-3286-4deb-8805-85f4528920aecfb49c0-a251-4657-87df-44996ea308ee'}}

config.get("api_one")

#RESULTS
{'host': '127.0.0.1',
 'port': 5782,
 'token': '2df228d6-890b-11eb-8dcd-0242ac130003',
 'secret': 'd51a8a7a-3286-4deb-8805-85f4528920aecfb49c0-a251-4657-87df-44996ea308ee'}

#Only `api_one` exists in the `analytics` namespace as expected
```
We have retrieved the `api_one` values lets go back to the sales namespace

```python
config.use_namespace("sales")
print(config.get_all())

#RESULTS 
{'database': {'host': '127.0.0.1',
              'port': 5432,
              'username': 'kabelo',
              'password': 'confoRocks'},
 'sale_report': {'host': '10.222.194.146',
                 'port': '2389',
                 'token': 'e9f2b59d-130d-4b61-b20c-94c73496655f',
                 'secret': 'cd58cb1d-22fc-4420-b5ab-6b67a565671d7d34f5e4-8916-11eb-8dcd'}}
```

Now if we were to open the `Configurations/` directory this is what I would find in the `sale` directory:

```
Configurations
        |___________analytics 
        |                |_________api_one.json 
        |____________sales
                       |___________database.json          
```
There is no file `Configurations/sales/sale_report.json` . The `sale_report` configuration only exists in memory. The
This allows the developer to explicitly decide when they want to persist the updated or new configuration as a 
result this helps the developer to handle cases where he creates session specific configurations, these should remain in
in memory and not be persisted.

#### persistence

`Confo` handles persistance at three levels :
```
backend level : This option persist the current state of all configuration in the current backend.
    |
    |namespace level: This option persist the current state of all configuration in the current namespace
         |
         | Configuration level: This option persists a specific configuration

```
##### backend level

```python
config.persist()
```
The code above will persist every configuration from all namespaces. 

##### namespace level

```python
config.persist(namespace="sales")
```

The above code will persist every configuration in the `sales` namespace

##### configuration level 

```python
config.persist(namespace="sales",config="sale_report")
```
The above code will persist the `sale_report` configuration only.If the configuration file already exists i will be updated.

2.2 <a href="docs/backends/zookeeper_backend.md">Zookeeper Backend</a>


Lets assume our application is operating a very distributed environments. One of the main problems in distributed systems
is finding one source of truth for application state and configuration.ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
All of these kinds of services are used in some form or another by distributed applications.We use zookeeper as a backend
for `Confo` essentially abstracting away the complex zookeeper API. The advantage of using confo in this environment is that you get the same API 
when testing locally and when deploying on production.

Lets load a zookeeper backend 

```python
# Instantiate a ZOOKEEPER_BACKEND backend 
cred = {"zookeeper_host":"127.0.0.1","zookeeper_port":"2181",
        #if your zookeeper instance has password authentication we can also send 

        "zookeeper_user":"kabelo",
        "zookeeper_passwd":"confoRocks"
        }
config.load_backend(credentials=cred,name="zookeeper_backend",backend_type=BE.ZOOKEEPER_BACKEND )

print(config.get_backend())

#RESULTS:
{'all_backends': ['example_backend', 'zookeeper_backend'],
 'active_backend': 'example_backend'}

```

Lets activate the zookeeper backend.

```python
config.activate_backend("zookeeper_backend")
config.get_backends()

#RESULTS:

{'all_backends': ['zookeeper_backend', 'example_backend'],
 'active_backend': 'zookeeper_backend'}
```

##### Zookeeper quick overview
ZooKeeper allows distributed processes to coordinate with each other through a shared hierarchical 
name space of data registers (we call these registers znodes), much like a file system.
Unlike normal file systems ZooKeeper provides its clients with high throughput, low latency,
highly available, strictly ordered access to the znodes.
The performance aspects of ZooKeeper allow it to be used in large distributed systems.
The reliability aspects prevent it from becoming the single point of failure in big systems. 
Its strict ordering allows sophisticated synchronization primitives to be implemented at the client.

Znodes are analogous to files and directory at the same time. Because a Znode can have children Znodes like a directory can have subdirectories and files.
Also every znode can store data just like a file. `Confo` depends on a znode call `confo` which it will create automatically if it does not exist.
Then every znode which is a child of `confo` is a namespace so they will not be queried for any data.Then every child of a namespace znode is considered a
configuration znode and are expected to have json object stored within. Now imagine we have znodes `systemA` and `systemB` under the `confo` znode:

``` 
"/"                                                                          ->zookeeper root 
  |________"confo"                                                           -> confo root ("/confo")
            |_________"systemA"                                              -> namespace called "systemA" ("/confo/systemA")
            |             |__________"database"                              -> a configuration called "database" ("/confo/systemA/database")
            |                           |______________host: 127.0.0.1       -> a configuration field called "host"
            |                           |______________port: 3306 
            |                           |______________user: root 
            |                           |______________password: newpassword
            |                           |______________vendor: postgres 
            |
            |_____________"systemB"                                          -> namespace called "systemB" ("/confo/systemB")  
                            |__________"email"                               -> a configuration called "email" ("/confo/systemB/email")
                                           |___________ "port":587           -> a configuration field called "port"
                                           |___________ "smtp_server": "smtp.gmail.com"
                                           |___________ "sender_email":"confo@sambe.co.za"
                                           |___________ "password" :"ThisIsAStrongPasswordTrustMeItIs"            
                                        

```

Now lets build a python app that sends an email verification link to newly registered users.We decoupled configuration from actual code by using confo:

```python
from confo.Confo import Confo
import confo.Backends as BE
import smtplib, ssl
from sqlalchemy import create_engine

config = Confo()
cred = {"zookeeper_host":"127.0.0.1","zookeeper_port":"2181",

        }

config.load_backend(credentials=cred,name="zookeeper_backend",backend_type=BE.ZOOKEEPER_BACKEND )
config.active_backend("zookeeper_backend")
config.use_namespace("systemA")
def send_email(smtp_server,sender_email,receiver_email,password,port=587):
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        message= "Please click <a href=\"http://verification-link.com\">here</a> to verify your email"
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
            # Print any error messages to stdout
            print(e)
    finally:
        server.quit()
def build_data_url(database):
    url = database['vendor'] + '://' + database['user'] + ':' + database['password']
    url = url +'@' +database['host'] + ':' + database['port'] + '/' + database['db_name'] + '?driver=' + database['driver']
    return url
def build_engine(config):
    database_config = config.get('database')
    url = build_data_url(database_config)
    engine = create_engine(url)
    return engine
def mail_recipients(engine,config):
    smtp_server = config["smtp_server"]
    port= config["port"]
    sender_email = config["sender_email"]
    password= config["password"]
    with engine.connect() as connection:
        result = connection.execute("select email from users where verified=0")
    for row in result:
        sender_email(smtp_server=smtp_server,sender_email=sender_email,receiver_email=row['email'],password=password,port=port) 
        
engine = build_engine(config)
config.active_backend("systemB")
email_config = config.get("email")
mail_recipients(engine,email_config)

    

```

The script above shows a simple use case for a robust configuration manager.

2.3 <a href="docs/backends/etcd_backend.md">Etcd Backend</a>
 

<p>Etcd is an open-source key value data store, used to manage and store data that help keep distributed
systems running. Etcd is most well known for being one of the core components of Kubernetes, where it
stores and manages Kubernetes state data, configuration data and metadata. Etcd can be relied upon to
be a single source of truth at any given point in time.</p>
<b>Install Etcd</b>
<p>1. Download and install etcd from pre-built binaries:</p>
<li>Download the compressed archive file for your platform from <a href="https://github.com/etcd-io/etcd/releases/tag/v3.5.0">Releases</a>, choosing release <a href="https://github.com/etcd-io/etcd/releases/tag/v3.5.0">v3.5.0 </a> or later.</li>
<li>Unpack the archive file. This results in a directory containing the binaries.</li>
<li>Add the executable binaries to your path. For example, rename and/or move the binaries to a directory in your path (like `usr/local/bin `),or add the directory created by the previous step to your path.</li>
<li>From a shell, test that `etcd` is in your path</li>

```
$ etcd --version
etcd Version: 3.5.0
...
```
<p> 2. Build from source </p>
<p> If you have <a href="https://golang.org/doc/install">Go version 1.13+</a>, you can build etcd from source by following these steps:</p>
<p><a href="https://github.com/etcd-io/etcd/archive/v3.4.16.zip"> Download the etcd repo as a zip file </a>and unzip it, or clone the repo using the following command.</p>

```
$ git clone -b v3.4.16 https://github.com/etcd-io/etcd.git

```
<p> To build from main@HEAD, omit the -b v3.4.16 flag.</p>
<p><b> Change directory:</b></p>

```
$ cd etcd
```
<p><b>Run the build script:</b></p>

```
$ ./build

```
<p> The binaries are under the bin directory.</p>
<p><b>Add the full path to the bin directory to your path, for example:</b></p>

```
$ export PATH="$PATH:`pwd`/bin"

```
<p><b>Test that etcd is in your path:</b></p>

```
$ etcd --version

```
2.4 <a href="docs/backends/consul_backend.md">Consul Backend</a>


<p> Consul is a service mesh solution providing a full featured control plane with service discovery, configuration, and segmentation functionality. Each of these features can be used individually as needed, or they can be used together to build a full service mesh. Consul requires a data plane and supports both a proxy and native integration model. Consul ships with a simple built-in proxy so that everything works out of the box, but also supports 3rd party proxy integrations such as Envoy.</p>

<p>1.<b> Download and install consul from precompiled binaries:</b></p>
<p> To install the precompiled binary, download the appropriate package for your system </p>
<p>1.1 Download consul for linux</p>

```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install consul

```
<p> 1.2 Install consul</p>
<p>Once the zip is downloaded, unzip it into any directory. The consul binary inside is all that is necessary to run Consul (or consul.exe for Windows). No additional files are required to run Consul.
Copy the binary to anywhere on your system. If you intend to access it from the command-line, make sure to place it somewhere on your PATH.</p>

<p>2. <b> Compiling from Source</b></p>
<p> To compile from source, you will need <a href="https://golang.org/"> Go </a> installed and configured properly (including a GOPATH environment variable set), as well as a copy of <a href="https://www.git-scm.com/"> git </a> in your PATH. </p>
<p>1. Clone the Consul repository from GitHub into your GOPATH:</p>

```
$ mkdir -p $GOPATH/src/github.com/hashicorp && cd !$
$ git clone https://github.com/hashicorp/consul.git
$ cd consul

```
<p>2. Bootstrap the project. This will download and compile libraries and tools needed to compile Consul:</p>

```
$ make tools

```
<p> 3. Build Consul for your current system and put the binary in ./bin/ (relative to the git checkout). The make dev target is just a shortcut that builds consul for only your local build environment (no cross-compiled targets).</p> 

```
$ make dev

```
<p> 3. <b>Verifying the Installation</p></b>
<p> To verify Consul is properly installed, run consul -v on your system. You should see help output. If you are executing it from the command line, make sure it is on your PATH or you may get an error about Consul not being found</p>

```
consul -v

```

2.5 <a href="docs/backends/redis_backend.md">Redis Backend</a>


<p> Redis is an open source (BSD licensed), in-memory <b>data structure store </b>, used as a database, cache, and message broker. Redis provides data structures such as <a href="https://redis.io/topics/data-types-intro#strings"> strings </a>, <a href="https://redis.io/topics/data-types-intro#hashes"> hashes </a>, <a href="https://redis.io/topics/data-types-intro#lists"> lists </a>, <a href="https://redis.io/topics/data-types-intro#sets"> sets </a>, <a href="https://redis.io/topics/data-types-intro#sorted-sets"> sorted sets </a> with range queries, <a href="https://redis.io/topics/data-types-intro#bitmaps">bitmaps</a>,<a href="https://redis.io/topics/data-types-intro#hyperloglogs"> hyperloglogs </a>, <a href="https://redis.io/commands/geoadd">geospatial indexes</a>, and <a href="https://redis.io/topics/streams-intro">streams</a>. Redis has built-in replication, Lua scripting, LRU eviction, transactions, and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.</p>

<b> Installing Redis</b>

<p>1. From source code </p>
<p> Download, extract and compile Redis with:</p>

```
$ wget https://download.redis.io/releases/redis-6.2.5.tar.gz
$ tar xzf redis-6.2.5.tar.gz
$ cd redis-6.2.5
$ make
```
<p> The binaries that are now compiled are available in the src directory. </p>
<p> 2. Run Redis with:</p>

```
$ src/redis-server

```
2.6 <a href="docs/backends/database_backend.md">Database Backend</a>


<p>Key-value databases use compact, efficient index structures to be able to quickly and reliably locate a value by its key, making them ideal for systems that need to be able to find and retrieve data in constant time. Redis, for instance, is a key-value database that is optimized for tracking relatively simple data structures (primitive types, lists, heaps, and maps) in a persistent database. By only supporting a limited number of value types, Redis is able to expose an extremely simple interface to querying and manipulating them, and when configured optimally is capable of extremely high throughput.</p>

<p><b>Features of a key-value database</b> </p>

<p> A key-value database is defined by the fact that it allows programs or users of programs to retrieve data by keys, which are essentially names, or identifiers, that point to some stored value. Because key-value databases are defined so simply, but can be extended and optimized in numerous ways, there is no global list of features, but there are a few common ones:</p>

<li>Retrieving a value (if there is one) stored and associated with a given key</li>
<li>Deleting the value (if there is one) stored and associated with a given key</li>
<li>Setting, updating, and replacing the value (if there is one) associated with a given key</li><br>

2.7 <a href="docs/backends/elasticsearch_backend.md">Elastic Search Backend</a>


<p>Elasticsearch is the distributed search and analytics engine at the heart of the Elastic Stack. Logstash and Beats facilitate collecting, aggregating, and enriching your data and storing it in Elasticsearch. Kibana enables you to interactively explore, visualize, and share insights into your data and manage and monitor the stack. Elasticsearch is where the indexing, search, and analysis magic happens.</p>

<p> 1. <b>Download and install archive from linux</b></p>

<p> The Linux archive for Elasticsearch v7.14.1 can be downloaded and installed as follows: </p>

```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.14.1-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.14.1-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-7.14.1-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-7.14.1-linux-x86_64.tar.gz
cd elasticsearch-7.14.1/ 

```
<p>2. <b>Enable automatic creation of system indices</b> </p>
<p>Some commercial features automatically create indices within Elasticsearch. By default, Elasticsearch is configured to allow automatic index creation, and no additional steps are required. However, if you have disabled automatic index creation in Elasticsearch, you must configure action.auto_create_index in elasticsearch.yml to allow the commercial features to create the following indices:</p>

```
action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*

```
<p> 3. <b>Run ElasticSearch from the command line</b></p>

```
./bin/elasticsearch

```
<p> 4. <b> Check ElasticSearch is running</b></p>

```
GET /

```
























