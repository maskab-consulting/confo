


<p align="center"><img src="https://raw.githubusercontent.com/sambe-consulting/confo/master/assets/logo.png" width="400"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Distributed configuration manager for python</h3></p>

<p align="center">
<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## Zookeeper Backend

Lets assume our application is operating a very distributed environments. One of the main problems in distributed systems
is finding one source of truth for application state and configuration. ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
All of these kinds of services are used in some form or another by distributed applications. We use zookeeper as a backend
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
