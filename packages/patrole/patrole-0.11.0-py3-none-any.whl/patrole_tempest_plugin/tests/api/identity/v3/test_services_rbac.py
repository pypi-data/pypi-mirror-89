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


class IdentitySericesV3RbacTest(rbac_base.BaseIdentityV3RbacTest):

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:create_service"])
    @decorators.idempotent_id('9a4bb317-f0bb-4005-8df0-4b672885b7c8')
    def test_create_service(self):
        with self.override_role():
            self.setup_test_service()

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:update_service"])
    @decorators.idempotent_id('b39447d1-2cf6-40e5-a899-46f287f2ecf0')
    def test_update_service(self):
        service = self.setup_test_service()
        new_name = data_utils.rand_name(self.__class__.__name__ + '-service')

        with self.override_role():
            self.services_client.update_service(service['id'],
                                                service=service,
                                                name=new_name,
                                                type=service['type'])

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:delete_service"])
    @decorators.idempotent_id('177b991a-438d-4bef-8e9f-9c6cc5a1c9e8')
    def test_delete_service(self):
        service = self.setup_test_service()

        with self.override_role():
            self.services_client.delete_service(service['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:get_service"])
    @decorators.idempotent_id('d89a9ac6-cd53-428d-84c0-5bc71f4a432d')
    def test_show_service(self):
        service = self.setup_test_service()

        with self.override_role():
            self.services_client.show_service(service['id'])

    @rbac_rule_validation.action(service="keystone",
                                 rules=["identity:list_services"])
    @decorators.idempotent_id('706e6bea-3385-4718-919c-0b5121395806')
    def test_list_services(self):
        with self.override_role():
            self.services_client.list_services()
