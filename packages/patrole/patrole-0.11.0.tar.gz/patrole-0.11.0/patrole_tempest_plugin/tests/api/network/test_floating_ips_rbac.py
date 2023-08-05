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

import netaddr

from tempest import config
from tempest.lib.common.utils import test_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.network import rbac_base as base

CONF = config.CONF


class FloatingIpsRbacTest(base.BaseNetworkRbacTest):

    @classmethod
    def resource_setup(cls):
        super(FloatingIpsRbacTest, cls).resource_setup()
        # Create an external network for floating ip creation.
        cls.fip_extnet = cls.create_network(**{'router:external': True})
        # Update router:external attribute to False for proper subnet resource
        # cleanup by base class.
        cls.fip_extnet_id = cls.fip_extnet['id']
        cls.addClassResourceCleanup(
            test_utils.call_and_ignore_notfound_exc,
            cls.networks_client.update_network, cls.fip_extnet_id,
            **{'router:external': False})

        # Create a subnet for the external network
        cls.cidr = netaddr.IPNetwork(CONF.network.project_network_cidr)
        cls.create_subnet(cls.fip_extnet,
                          cidr=cls.cidr,
                          mask_bits=24)

    def _create_floatingip(self, floating_ip_address=None):
        if floating_ip_address is not None:
            body = self.floating_ips_client.create_floatingip(
                floating_network_id=self.fip_extnet_id,
                floating_ip_address=floating_ip_address)
        else:
            body = self.floating_ips_client.create_floatingip(
                floating_network_id=self.fip_extnet_id)

        floating_ip = body['floatingip']
        self.addCleanup(test_utils.call_and_ignore_notfound_exc,
                        self.floating_ips_client.delete_floatingip,
                        floating_ip['id'])

        return floating_ip

    @rbac_rule_validation.action(service="neutron",
                                 rules=["create_floatingip"])
    @decorators.idempotent_id('f8f7474c-b8a5-4174-af84-73097d6ced38')
    def test_create_floating_ip(self):
        """Create floating IP.

        RBAC test for the neutron create_floatingip policy
        """
        with self.override_role():
            self._create_floatingip()

    @rbac_rule_validation.action(
        service="neutron",
        rules=["create_floatingip",
               "create_floatingip:floating_ip_address"])
    @decorators.idempotent_id('a8bb826a-403d-4130-a55d-120a0a660806')
    def test_create_floating_ip_floatingip_address(self):
        """Create floating IP with address.

        RBAC test for the neutron create_floatingip:floating_ip_address policy
        """
        fip = str(netaddr.IPAddress(self.cidr) + 10)

        with self.override_role():
            self._create_floatingip(floating_ip_address=fip)

    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_floatingip", "update_floatingip"],
                                 expected_error_codes=[404, 403])
    @decorators.idempotent_id('2ab1b060-19f8-4ef6-a838-e2ab7b377c63')
    def test_update_floating_ip(self):
        """Update floating IP.

        RBAC test for the neutron update_floatingip policy
        """
        floating_ip = self._create_floatingip()
        with self.override_role():
            # Associate floating IP to the other port
            self.floating_ips_client.update_floatingip(
                floating_ip['id'], port_id=None)

    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_floatingip"],
                                 expected_error_codes=[404])
    @decorators.idempotent_id('f8846fd0-c976-48fe-a148-105303931b32')
    def test_show_floating_ip(self):
        """Show floating IP.

        RBAC test for the neutron get_floatingip policy
        """
        floating_ip = self._create_floatingip()
        with self.override_role():
            # Show floating IP
            self.floating_ips_client.show_floatingip(floating_ip['id'])

    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_floatingip", "delete_floatingip"],
                                 expected_error_codes=[404, 403])
    @decorators.idempotent_id('2611b068-30d4-4241-a78f-1b801a14db7e')
    def test_delete_floating_ip(self):
        """Delete floating IP.

        RBAC test for the neutron delete_floatingip policy
        """
        floating_ip = self._create_floatingip()
        with self.override_role():
            # Delete the floating IP
            self.floating_ips_client.delete_floatingip(floating_ip['id'])

    @rbac_rule_validation.action(service="neutron", rules=["get_floatingip"])
    @decorators.idempotent_id('824965e3-8be8-46e2-be64-0d793533ad20')
    def test_list_floating_ips(self):
        """List Floating IPs.

        RBAC test for the neutron ``list_floatingips`` function and
        the ``get_floatingip`` policy
        """
        admin_resource_id = self._create_floatingip()['id']
        with (self.override_role_and_validate_list(
                admin_resource_id=admin_resource_id)) as ctx:
            ctx.resources = self.floating_ips_client.list_floatingips(
                id=admin_resource_id)["floatingips"]
