#!/usr/bin/env python3
# Copyright 2022 Catalogic Software 
# See LICENSE file for licensing details.

import logging
from pathlib import Path

import lightkube
import pytest
from pytest_operator.plugin import OpsTest
# import unittest
# from unittest.mock import Mock

import yaml
from lightkube import Client, codecs
from lightkube.resources.core_v1 import Pod, Namespace, ServiceAccount
from lightkube.core.exceptions import ApiError
from lightkube.models.meta_v1 import ObjectMeta
from lightkube.resources.apps_v1 import Deployment
from lightkube.resources.rbac_authorization_v1 import ClusterRoleBinding
# import ops
# from ops.model import ActiveStatus
# from ops.testing import Harness

logger = logging.getLogger(__name__)

# METADATA = yaml.safe_load(Path("./metadata.yaml")).read_text()
# APP_NAME = METADATA["name"]

APP_NAME = "cloudcasa"
client = Client()

@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    """Build the charm-under-test and deploy it together with related charms."""
    charm = await ops_test.build_charm(".")
    resources = {"cloudcasa-image": METADATA["resources"]["cloudcasa-image"]["upstream-source"]}
    await ops_test.model.deploy(charm, resources=resources, application_name=APP_NAME, trust=True)

    # issuing dummy update_status just to trigger an event
    await ops_test.model.set_config({"update-status-hook-interval": "30s"})
    await ops_test.model.wait_for_idle(apps=[APP_NAME], status="active", timeout=1000)
    assert ops_test.model.applications[APP_NAME].units[0].workload_status == "active"

    # effectively disable the update status from firing
    await ops_test.model.set_config({"update-status-hook-interval": "60m"})


# @pytest.mark.abort_on_fail
# async def test_kubernetes_resources_created(ops_test: OpsTest):
#     """Test if kubernetes resources have been created properly."""
#     client = Client()

#     # If any of these fail, an exception is raised and the test will fail
#     client.get(Namespace, name="cloudcasa-io")
#     client.get(ServiceAccount, name="cloudcasa-io", namespace="cloudcasa-io")
#     # client.get(CustomResourceDefinition, name="test")
#     client.get(ClusterRoleBinding, name="cloudcasa-io")
#     client.get(Deployment, name="cloudcasa-kubeagent-manager")

# @pytest.mark.abort_on_fail
# async def test_connection_creation(ops_test: OpsTest):
#     """Test if cluster is registered properly."""

#     with open("./tests/integration/connection.yaml", encoding="utf-8") as connection_manifest:
#         connection_obj = codecs.load_all_yaml(connection_manifest)
#         logging.info("Collecting all resource manifests")
#         # wait for capsule ready
#         await ops_test.model.wait_for_idle(wait_for_active=True, idle_period=60, status="active")

#         try:
#             cloudcasa_deployment = client.get(Deployment, name="cloudcasa-kubeagent-manager", namespace="cloudcasa-io")
#         except Exception as e:
#             cloudcasa_deployment = None
#             logger.info("Issue seen in fetching Deployment information")
#         except FileNotFoundError:
#             pass

#         try:
#             cloudcasa_namespace = client.get(Namespace, name="cloudcasa-io")
#         except Exception as e:
#             cloudcasa_namespace = None
#             logger.info("Issue seen in fetching Namespace information")
#         except FileNotFoundError:
#             pass

#         try:
#             cloudcasa_sa = client.get(ServiceAccount, name="cloudcasa-io", namespace="cloudcasa-io")
#         except Exception as e:
#             cloudcasa_sa = None
#             logger.info("Issue seen in fetching ServiceAccount information")
#         except FileNotFoundError:
#             pass

#         try:
#             cloudcasa_crb = client.get(ClusterRoleBinding, name="cloudcasa-io")
#         except Exception as e:
#             cloudcasa_crb = None
#             logger.info("Issue seen in fetching ClusterRoleBinding information")
#         except FileNotFoundError:
#             pass
#         for obj in codecs.load_all_yaml(f):
#             if obj.kind == "Namespace":
#                 if not cloudcasa_namespace:
#                     logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
#                     client.create(obj)
#                 else:
#                     logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

#             if obj.kind == "ServiceAccount":
#                 if not cloudcasa_sa:
#                     logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
#                     client.create(obj)
#                 else:
#                     logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

#             if obj.kind == "ClusterRoleBinding":
#                 if not cloudcasa_crb:
#                     logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
#                     client.create(obj)
#                 else:
#                     logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)

#             if obj.kind == "Deployment":
#                 if not cloudcasa_deployment:
#                     logging.info("Creating resource %s of kind %s from manifest.", obj.metadata.name, obj.kind)
#                     client.create(obj)
#                 else:
#                     logging.info("Resource %s of kind %s already present", obj.metadata.name, obj.kind)
