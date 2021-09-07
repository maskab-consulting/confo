<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Redis Backend
#### Configuration Level Operations

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
