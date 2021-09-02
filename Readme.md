<h1>Introduction To Consul</h1>
Consul is a full featured service mesh solution that solves networking and security challenges of operating 
microservices and cloud infrastructure. It offers a software driven approach to routing and segmentation. 
Benefits include:</br>
- failure handling, retries and network observability

<b>Service Mesh</b>
<li>
Discovery
</li>
<li>
Configuration
</li>
<li>
Segmentation
</li>

<h2>Architecture View</h2>
Consul is a distributed system designed to run on a cluster of nodes. A node can be a physical server, cloud instance, 
virtual machine or container. Connected, the set of nodes Consul runs on is called a datacenter. Within the data center, 
Consul can run in two modes <b>server</b> or <b>client</b>.</br>
<b>Clients</b>  are a light weigh process that run on every node where services are running.
A <b>datacenter</b> will have 3 to 5 servers and many <b>clients</b>.
<b>Sever Agents</b> maintain the consistent state for Consul.
<b>Clients</b> register services, runs health checks, and forwards queries to servers. 
A client must be running on every node in the Consul datacenter that runs services
Non-server agents run in client mode.</br>

<h2>Use Cases</h2>
- <b>Service Discovery & Health Checking</b> - Discover, Register & Resolve Services For Application Workloads Across Any Cloud.
Automatically Add & Remove Services Based On Health Checking.
  - Features Include:
    - <b>Centralised Service Registry</b> - Which enables services to discover each other by storing location information in a
    single registry( i.e. IP Addresses)
    - <b>Real-Tme Health Monitoring</b> - Which improves resiliency by tracking health of deployed services
    - <b>Open & Extensible API </b> - Which enables users to integrate ecosystem technologies into their environments and
        service discovery at a greater scale.
    - <b>Simplified Resource Discovery</b> - Leverage DNS (Domain Name System) or HTTP interface to discover services and their 
      locations registered with consul.
    - <b>Multi-Region, Multi-Cloud</b> - Consul's distributed architecture allows it to be deployed at scale in any environment,
    region and cloud
    - <b>Built For Enterprise Scale</b> - Consul Enterprise provides the foundation for organisations to build a strong service
    networking platform at scale, with Resiliency.</br></br>
- <b>Network Infrastructure Automation</b> - Reduce deployment time for applications and eliminate manual processes by automating 
    network tasks; Enable operators to easily deploy, manage and optimise a network infrastructure.
  - Features Include:
    - <b>Dynamic Load Balancing</b> - In which consul can automatically provide service updates to load balancers, 
    eliminating their need for manual updates.
    - <b>Automated Firewalling</b> - Use of Consul-Terraform-Sync to automate security updates. Organisations can elevate
    their security posture and adopt fine access policies.
    - <b>Health Checks Visibility</b> - Consul enables operators to gain real-time insights into the service definitions
    , health, and location of applications supported by the network.
    - <b>Extended Through Ecosystems</b> - Consul's open API enables integrations with many popular networking technologies
    such as cisco and VMware.
    - <b>Flexible Architecture</b> -  Consul can be deployed in any environment and across any cloud or runtime.
    - <b>Reduction Of Downtime & Outages</b> - Consul can be used to automate networking tasks, which reduces the risk of outages
    from manual errors and driving down ticket driven operations.</br></br>
- <b>Multiplatform Service Mesh</b> - Create consistent platform for modern application networking and security with identity based
- authorisation, L7 traffic management, and service-to-service encryption.
  - Features Include:
    - <b>Multi-Datacenter, Multi-Region</b> - Merge Consul between multiple clusters and environments, creating a 
    global service mesh. Consistently apply policies and security across platforms.
    - <b>Secure Service To Service Communication</b> - Automatic mTLS (mutual authentication - ensures that the parties 
    at each end of a network connection are who they claim to be by verifying that they both have the correct private key.)
    communication between services both inside Kubernetes and in traditional runtime platforms. Extend and integrate with 
    external certificate platforms like Vault. 
    - <b>Layer 7 Traffic Management</b> - Service-to-service communication policy at Layer 7 enables progressive delivery 
    of application communication.
    - <b>Robust Ecosystem</b> - Rich ecosystem community extends Consul’s functionality into spaces such as networking, 
    observability, and security.
    - <b>Improved Observability</b> - Gain insight into service health and performance metrics with a built-in 
    visualization directly in the Consul UI or by exporting metrics to a third-party solution.

