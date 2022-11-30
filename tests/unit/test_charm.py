#!/usr/bin/env python3
# Copyright 2022 Catalogic Software 
# See LICENSE file for licensing details.

import logging
from pathlib import Path

import lightkube
import unittest2
from unittest.mock import Mock

import yaml
from lightkube import Client, codecs
from lightkube.resources.core_v1 import Pod, Namespace, ServiceAccount
from lightkube.core.exceptions import ApiError
from lightkube.models.meta_v1 import ObjectMeta
from lightkube.resources.apps_v1 import Deployment
from lightkube.resources.rbac_authorization_v1 import ClusterRoleBinding

from charm import CloudCasaCharm
# import ops
from ops.model import ActiveStatus
from ops.testing import Harness

logger = logging.getLogger(__name__)

# METADATA = yaml.safe_load(Path("./metadata.yaml")).read_text()
# APP_NAME = METADATA["name"]
APP_NAME = "cloudcasa"
client = Client()

# class TestCharm(unittest2.TestCase):
#     def setUp(self):
#         self.harness = Harness(cloudcasa)
#         self.addCleanup(self.harness.cleanup)
#         self.harness.begin()

#     def test_config_changed(self):
#         self.assertEqual(list(self.harness.charm._stored.things), [])
#         self.harness.update_config({"thing": "foo"})
#         self.assertEqual(list(self.harness.charm._stored.things), ["foo"])

#     def test_action(self):
#         # the harness doesn't (yet!) help much with actions themselves
#         action_event = Mock(params={"fail": ""})
#         self.harness.charm._on_fortune_action(action_event)

#         self.assertTrue(action_event.set_results.called)

#     def test_action_fail(self):
#         action_event = Mock(params={"fail": "fail this"})
#         self.harness.charm._on_fortune_action(action_event)

#         self.assertEqual(action_event.fail.call_args, [("fail this",)])

#     def test_httpbin_pebble_ready(self):
#         # Simulate making the Pebble socket available
#         self.harness.set_can_connect("httpbin", True)
#         # Check the initial Pebble plan is empty
#         initial_plan = self.harness.get_container_pebble_plan("httpbin")
#         self.assertEqual(initial_plan.to_yaml(), "{}\n")
#         # Expected plan after Pebble ready with default config
#         expected_plan = {
#             "services": {
#                 "httpbin": {
#                     "override": "replace",
#                     "summary": "httpbin",
#                     "command": "gunicorn -b 0.0.0.0:80 httpbin:app -k gevent",
#                     "startup": "enabled",
#                     "environment": {"thing": "🎁"},
#                 }
#             },
#         }
#         # Get the httpbin container from the model
#         container = self.harness.model.unit.get_container("httpbin")
#         # Emit the PebbleReadyEvent carrying the httpbin container
#         self.harness.charm.on.httpbin_pebble_ready.emit(container)
#         # Get the plan now we've run PebbleReady
#         updated_plan = self.harness.get_container_pebble_plan("httpbin").to_dict()
#         # Check we've got the plan we expected
#         self.assertEqual(expected_plan, updated_plan)
#         # Check the service was started
#         service = self.harness.model.unit.get_container("httpbin").get_service("httpbin")
#         self.assertTrue(service.is_running())
#         # Ensure we set an ActiveStatus with no message
#         self.assertEqual(self.harness.model.unit.status, ActiveStatus())


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
