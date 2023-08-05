# Copyright 2017 AT&T Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.common import utils
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.network import rbac_base as base


class SubnetsRbacTest(base.BaseNetworkRbacTest):

    @classmethod
    def skip_checks(cls):
        super(SubnetsRbacTest, cls).skip_checks()
        if not utils.is_extension_enabled('subnet_allocation', 'network'):
            msg = "subnet_allocation extension not enabled."
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        super(SubnetsRbacTest, cls).resource_setup()
        cls.network = cls.create_network()
        cls.subnet = cls.create_subnet(cls.network)

    @decorators.idempotent_id('0481adeb-4301-44d5-851c-35910cc18a6b')
    @rbac_rule_validation.action(service="neutron",
                                 rules=["create_subnet"])
    def test_create_subnet(self):
        """Create subnet.

        RBAC test for the neutron "create_subnet" policy
        """
        with self.override_role():
            self.create_subnet(self.network)

    @decorators.idempotent_id('c02618e7-bb20-4abd-83c8-6eec2af08752')
    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_subnet"],
                                 expected_error_codes=[404])
    def test_show_subnet(self):
        """Show subnet.

        RBAC test for the neutron "get_subnet" policy
        """
        with self.override_role():
            self.subnets_client.show_subnet(self.subnet['id'])

    @decorators.idempotent_id('e2ddc415-5cab-43f4-9b61-166aed65d637')
    @rbac_rule_validation.action(service="neutron", rules=["get_subnet"])
    def test_list_subnets(self):
        """List subnets.

        RBAC test for the neutron ``list_subnets`` function and
        the ``get_subnet`` policy
        """
        admin_resource_id = self.subnet['id']
        with (self.override_role_and_validate_list(
                admin_resource_id=admin_resource_id)) as ctx:
            ctx.resources = self.subnets_client.list_subnets(
                id=admin_resource_id)["subnets"]

    @decorators.idempotent_id('f36cd821-dd22-4bd0-b43d-110fc4b553eb')
    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_subnet", "update_subnet"],
                                 expected_error_codes=[404, 403])
    def test_update_subnet(self):
        """Update subnet.

        RBAC test for the neutron "update_subnet" policy
        """
        update_name = data_utils.rand_name(self.__class__.__name__ + '-Subnet')

        with self.override_role():
            self.subnets_client.update_subnet(self.subnet['id'],
                                              name=update_name)

    @decorators.idempotent_id('bcfc7153-bbd1-43a4-a908-b3e1b0cde0dc')
    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_subnet", "delete_subnet"],
                                 expected_error_codes=[404, 403])
    def test_delete_subnet(self):
        """Delete subnet.

        RBAC test for the neutron "delete_subnet" policy
        """
        subnet = self.create_subnet(self.network)

        with self.override_role():
            self.subnets_client.delete_subnet(subnet['id'])
