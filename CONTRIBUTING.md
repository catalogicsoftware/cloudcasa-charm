# CloudCasa

## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Code overview

Once deployed, Cloudcasa-charm initializes CloudcasaCharm class object.
CloudcasaCharm is extended from ops.charm.CharmBase class, which provides the
framework to register events with their eventhandlers. 
Events and their respective eventhandlers registered by CloudcasaCharm are the following:
- install, _on_install
- cloudcasa_pebble_ready, _on_cloudcasa_pebble_ready
- config_changed, _on_config_changed
- stop, _on_stop

Cloudcasa-charm mainly uses the lightkube python package for invoking the 
Kubernetes client apis and making requests to the Charmed Kubernetes cluster for 
creating following resources:
- cloudcasa_deployment
- cloudcasa_namespace
- cloudcasa_sa ( i.e. cloudcasa service account )
- cloudcasa_crb ( i.e. cloudcasa cluster role binding )

There are two main components of cloudcasa_deployment:
- cloudcasa-kubeagent-manager
- kubeagent
  kubeagent is responsible for taking snapshots and backups of your local kubernetes cluster,
while cloudcasa-kubeagent-manager is responsible for managing kubeagent and communicating with
the CloudCasa service.

## Intended use case

CloudCasa is a powerful and easy-to-use backup service for protecting Kubernetes, cloud
databases, and cloud native applications. It relies on an agent, running on the cluster,
to perform required snapshot, backup, and restore operations. This agent can be installed,
maintained, and updated using a variety of methods.

The Cloudcasa-charm provides this functionality for a Charmed Kubernetes cluster.
When you apply the Cloudcasa-charm, it spins up a kubeagent in your Charmed 
Kubernetes cluster, and the kubeagent initiates communications with the CloudCasa
service.

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just execute `run_tests`:

    ./run_tests
