# Development Environment Setup

After setting up the [test environment](https://github.com/catalogicsoftware/cloudcasa-charm/blob/master/docs/test-env-setup.md#local-environment-setup) to deploy your artifacts, you need a development environment to build and package the charms.

Our suggestion is to create a separate VM with **Ubuntu 20.04** in order to have better compatibility with **LXD** and other Canonical utilities.

At first we have to download **snap**:

```bash
sudo apt update && apt install snapd
```

Let's install **LXD**:

```bash
sudo snap install lxd
sudo adduser $USER lxd
newgrp lxd
lxd init --auto
```

Install **charmcraft** utility to build, package and upload our charm.

```bash
sudo snap install charmcraft --classic
```

Now we have all we need to start developing the charm. Upload the code on the development VM and build it.

```bash
cd /path/to/charm-project
charmcraft pack
```

You will now have the **charm** inside the project directory, ready to be deployed with **juju**.
