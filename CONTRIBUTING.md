# cloudcasa

## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Code overview

Once deployed, Cloudcasa-charm initializes CloudcasaCharm class object
CloudcasaCharm is extended from ops.charm.CharmBase class, which provides 
framework to register the event with their eventhandlers. 
Events and their respective eventhandlers registered with CloudcasaCharm are following:
- install, _on_install
- cloudcasa_pebble_ready, _on_cloudcasa_pebble_ready
- config_changed, _on_config_changed
- stop, _on_stop

Cloudcasa-charm mainly uses lightkube python package for invoking the 
kubernetes client apis and request the charmed kubernetes cluster for 
creating following resources:
- cloudcasa_deployment
- cloudcasa_namespace
- cloudcasa_sa ( i.e. cloudcasa service account )
- cloudcasa_crb ( i.e. cloudcasa cluster role binding )

There are two main components of cloudcasa_deployment:
- cloudcasa-kubeagent-manager
- kubeagent
  kubeagent is responsible to take the snapshot of your local kubernetes cluster,
while cloudcasa-kubeagent-manager is responsible for communicating kubeagent server
of SAAS version of cloudcasa.

## Intended use case

Now a days organizations are using kubernates clusters extensivly. Cloudcasa
provides backup and restore functionality for managed and on-premise kubernetes 
cluster. Cloudcasa-charm provides the same functionality for charmed kubernetes 
cluster.

## Roadmap

If this Charm doesn't fulfill all of the initial functionality you were
hoping for or planning on, please add a Roadmap or TODO here

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
