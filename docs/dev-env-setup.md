# Development Environment Setup

You will need a development environment to build and package the CloudCasa charm, and a test environment to try it out.
It is usually easiest to create both is a single VM.
We suggest creating a VM running Ubuntu 22.04 with the latest updates where you can install the necessary tools.
You will need your favorite editor, git, Python 3 and tox for development, charmcraft and LXD for building/packaging, and juju and Kubernetes for testing.

We typically create an x86 VM with 8GB of RAM, 4 vCPUs, and 160 GB of disk for development, but a smaller configuration will likely work as well.
You should log in as a non-root user with sudo capabilities when executing the commands below. Replace <user> with the non-root user you are logged in as.

First, make sure git, Python, pip, and tox are installed.

```bash
sudo apt install git python3 python3-pip
sudo python3 -m pip install tox
```

Charmcraft relies on LXD, so configure LXD before installing.
You'll also need to add your user to the lxd group.

```bash
sudo lxd init --auto
sudo usermod -a -G lxd <user>
```

Than install Charmcraft.

```bash
sudo snap install charmcraft --classic
```

Now clone the CloudCasa charm repo from Github using your preferred method and build the charm.

```bash
git clone https://github.com/catalogicsoftware/cloudcasa-charm.git
cd cloudcasa-charm
charmcraft pack
```

Assuming everything worked, you should now have the charm in the project directory,
with a file name such as cloudcasa_ubuntu-20.04-amd64.charm, ready to be deployed with **juju**.

## Test Environment Setup

For testing, the charm needs to be run under Kubernetes.
For this we will use Microk8s here, but you could use an alternate Kubernetes distribution such as Minikube instead.

Install Microk8s using snap. You must use a strictly confined version.

```bash
sudo snap install microk8s --channel 1.25-strict/stable
```

Add your user to the MicroK8s group.

```bash
sudo usermod -a -G snap_microk8s <user>
```

Enable the necessary MicroK8s addons for juju.

```bash
sudo microk8s enable hostpath-storage dns
```

Set up an alias for the Kubernetes CLI.

```bash
sudo snap alias microk8s.kubectl kubectl
```

Create a kubectl config file for juju to reference.

```bash
microk8s config > ~/.kube/config
```

Install juju. Since the juju package is strictly confined, you also need to manually create a path.

```bash
sudo snap install juju --channel 3.1/stable
mkdir -p ~/.local/share/juju
```

Install a juju controller into your microk8s cloud. 

```bash
juju bootstrap microk8s cloudcasa-controller
```

Now you are ready to install the CloudCasa charm. You will need a cluster ID to configure it,
which you can obtain from CloudCasa when registering the cluster (or later from the Cluster dashboard).

```bash
juju add-model cloudcasa-system
juju deploy --trust ./cloudcasa_ubuntu-20.04-amd64.charm --resource cloudcasa-image=catalogicsoftware/amds-kagent:latest 
juju config cloudcasa clusterid=<Registered CloudCasa Cluster ID>
```

You can examine the debug log using the ```juju debug-log``` command.
See the [test environment docs](https://github.com/catalogicsoftware/cloudcasa-charm/blob/master/docs/test-env-setup.md)
for more details.

Happy coding!

