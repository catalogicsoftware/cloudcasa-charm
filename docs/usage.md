## Usage

### Install

To install the charm, run:

```bash
# Create dedicated namespace on k8s cluster
juju add-model cloudcasa-system
# Deploy capsule along with the charm operator
juju deploy --trust cloudcasa
```

### Configure

To configure the charm, run:

```bash
# Example: juju config cloudcasa key=value
juju config cloudcasa clusterid=<Registered K8S Cluster Id>
```

The configurable parameters are:

| **name**                    | **description**                                              | type    | **default**          | references                                                   |
| --------------------------- | ------------------------------------------------------------ | ------- | -------------------- | ------------------------------------------------------------ |
| `clusterid`               | Provide the value of clusterid fetched after registering the K8S cluster with CloudCasa (example: `83624dy57c8e4edcd32lk4b1`). | string  | `""` | [cloudcasa](https://cloudcasa.io) |

