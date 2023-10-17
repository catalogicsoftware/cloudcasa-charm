#!/usr/bin/env python3
# Copyright 2022 catalogicsoftware

import logging
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus
import traceback
from lightkube import Client, codecs
from lightkube.resources.core_v1 import Pod, Namespace, ServiceAccount
from lightkube.core.exceptions import ApiError
#from lightkube.models.meta_v1 import ObjectMeta
from lightkube.resources.apps_v1 import Deployment
from lightkube.resources.rbac_authorization_v1 import ClusterRoleBinding
from ops.charm import CharmBase, WorkloadEvent

logger = logging.getLogger(__name__)
TEMPLATE_DIR = "src/templates/"

class CloudcasaCharm(CharmBase):
    
    """Charm the service."""
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.cloudcasa_pebble_ready, self._on_cloudcasa_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.stop, self._on_stop)

    def _on_cloudcasa_pebble_ready(self, event: WorkloadEvent):
        """Define and start a workload using the Pebble API."""
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        # Define an initial Pebble layer configuration
        pebble_layer = {
            "summary": "cloudcasa layer",
            "description": "pebble config layer for cloudcasa",
            "services": {
                "cloudcasa": {
                    "override": "replace",
                    "summary": "cloudcasa",
                    "command": "ls",
                    "startup": "enabled",
                    "environment": {
                        "clusterid": self.config["clusterid"]
                    },
                }
            },
        }
        # Add initial Pebble config layer using the Pebble API
        container.add_layer("cloudcasa", pebble_layer, combine=True)

    def _on_config_changed(self, event):
        client = Client()
        cloudcasa_pod = client.get(Pod, name="cloudcasa-0", namespace="cloudcasa-system")
        for con in cloudcasa_pod.spec.containers:
            if con.name == "cloudcasa":
                kagentimage = con.image
        clusterid = self.config["clusterid"]
        patch = {"spec": {"template": {"spec": {"containers": [{"image": kagentimage, "args": ["/usr/local/bin/kubeagentmanager", "--server_addr", "agent.cloudcasa.io:443", "--tls", "true"], "imagePullPolicy": "Always", "name": "kubeagentmanager", "resources": {"requests": {"memory": "64Mi", "cpu": "250m"}, "limits": {"memory": "128Mi", "cpu": "500m"}}, "volumeMounts": [{"mountPath": "/scratch", "name": "scratch"}], "env": [{"name": "MY_POD_NAME", "valueFrom": {"fieldRef": {"fieldPath": "metadata.name"}}}, {"name": "AMDS_CLUSTER_ID", "value": clusterid}, {"name": "KUBEMOVER_IMAGE", "value": kagentimage}, {"name": "DEPLOYMENT_PLATFORM", "value": "charmed"}]}], "restartPolicy": "Always", "serviceAccountName": "cloudcasa-io", "volumes": [{"emptyDir": {}, "name": "scratch"}]}}}}
        try:
            client.patch(Deployment, name='cloudcasa-kubeagent-manager', namespace='cloudcasa-io', obj=patch)
            logging.info("cluster id patched with kubeagent")
        except Exception:
            pass
        self.unit.status = ActiveStatus()

    def _on_stop(self, event):
        client = Client()
        try:
            client.delete(ClusterRoleBinding, name="cloudcasa-io")
        except Exception:
            pass
        try:
            client.delete(Namespace, name="cloudcasa-io")
        except Exception:
            pass         

        self.unit.status = ActiveStatus()       
        
    def _create_kubernetes_resources(self):
        client = Client()
        path = TEMPLATE_DIR + "cluster-register.yaml"

        with open(path, encoding="utf-8") as f:
            logging.info("Collecting all resource manifests")

            try:
                cloudcasa_deployment = client.get(Deployment, name="cloudcasa-kubeagent-manager", namespace="cloudcasa-io")
            except FileNotFoundError:
                pass
            except Exception:
                cloudcasa_deployment = None
                logger.info("Issue seen in fetching Deployment information")

            try:
                cloudcasa_namespace = client.get(Namespace, name="cloudcasa-io")
            except FileNotFoundError:
                pass
            except Exception:
                cloudcasa_namespace = None
                logger.info("Issue seen in fetching Namespace information")

            try:
                cloudcasa_sa = client.get(ServiceAccount, name="cloudcasa-io", namespace="cloudcasa-io")
            except FileNotFoundError:
                pass
            except Exception:
                cloudcasa_sa = None
                logger.info("Issue seen in fetching ServiceAccount information")  

            try:
                cloudcasa_crb = client.get(ClusterRoleBinding, name="cloudcasa-io")
            except FileNotFoundError:
                pass
            except Exception:
                cloudcasa_crb = None
                logger.info("Issue seen in fetching ClusterRoleBinding information")

            for obj in codecs.load_all_yaml(f):
                if obj.kind == "Namespace":     
                    if not cloudcasa_namespace:
                        logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
                        client.create(obj)
                    else:
                        logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

                if obj.kind == "ServiceAccount":     
                    if not cloudcasa_sa:
                        logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
                        client.create(obj)
                    else:
                        logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

                if obj.kind == "ClusterRoleBinding": 
                    if not cloudcasa_crb:
                        logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
                        client.create(obj)
                    else:
                        logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

                if obj.kind == "Deployment":     
                    if not cloudcasa_deployment:
                        logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
                        client.create(obj)
                    else:
                        logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

    def _on_install(self, event) -> None:
        try:
            logger.info("Create kubernetes resources.")
            self._create_kubernetes_resources()
            logging.info("All required cloudcasa resources created successfully")
            self.unit.status = ActiveStatus()
        except ApiError:
            logger.error(traceback.format_exc())
            self.unit.status = BlockedStatus("Creation failed.")

if __name__ == "__main__":
    main(CloudcasaCharm)