<h2>Server And Client Agents</h2>
In production, run each Consul agent in server or client mode. Each Consul datacenter must have at least ibe server that
is responsible for maintaining the Consul's state.This includes information about other Consul servers and clients, what 
services are available for discovery, and which services are allowed to talk to which other services.
Just like zookeeper, In order to ensure that Consul's state is preserved even if a server fails, 
run either three or five servers (No more than 5) in production. The odd number of servers  strikes a 
balance between performance and failure tolerance.</br>
<b>Single-server production deployments are discouraged</b>
</br><b>Warning:</b> Never run Consul in <b>-dev</b> mode in production - Does not persist any state

<h3>Start Agent In Development Mode</h3>
$ consul agent -dev </br>

After the agent has started, the logs report that the Consul agent has started and is streaming some log data. 
They also report that the agent is running as a server and has claimed leadership. Additionally, the local agent 
has been marked as a healthy member of the datacenter.

<h3>Discover Datacenter Members</h3>
$ consul members </br>
$ consul members -detailed </br>
- Run this command in a new terminal window as the consul is running on the other terminal window.
</br>The output displays your agent, its IP address, its health state, its role in the datacenter, 
and some version information. 
</br>You can discover additional metadata by providing the -detailed flag.

$ curl localhost:8500/v1/catalog/nodes </br></br>
The members command runs against the Consul client, which gets its information via gossip protocol. 
The information that the client has is eventually consistent, but at any point in time its view of the world may not 
exactly match the state on the servers. For a strongly consistent view of the world, query the HTTP API, which forwards 
the request to the Consul servers.</br>

$ dig @127.0.0.1 -p 8600 Judiths-MBP.node.consul</br></br>
In addition to the HTTP API, you can use the DNS interface to discover the nodes. The DNS interface will send your query 
to the Consul servers unless you've enabled caching. To perform DNS lookups you have to point to the Consul agent's 
DNS server, which runs on port 8600 by default

<h3>Stopping The Agent</h3>
$ consul leave </br>

Stop the Consul agent by using the consul leave command. This will gracefully stop the agent, 
causing it to leave the Consul datacenter and shut down.</br>

When you issue the leave command, Consul notifies other members that the agent left the datacenter. 
When an agent leaves, its local services running on the same node and their checks are removed from 
the catalog and Consul doesn't try to contact that node again. </br></br>

Forcibly killing the agent process indicates to other agents in the Consul datacenter that the node failed instead
of left. When a node fails, its health is marked as critical, but it is not removed from the catalog. Consul will 
automatically try to reconnect to a failed node, assuming that it may be unavailable because of a network partition, 
and that it may be coming back. </br></br>

<h3>Register A Service With Consul Service Discovery</h3>
One of the major use cases for Consul is service discovery. Consul provides a DNS interface that downstream services 
can use to find the IP addresses of their upstream dependencies.
Consul knows where these services are located because each service registers with its local Consul client. 
Operators can register services manually, configuration management tools can register services when they are deployed, 
or container orchestration platforms can register services automatically via integrations.

<h4>Define A Service</h4>

$ mkdir ./consul.d </br></br>
You can register services either by providing a service definition, which is the most common way to register services,
or by making a call to the HTTP API. Above, we are using a service definition.</br>

First, create a directory for Consul configuration. Consul loads all configuration files in the configuration directory,
so a common convention on Unix systems is to name the directory something like /etc/consul.d 
(the .d suffix implies "this directory contains a set of configuration files").</br>

