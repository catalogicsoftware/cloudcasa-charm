# Test Environment Setup

This guide will show you how to create an environment for local installation of the CloudCasa charm for testing.

## Requirements

First of all, let's see what you need to set up the distribution:

* Ubuntu 20.04 OS image
* 8 GB RAM
* 50 GB additional HDD

### LXD setup

The test environment depends on `lxd`.

First of all, let's install `lxd` using `snap`:

```bash
sudo apt update
sudo apt install snapd
sudo snap install lxd
```

Run the `lxd` initialization script:

```bash
/snap/bin/lxd init
```

Answer the questions in this way:

* Would you like to use LXD clustering? (yes/no) [default=no]:
* Do you want to configure a new storage pool? (yes/no) [default=yes]:
* Name of the new storage pool [default=default]:
* Name of the storage backend to use (dir, lvm, zfs, btrfs, ceph, cephobject) [default=zfs]:
* Create a new ZFS pool? (yes/no) [default=yes]:
* Would you like to use an existing empty block device (e.g. a disk or partition)? (yes/no) [default=no]:
* Size in GiB of the new loop device (1GiB minimum) [default=30GiB]:
* Would you like to connect to a MAAS server? (yes/no) [default=no]:
* Would you like to create a new local network bridge? (yes/no) [default=yes]:
* What should the new bridge be called? [default=lxdbr0]:
* What IPv4 address should be used? (CIDR subnet notation, “auto” or “none”) [default=auto]:
* What IPv6 address should be used? (CIDR subnet notation, “auto” or “none”) [default=auto]: `none`
* Would you like the LXD server to be available over the network? (yes/no) [default=no]:
* Would you like stale cached images to be updated automatically? (yes/no) [default=yes]:
* Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]: `yes`

Disable IPv6
```bash
lxc network set lxdbr0 ipv6.address none
```

### Juju setup

Juju should be installed from a snap:

```bash
sudo snap install juju --classic
```

Juju comes pre-configured to work with LXD.

A cloud created by using LXD containers on the local machine is known as `localhost` to Juju.

To begin, you need to create a Juju controller for this cloud:

```bash
juju bootstrap localhost
```

If you are creating a development environment, you can jump to the development environment setup document now.

### Charm setup

All that remains is to deploy the CloudCasa charm. A simple install can be achieved with one command:

```bash
juju add-model cloudcasa-system
juju deploy --trust cloudcasa
```

Check installation progress with:

```bash
watch -c juju status --color
```

## Troubleshooting

### Kubelet fails to start with errors related to inotify_add_watch

For example, `systemctl status snap.kubelet.daemon.service` may report the following error:

```
kubelet.go:1414] "Failed to start cAdvisor" err="inotify_add_watch /sys/fs/cgroup/cpu,cpuacct: no space left on device"
```

This problem usually is related to the kernel parameters, `fs.inotify.max_user_instances` and `fs.inotify.max_user_watches`.

At first, you should increase their values on the machine that is hosting the test environment:

```bash
sysctl -w fs.inotify.max_user_instances=8192
sysctl -w fs.inotify.max_user_watches=1048576
```

Then, you can increase them also inside the worker containers:

```bash
juju config kubernetes-worker sysctl="{ fs.inotify.max_user_instances=8192 }"
juju config kubernetes-worker sysctl="{ fs.inotify.max_user_watches=1048576 }"
```

----

# Local Environment Setup

In case you don't need a production environment like the one described above, you can setup a minimal configuration locally using **kind**.

First, create your cluster with `kind`:

```bash
kind create cluster --name charmed-kubernetes
```

Then, deploy the **juju OLM** into your local cluster:

```bash
juju add-k8s --client mycluster --cluster-name=kind-charmed-kubernetes
```

Let's start the operator lifecycle manager on your cluster:

```bash
juju bootstrap mycluster
```

Now your cluster has the **juju OLM** controller installed.

From now, you can use `juju` to create **models** and **deploy** charms.

```bash
juju add-model cloudcasa-system
```

On Kubernetes, each model is put into a different namespace on the cluster. So you should see a `cloudcasa-system` namespace in your Kubernetes:

```bash
kubectl get namespaces
NAME                   STATUS   AGE
cloudcasa-system       Active   6s
controller-mycluster   Active   2m4s
default                Active   3m37s
kube-node-lease        Active   3m38s
kube-public            Active   3m38s
kube-system            Active   3m38s
local-path-storage     Active   3m33s
```
