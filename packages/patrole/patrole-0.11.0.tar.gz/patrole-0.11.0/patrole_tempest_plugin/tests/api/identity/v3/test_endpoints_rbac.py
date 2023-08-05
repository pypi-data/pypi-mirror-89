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

from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.identity import rbac_base


class IdentityEndpointsV3RbacTest(rbac_base.BaseIdentityV3RbacTest):

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:create_endpoint"])
    @decorators.idempotent_id('6bdaecd4-0843-4ed6-ab64-3a57ab0cd127')
    def test_create_endpoint(self):
        service = self.setup_test_service()
        with self.override_role():
            self.setup_test_endpoint(service=service)

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:update_endpoint"])
    @decorators.idempotent_id('6bdaecd4-0843-4ed6-ab64-3a57ab0cd128')
    def test_update_endpoint(self):
        endpoint = self.setup_test_endpoint()
        new_url = data_utils.rand_url()

        with self.override_role():
            self.endpoints_client.update_endpoint(
                endpoint["id"],
                url=new_url)

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:delete_endpoint"])
    @decorators.idempotent_id('6bdaecd4-0843-4ed6-ab64-3a57ab0cd129')
    def test_delete_endpoint(self):
        endpoint = self.setup_test_endpoint()

        with self.override_role():
            self.endpoints_client.delete_endpoint(endpoint['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:get_endpoint"])
    @decorators.idempotent_id('6bdaecd4-0843-4ed6-ab64-3a57ab0cd130')
    def test_show_endpoint(self):
        endpoint = self.setup_test_endpoint()

        with self.override_role():
            self.endpoints_client.show_endpoint(endpoint['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:list_endpoints"])
    @decorators.idempotent_id('6bdaecd4-0843-4ed6-ab64-3a57ab0cd131')
    def test_list_endpoints(self):
        with self.override_role():
            self.endpoints_client.list_endpoints()