</br><b>Next, write a service definition configuration file </b></br> - Scenario, there is a service named "web" running 
on port 80.create a file called web.json in the configuration directory. This file will contain the service definition:
name, port, and an optional tag you can use to find the service later on.

$ echo '{
     "service": 
        {       "name": "web",    
                "tags": ["rails"],    
                "port": 80  
        }
    }' > ./consul.d/web.json
</br></br>


Thereafter, restart the agent, using command line flags to specify the configuration directory and enable script checks 
on the agent. <b>WARNING</b>: Enabling script checks in some configurations may introduce a remote execution
vulnerability which is known to be targeted by malware. In production, it is recommended to use
-enable-local-script-checks instead. </br>

$ consul agent -dev -enable-script-checks -config-dir=./consul.d</br></br>

If you want to register multiple services, you can create multiple service definition files in the consul configuration 
directory  - consul.d

<h4>Query The Service</h4>
Once the agent adds the service to Consul's service catalog you can query it using either the DNS interface or HTTP API.

<b>DNS Interface</b></br>
The DNS name for a service registered with Consul is NAME.service.consul, where NAME is the name you used to register 
the service (in this case, web). By default, all DNS names are in the consul namespace.
The fully-qualified domain name of the web service is web.service.consul. Query the DNS interface 
(which Consul runs by default on port 8600) for the registered service.</br>

$ dig @127.0.0.1 -p *NAME.service.consul* - service subdomain tells we are querying services & name is name of 
service</br>
$ dig @127.0.0.1 -p 8600 web.service.consul </br></br>

You can also use the DNS interface to retrieve the entire address/port pair as a SRV record.</br>
SRV Record - Specification of data in the Domain Name System defining the location, i.e., the hostname and port number, 
of servers for specified services. </br>

$ dig @127.0.0.1 -p 8600 web.service.consul SRV </br></br>

The SRV record says that the web service is running on port 80 and exists on the node 
mahlatsi-Latitude-5490.node.dc1.consul. </br></br>

<b>DNS interface to filter services by tags</b></br>
Format for tag-based service queries is TAG.NAME.service.consul.</br>

$ dig @127.0.0.1 -p 8600 rails.web.service.consul</br>
- here we ask consul for all web services with the rails tag</br></br>

<b>HTTP API</b></br>
Lists all nodes hosting a given service. 
We must filter query for only healthy service instances, which DNS does automatically.
Therefore, Filter your HTTP API query to look for only healthy instances.</br>

$ curl 'http://localhost:8500/v1/health/service/web?passing' </br>

<b>Update Services</b></br>
Update the web service by registering a health check for it.
- Because you never started a service on port 80 where you registered web, the health check you register will fail.

Therefore, You can update service definitions without any downtime by changing the service definition file and sending 
a SIGHUP to the agent or running consul reload. 
Alternatively, you can use the HTTP API to add, remove, and modify services dynamically.</br>

<b>Updating The Registration File</b></br>
- Edit the registration file by running:
  - $  echo 
  '{  "service":
    { "name": "web",
      "tags": ["rails"],    
      "port": 80,    
      "check": 
      {      
         "args": ["curl","localhost" ],
         "interval": "10s"
      }  
    }
  }' > ./consul.d/web.json </br></br>

The 'check' of this service definition adds a script-based health check that tries to connect to the web service every
10 seconds via curl. 
Script based health checks run as the same user that started the Consul process.
If the command exits with an exit code >= 2, then the check will fail and Consul will consider the service unhealthy. 
An exit code of 1 will be considered as warning state.</br>
After editing the file, Reload the Consul configuration.</br>

$ consul reload - Reload configuration </br></br>

Consul's DNS server only returns healthy results. So if we query DNS for the web service again, It won't return any IP 
addresses since web's health check is failing.</br>

$ dig @127.0.0.1 -p 8600 web.service.consul

<h2>Secure Service Communication with Consul Service Mesh and Envoy</h2>
<p>Consul service mesh secures service-to-service communication with authorization and encryption. Applications can use 
sidecar proxies in a service mesh configuration to automatically establish Transport Layer Security connections for 
inbound and outbound connections without being aware of the network configuration and topology. In addition to securing 
your services, Consul service mesh can also intercept data about service-to-service communications and surface it to 
monitoring tools.</p>

