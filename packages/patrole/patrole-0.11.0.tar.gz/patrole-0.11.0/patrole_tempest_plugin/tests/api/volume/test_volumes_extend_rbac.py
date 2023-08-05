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

from tempest.common import waiters
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.volume import rbac_base


class VolumesExtendV3RbacTest(rbac_base.BaseVolumeRbacTest):

    @classmethod
    def resource_setup(cls):
        super(VolumesExtendV3RbacTest, cls).resource_setup()
        # Create a test shared volume for tests
        cls.volume = cls.create_volume()

    @rbac_rule_validation.action(service="cinder", rules=["volume:extend"])
    @decorators.idempotent_id('1627b065-4081-4e14-8340-8e4fb02ceaf2')
    def test_volume_extend(self):
        # Extend volume test
        extend_size = int(self.volume['size']) + 1
        with self.override_role():
            self.volumes_client.extend_volume(self.volume['id'],
                                              new_size=extend_size)
        waiters.wait_for_volume_resource_status(
            self.volumes_client, self.volume['id'], 'available')
