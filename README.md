## CloudCasa

## Description

**CloudCasa** is a powerful and easy-to-use backup service for protecting Kubernetes, cloud databases, and cloud native applications. As a SaaS solution, CloudCasa eliminates the complexity of managing traditional backup infrastructure, while providing the same level of applications-consistent data protection and disaster recovery capabilities that more traditional backup solutions provide for server-based applications. CloudCasa’s rich feature set simplifies disaster recovery and data migration. Its compatibility with Velero allows users to manage their existing Velero installations centrally, at scale, without having to modify their existing configuration. Finally, CloudCasa helps you take cyber resilience to the next level by providing vulnerability scanning alongside traditional data protection services.

A free service plan is available that allows user to protect an unlimited number of Kubernetes clusters and worker nodes using local snapshots. Velero users can manage Velero n clusters with a combined total of up to 15 worker nodes for free.

This repository contains a Charm Operator for deploying **CloudCasa** agent in a Charmed Kubernetes cluster.

## Requirements
1. CloudCasa requires Kubernetes 1.17 or higher. 
2. This CloudCasa charm requires juju 2.8.0 and newer.

## CloudCasa Sign Up

1. Sign Up the free service - https://cloudcasa.io/kubernetes-backup 
2. Register your Charmed Kubernetes cluster
3. Fetch the cluster ID and keep it for future use.

## Installation steps

1. Create a dedicated model in juju
    ```bash
    juju scp kubernetes-control-plane/0:config ~/.kube/config
    juju add-model cloudcasa-system
    ```
2. Deploy and configuring CloudCasa charm
    ```bash
    juju deploy --trust cloudcasa
    juju config cloudcasa clusterid=<clusterid>
      ```
3. Visit www.cloudcasa.io for more information on configuring and using CloudCasa and to create a CloudCasa account.

## Troubleshooting
If there is an issue with the CloudCasa charm, it can be useful to inspect the Juju logs. To see a complete set of logs for CloudCasa: 
  ```bash
  juju debug-log --replay --include=cloudcasa
  ```

## Documentation

Read the official documentation here: [cloudcasa.io](https://cloudcasa.io)
