# CloudCasa

## Description

**CloudCasa** is a powerful and easy-to-use backup service for protecting Kubernetes, cloud databases, and cloud native applications. As a SaaS solution, CloudCasa eliminates the complexity of managing traditional backup infrastructure, while providing the same level of applications-consistent data protection and disaster recovery capabilities that more traditional backup solutions provide for server-based applications. CloudCasa’s rich feature set simplifies disaster recovery and data migration. Its compatibility with Velero allows users to manage their existing Velero installations centrally, at scale, without having to modify their existing configuration. Finally, CloudCasa helps you take cyber resilience to the next level by providing vulnerability scanning alongside traditional data protection services.

A free service plan is available that allows users to protect Kubernetes clusters with up to 10 worker nodes.

This repository contains a Charmed Operator which deploys the **CloudCasa** agent in a Kubernetes cluster.

## Requirements
1. CloudCasa requires Kubernetes 1.17 or higher. 
2. This CloudCasa charm requires juju 2.8.0 or newer.

## CloudCasa Sign Up

1. Sign up for the free service at https://cloudcasa.io/kubernetes-backup 
2. Register your Charmed Kubernetes cluster.
3. Record the cluster ID and keep it for future use.

## Installation steps

1. Create a dedicated model in juju
    ```bash
    juju add-model cloudcasa-system
    ```
2. Deploy and configure the CloudCasa charm
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

See the official CloudCasa documentation here: [docs.cloudcasa.io](https://docs.cloudcasa.io/help)
