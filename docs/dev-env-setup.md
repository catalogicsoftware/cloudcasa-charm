# Development Environment Setup

After setting up the [test environment](https://github.com/catalogicsoftware/cloudcasa-charm/blob/master/docs/test-env-setup.md#local-environment-setup) to deploy your artifacts, you will need a development environment to build and package the charm.

Our suggestion is to create a separate VM with **Ubuntu 20.04** in order to have better compatibility with **LXD** and other Canonical utilities.

First yous should install **snap** if it doesn't already exist on your system:

```bash
sudo apt update && apt install snapd
```

Next install **LXD**:

```bash
sudo snap install lxd
sudo adduser $USER lxd
newgrp lxd
lxd init --auto
```

Install the **charmcraft** utility to build, package and upload our charm.

```bash
sudo snap install charmcraft --classic
```

Now you have all the tools you need to start developing the charm.
Next you should pull the code down from github using your preferred method, for example:

```bash
git clone https://github.com/catalogicsoftware/cloudcasa-charm.git
```

Now you are ready to build the charm! Go to the cloudcasa-charm directory and use **charmcraft** to build it.

```bash
cd /<path-to-project>/cloudcasa-charm
charmcraft pack
```

You will now have the **charm** inside the project directory, with a file name such as cloudcasa_ubuntu-20.04-amd64.charm, ready to be deployed with **juju**.
Obtain a cluster ID from CloudCasa and use the following commands.

```bash
juju add-model cloudcasa-system
juju deploy --trust ./<charm-file-name>.charm
juju config cloudcasa clusterid=<Registered CloudCasa Cluster Id>
```

You can examine the debug log using the ```juju debug-log``` command.

Happy coding!
