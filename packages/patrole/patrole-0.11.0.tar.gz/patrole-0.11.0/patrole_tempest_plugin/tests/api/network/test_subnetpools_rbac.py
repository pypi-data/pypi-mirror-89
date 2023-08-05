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
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib.common.utils import test_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.network import rbac_base as base

CONF = config.CONF


class SubnetPoolsRbacTest(base.BaseNetworkRbacTest):

    @classmethod
    def skip_checks(cls):
        super(SubnetPoolsRbacTest, cls).skip_checks()
        if not utils.is_extension_enabled('subnet_allocation', 'network'):
            msg = "subnet_allocation extension not enabled."
            raise cls.skipException(msg)

    def _create_subnetpool(self, **kwargs):
        post_body = {'name': data_utils.rand_name(self.__class__.__name__),
                     'min_prefixlen': 24,
                     'max_prefixlen': 32,
                     'prefixes': [CONF.network.project_network_cidr]}

        if kwargs:
            post_body.update(kwargs)

        body = self.subnetpools_client.create_subnetpool(**post_body)
        subnetpool = body['subnetpool']

        self.addCleanup(test_utils.call_and_ignore_notfound_exc,
                        self.subnetpools_client.delete_subnetpool,
                        subnetpool['id'])

        return subnetpool

    @rbac_rule_validation.action(service="neutron",
                                 rules=["create_subnetpool"])
    @decorators.idempotent_id('1b5509fd-2c32-44a8-a786-1b6ca162dbd1')
    def test_create_subnetpool(self):
        """Create subnetpool.

        RBAC test for the neutron create_subnetpool policy
        """
        with self.override_role():
            self._create_subnetpool()

    @rbac_rule_validation.action(service="neutron",
                                 rules=["create_subnetpool",
                                        "create_subnetpool:is_default"],
                                 expected_error_codes=[403, 403])
    @decorators.idempotent_id('1b5509fd-2c32-44a8-a786-1b6ca162dbd2')
    def test_create_subnetpool_default(self):
        """Create default subnetpool.

        RBAC test for the neutron create_subnetpool:is_default policy
        """
        # Most likely we already have default subnetpools for ipv4 and ipv6,
        # so we temporary mark them as is_default=False, to let this test pass.
        def_pools = self.subnetpools_client.list_subnetpools(is_default=True)
        for default_pool in def_pools["subnetpools"]:
            self.subnetpools_client.update_subnetpool(default_pool["id"],
                                                      is_default=False)

            self.addCleanup(self.subnetpools_client.update_subnetpool,
                            default_pool["id"], is_default=True)

        with self.override_role():
            # It apparently only enforces the policy for is_default=True.
            # It does nothing for is_default=False
            self._create_subnetpool(is_default=True)

    @rbac_rule_validation.action(service="neutron",
                                 rules=["create_subnetpool",
                                        "create_subnetpool:shared"],
                                 expected_error_codes=[403, 403])
    @decorators.idempotent_id('cf730989-0d47-40bc-b39a-99e7de484723')
    def test_create_subnetpool_shared(self):
        """Create subnetpool shared.

        RBAC test for the neutron create_subnetpool:shared policy
        """
        with self.override_role():
            self._create_subnetpool(shared=True)

    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_subnetpool"],
                                 expected_error_codes=[404])
    @decorators.idempotent_id('4f5aee26-0507-4b6d-b44c-3128a25094d2')
    def test_show_subnetpool(self):
        """Show subnetpool.

        RBAC test for the neutron get_subnetpool policy
        """
        subnetpool = self._create_subnetpool()
        with self.override_role():
            self.subnetpools_client.show_subnetpool(subnetpool['id'])

    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_subnetpool",
                                        "update_subnetpool"],
                                 expected_error_codes=[404, 403])
    @decorators.idempotent_id('1e79cead-5081-4be2-a4f7-484c0f443b9b')
    def test_update_subnetpool(self):
        """Update subnetpool.

        RBAC test for the neutron update_subnetpool policy
        """
        subnetpool = self._create_subnetpool()
        with self.override_role():
            self.subnetpools_client.update_subnetpool(subnetpool['id'],
                                                      min_prefixlen=24)

    @decorators.idempotent_id('a16f4e5c-0675-415f-b636-00af00638693')
    @rbac_rule_validation.action(service="neutron",
                                 rules=["update_subnetpool",
                                        "update_subnetpool:is_default"])
    def test_update_subnetpool_is_default(self):
        """Update default subnetpool.

        RBAC test for the neutron update_subnetpool:is_default policy
        """
        subnetpools = self.subnetpools_client.list_subnetpools()['subnetpools']
        default_pool = list(
            filter(lambda p: p['is_default'] is True, subnetpools))
        if default_pool:
            default_pool = default_pool[0]
        else:
            default_pool = self._create_subnetpool(is_default=True)
        original_desc = default_pool['description']

        with self.override_role():
            self.subnetpools_client.update_subnetpool(
                default_pool['id'], description=original_desc, is_default=True)

    @rbac_rule_validation.action(service="neutron",
                                 rules=["get_subnetpool",
                                        "delete_subnetpool"],
                                 expected_error_codes=[404, 403])
    @decorators.idempotent_id('50f5944e-43e5-457b-ab50-fb48a73f0d3e')
    def test_delete_subnetpool(self):
        """Delete subnetpool.

        RBAC test for the neutron delete_subnetpool policy
        """
        subnetpool = self._create_subnetpool()
        with self.override_role():
            self.subnetpools_client.delete_subnetpool(subnetpool['id'])

    @rbac_rule_validation.action(service="neutron", rules=["get_subnetpool"])
    @decorators.idempotent_id('f1caf0f6-bde5-11e8-a355-529269fb1459')
    def test_list_subnetpools(self):
        """List subnetpools.

        RBAC test for the neutron ``list_subnetpools`` function and
        the ``get_subnetpool`` policy
        """
        admin_resource_id = self._create_subnetpool()['id']
        with (self.override_role_and_validate_list(
                admin_resource_id=admin_resource_id)) as ctx:
            ctx.resources = self.subnetpools_client.list_subnetpools(
                id=admin_resource_id)["subnetpools"]
