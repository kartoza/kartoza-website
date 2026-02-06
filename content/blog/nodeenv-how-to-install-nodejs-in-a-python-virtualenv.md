---
title: "Nodeenv: How to Install Nodejs in a Python Virtualenv"
description: "At Kartoza, the team uses Python virtual environments as standard practice for development. The article explains how to use nodeenv, which provides isolated Node.js environments similar to Python virtualenv."
tags:
  - Python
  - Node.js
  - Development
date: 2014-08-24
author: "Gavin Fleming"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Nodeenv: How to Install Nodejs in a Python Virtualenv"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
At Kartoza, the team uses Python virtual environments as standard practice for development. The article explains how to use nodeenv, which provides isolated Node.js environments similar to Python virtualenv.
{{< /block >}}

## Main Article

Here at Kartoza, working in python virtual environments is our default modus operandi when embarking on any python development. For some time we have been enjoying yuglify, tilemill and other node.js based applications as part of our workflow, and early on in my use of these technologies I discovered nodeenv - mainly because I had been bitten on the ass by different node applications on the same host expecting to have different versions of node.js. Nodeenv provides a python virtualenv like environment for sandboxing your node applications so that each can run under its own discrete version of node.js. It operates very much like python virtualenv does and in fact it requires virtualenv so for pythonistas it is a very good fit! In this article I document the steps needed to get node running under such an environment.

## Install host operating system dependencies

You need to have python-virtualenv and curl installed - under ubuntu and debian derived distros you can simply do:

```bash
sudo apt-get install python-virtualenv curl
```

## Setup your virtualenv and install nodeenv in it

```bash
DEV=${HOME}/dev/javascript/nodedemo
mkdir -p $DEV; cd $DEV
virtualenv venv
source venv/bin/activate
pip install nodeenv
```

You should see output similar to this after running the above commands:

```
Downloading/unpacking nodeenv
 Using download cache from /home/timlinux/.cache/pip/https%3A%2F%2Fpypi.python.org%2Fpackages%2Fsource%2Fn%2Fnodeenv%2Fnodeenv-0.11.0.tar.gz
 Running setup.py (path:/home/timlinux/dev/javascript/nodedemo/venv/build/nodeenv/setup.py) egg_info for package nodeenv

 no previously-included directories found matching 'debian/nodeenv'
 no previously-included directories found matching 'debian/sdist'
 warning: no previously-included files matching '*.log' found under directory 'debian'
 warning: no previously-included files matching '*.substvars' found under directory 'debian'
 warning: no previously-included files matching 'files' found under directory 'debian'
 Installing collected packages: nodeenv
 Running setup.py install for nodeenv

 no previously-included directories found matching 'debian/nodeenv'
 no previously-included directories found matching 'debian/sdist'
 warning: no previously-included files matching '*.log' found under directory 'debian'
 warning: no previously-included files matching '*.substvars' found under directory 'debian'
 warning: no previously-included files matching 'files' found under directory 'debian'
 Installing nodeenv script to /home/timlinux/dev/javascript/nodedemo/venv/bin
 Successfully installed nodeenv
 Cleaning up...
```

Now we need to install node and npm (the node package manager) into the nodeenv. And here is the good part - you can install a specific version in the process:

```bash
source nenv/bin/activate

nodeenv --node=0.10.31 nenv
```

**Update (5 Sept 2014):** The nodeenv `-p` option will install node into your python venv which will make your life easier probably.

## Using your shiny new virtual node installation

Once npm is installed you can then go on to install any node packages using npm. For example here we install and run the nodeschool tutorial packages:

```bash
npm install -g learnyounode
learnyounode
```

**Note:** Do remember that you need to source your python virtualenv and nodeenv before you use your virtual node env:

```bash
source venv/bin/activate
source nenv/bin/activate
```

## Troubleshooting: If you get something like this when building:

```
 * Install node.js (0.4.6) ..Traceback (most recent call last):
 File "/home/timlinux/dev/javascript/nodedemo/venv/bin/nodeenv", line 9, in <module>
 load_entry_point('nodeenv==0.11.0', 'console_scripts', 'nodeenv')()
 File "/home/timlinux/dev/javascript/nodedemo/venv/local/lib/python2.7/site-packages/nodeenv.py", line 765, in main
 create_environment(env_dir, opt)
 File "/home/timlinux/dev/javascript/nodedemo/venv/local/lib/python2.7/site-packages/nodeenv.py", line 674, in create_environment
 install_node(env_dir, src_dir, opt)
 File "/home/timlinux/dev/javascript/nodedemo/venv/local/lib/python2.7/site-packages/nodeenv.py", line 563, in install_node
 build_node_from_src(env_dir, src_dir, node_src_dir, opt)
 File "/home/timlinux/dev/javascript/nodedemo/venv/local/lib/python2.7/site-packages/nodeenv.py", line 537, in build_node_from_src
 callit([make_cmd] + make_opts, opt.verbose, True, node_src_dir, env)
 File "/home/timlinux/dev/javascript/nodedemo/venv/local/lib/python2.7/site-packages/nodeenv.py", line 420, in callit
 % (cmd_desc, proc.returncode))
 OSError: Command make --jobs=2 failed with error code 2
```

Older versions of node don't always build nicely - try using a more recent version.

## Troubleshooting: If you are behind an http proxy, you should first tell npm:

```bash
nenv/bin/npm config set proxy http://192.168.2.2:3128
nenv/bin/npm config set https-proxy http://192.168.2.2:3128
```

## Troubleshooting: /usr/bin/env: node: No such file or directory

Make sure you have sourced venv and node:

```bash
source venv/bin/activate
source nenv/bin/activate
```

For more information on how to use nodeenv, please see the nodeenv project page on github.
