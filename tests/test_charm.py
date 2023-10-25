# Copyright 2022 Catalogic Software
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import patch
# from unittest.mock import Mock

from charm import CloudcasaCharm
# from ops.model import ActiveStatus
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.clusterid = "6qw77af945675b1327d0bc5ee"
        self.harness = Harness(CloudcasaCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_clusterid(self):
        # Test with empty clusterid.
        self.assertEqual(self.harness.charm.config["clusterid"], "")
        self.harness.disable_hooks()
        # Test with some dummy clusterid
        self.harness.update_config({"clusterid": self.clusterid})
        self.assertEqual(len(self.harness.charm.config["clusterid"]), 25)

    @patch("charm.CloudcasaCharm._create_kubernetes_resources")
    def test_on_install(self, _create_kubernetes_resources):
        # Test with not install.
        self.harness.charm._on_install("mock_event")
        _create_kubernetes_resources.assert_called_once()
