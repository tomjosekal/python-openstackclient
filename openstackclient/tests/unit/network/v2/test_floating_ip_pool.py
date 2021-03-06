#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from osc_lib import exceptions

from openstackclient.network.v2 import floating_ip_pool
from openstackclient.tests.unit.compute.v2 import fakes as compute_fakes
from openstackclient.tests.unit.network.v2 import fakes as network_fakes


# Tests for Network API v2
#
class TestFloatingIPPoolNetwork(network_fakes.TestNetworkV2):

    def setUp(self):
        super(TestFloatingIPPoolNetwork, self).setUp()

        # Get a shortcut to the network client
        self.network = self.app.client_manager.network


class TestListFloatingIPPoolNetwork(TestFloatingIPPoolNetwork):

    def setUp(self):
        super(TestListFloatingIPPoolNetwork, self).setUp()

        # Get the command object to test
        self.cmd = floating_ip_pool.ListFloatingIPPool(self.app,
                                                       self.namespace)

    def test_floating_ip_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)


# Tests for Compute network
#
class TestFloatingIPPoolCompute(compute_fakes.TestComputev2):

    def setUp(self):
        super(TestFloatingIPPoolCompute, self).setUp()

        # Get a shortcut to the compute client
        self.compute = self.app.client_manager.compute


class TestListFloatingIPPoolCompute(TestFloatingIPPoolCompute):

    # The floating ip pools to list up
    floating_ip_pools = \
        compute_fakes.FakeFloatingIPPool.create_floating_ip_pools(count=3)

    columns = (
        'Name',
    )

    data = []
    for pool in floating_ip_pools:
        data.append((
            pool.name,
        ))

    def setUp(self):
        super(TestListFloatingIPPoolCompute, self).setUp()

        self.app.client_manager.network_endpoint_enabled = False

        self.compute.floating_ip_pools.list.return_value = \
            self.floating_ip_pools

        # Get the command object to test
        self.cmd = floating_ip_pool.ListFloatingIPPool(self.app, None)

    def test_floating_ip_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.compute.floating_ip_pools.list.assert_called_once_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
