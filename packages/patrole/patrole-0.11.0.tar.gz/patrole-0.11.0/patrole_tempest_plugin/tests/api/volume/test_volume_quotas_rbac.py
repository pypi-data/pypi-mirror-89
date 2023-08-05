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

from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.volume import rbac_base

QUOTA_KEYS = ['gigabytes', 'snapshots', 'volumes', 'backups',
              'backup_gigabytes', 'per_volume_gigabytes']


class VolumeQuotasV3RbacTest(rbac_base.BaseVolumeRbacTest):

    @classmethod
    def setup_credentials(cls):
        super(VolumeQuotasV3RbacTest, cls).setup_credentials()
        cls.demo_tenant_id = cls.os_primary.credentials.tenant_id

    @classmethod
    def setup_clients(cls):
        super(VolumeQuotasV3RbacTest, cls).setup_clients()
        cls.quotas_client = cls.os_primary.volume_quotas_client_latest

    def _restore_default_quota_set(self):
        default_quota_set = self.quotas_client.show_default_quota_set(
            self.demo_tenant_id)['quota_set']
        cleanup_quota_set = dict(
            (k, v) for k, v in default_quota_set.items()
            if k in QUOTA_KEYS)
        self.addCleanup(self.quotas_client.update_quota_set,
                        self.demo_tenant_id, **cleanup_quota_set)

    @decorators.idempotent_id('427c9f0c-982e-403d-ae45-c05f4d6322ff')
    @rbac_rule_validation.action(service="cinder",
                                 rules=["volume_extension:quotas:show"])
    def test_list_quotas(self):
        with self.override_role():
            self.quotas_client.show_quota_set(self.demo_tenant_id)

    @decorators.idempotent_id('e47cf444-2753-4983-be6d-fc0d6523720f')
    @rbac_rule_validation.action(service="cinder",
                                 rules=["volume_extension:quotas:show"])
    def test_list_quotas_usage_true(self):
        with self.override_role():
            self.quotas_client.show_quota_set(self.demo_tenant_id,
                                              params={'usage': True})

    @rbac_rule_validation.action(service="cinder",
                                 rules=["volume_extension:quotas:show"])
    @decorators.idempotent_id('b3c7177e-b6b1-4d0f-810a-fc95606964dd')
    def test_list_default_quotas(self):
        with self.override_role():
            self.quotas_client.show_default_quota_set(
                self.demo_tenant_id)

    @rbac_rule_validation.action(service="cinder",
                                 rules=["volume_extension:quotas:update"])
    @decorators.idempotent_id('60f8f421-1630-4953-b449-b22af32265c7')
    def test_update_quota_set(self):
        self._restore_default_quota_set()
        new_quota_set = {'gigabytes': 1009,
                         'volumes': 11,
                         'snapshots': 11}
        # Update limits for all quota resources.
        with self.override_role():
            self.quotas_client.update_quota_set(
                self.demo_tenant_id, **new_quota_set)

    @decorators.idempotent_id('329bdb88-5132-4810-b1fc-350d181577e3')
    @rbac_rule_validation.action(service="cinder",
                                 rules=["volume_extension:quotas:delete"])
    def test_delete_quota_set(self):
        self._restore_default_quota_set()

        with self.override_role():
            self.quotas_client.delete_quota_set(self.demo_tenant_id)
