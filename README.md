<h1> Introduction to Etcd </h1>
Etcd is an open-source key value data store, used to manage and store data that help keep distributed
systems running. Etcd is most well known for being one of the core components of Kubernetes, where it
stores and manages Kubernetes state data, configuration data and metadata. Etcd can be relied upon to
be a single source of truth at any given point in time.
<h3>Getting Started</h3>
<p>Install Etcd</p>
<p>1. To help with the commands that follow, set these environment variables:</p>

```
ETCD_VER=v3.5.0
ETCD_BIN=/tmp/test-etcd
GOOGLE_URL=https://storage.googleapis.com/etcd
GITHUB_URL=https://github.com/etcd-io/etcd/releases/download

```

<p>2. Download and install etcd from pre-built binaries:</p>
<li>Download the compressed archive file for your platform from <a href="https://github.com/etcd-io/etcd/releases/tag/v3.5.0">Releases</a>, choosing release <a href="https://github.com/etcd-io/etcd/releases/tag/v3.5.0">v3.5.0 </a> or later.</li>
<li>Unpack the archive file. This results in a directory containing the binaries.</li>
<li>Add the executable binaries to your path. For example, rename and/or move the binaries to a directory in your path (like `usr/local/bin `),or add the directory created by the previous step to your path.</li>
<li>From a shell, test that etcd is in your path</li>

```
$ etcd --version
etcd Version: 3.5.0
...
```