https://learn.hashicorp.com/tutorials/consul/service-mesh-with-envoy-proxy?in=consul/getting-started

<h2>Store Data in Consul KV</h2>

<p>
Consul includes a key value store, which you can use to dynamically configure applications, coordinate services, manage
leader election, or serve as a data backend for Vault. Consul KV is enabled automatically on Consul agents; you don't need 
to enable it in Consul's configuration. There are two ways to interact with the Consul KV store: the Consul CLI and UI.
</p>
<h3>Add data</h3>
<p>
First, insert some values into the KV store with the consul kv put command. The first entry after the command 
is the key, and the second entry is the value.
</p>
<br>
<p>
<b>$ consul kv put redis/config/minconns 1</b><br>
<b>$ consul kv put redis/config/maxconns 25</b>
- Here the key is redis/config/maxconns and the value is set to 25.
</p>
<p>
  $ consul kv put -flags=42 redis/config/users/admin abcd1234 <br>
  The key entered Above, ("redis/config/users/admin"),a flags value of 42 is set. 
  Keys support setting a 64-bit integer flag value that isn't used internally by Consul,
  but can be used by clients to add metadata to any KV pair.
</p>

<h3>Query data</h3>
<p>
$ consul kv get redis/config/minconns <br>
- Query for the value of one of the keys<br><br>
$ consul kv get -detailed redis/config/users/admin<br>
- Retrieve the some metadata (including the "flag" ) using the -detailed command line flag. <br><br>
$ consul kv get -recurse <br>
- List all the keys in the store using the recurse options.
</p>

<h3>Delete Data</h3>
<p>
$ consul kv delete redis/config/minconns <br>
- Delete a key from the Consul KV store, issue a "delete" call.<br><br>

Consul lets you interact with keys in a folder-like way. Although all the keys in the KV store are actually 
stored flat, Consul allows you to manipulate keys that share a certain prefix as a group, as if they were in folders or 
sub-folders. <br><br>

$ consul kv delete -recurse redis <br>
Delete all the keys with the redis prefix using the recurse option. <br><br>
</p>

<h3>Modify Existing Data</h3>
<p>
$ consul kv put foo bar <br>
- Update the value of an existing key.<br><br>
$ consul kv get foo <br>
- Get the updated key. <br><br>
$ consul kv put foo zip <br>
- Put the new value at an extant "path".<br><br>
$ consul kv get foo <br>
- Check the updated path.<br><br>
</p>
<p>
Consul can perform atomic key updates using a Check-And-Set (CAS) operation.
You can explore these options on the help page for the consul kv put command.
<br>
<br>
$ consul kv put -h
</p>

<h3>Consul UI</h3>
<p>
Consul's UI allows you to view and interact with Consul via a graphical user interface, which can lower the barrier 
of entry for new users, and ease troubleshooting.
</p>
<p>
The Consul UI enables you to view all information about your Consul datacenter, including:

    Registered nodes, both Consul servers and clients.
    Registered services and their sidecar proxies.
    Registered gateways including terminating, ingress, and mesh.

Additionally, you can view and update the following information through the Consul UI:

    Key-value pairs.
    Access Control List (ACL) tokens.
    Service mesh intentions.
</p>
<p>
    
    To Access UI: Run Consul Agent -  $ consul agent -dev
    Then Proceed Too The Following Site - http://localhost:8500/ui

</p>

<h3>Creating Local Datacenter</h3>
<p>
When a new Consul agent starts, it doesn't know about other agents; it is essentially a datacenter with one member.
To add a new agent to an existing datacenter you give it the IP address of any other agent in the datacenter 
(either a client or a server), which causes the new agent to join the datacenter. Once the agent is a member of the 
new datacenter, it automatically learns about the other agents via gossip.
</p>

<h1></h1>
<p>
ihyihuu
</p>
