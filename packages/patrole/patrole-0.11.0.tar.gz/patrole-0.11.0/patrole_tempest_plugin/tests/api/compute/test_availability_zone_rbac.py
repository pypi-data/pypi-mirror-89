# Copyright 2017 AT&T Corporation.
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
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.compute import rbac_base


class NovaAvailabilityZoneRbacTest(rbac_base.BaseV2ComputeRbacTest):

    @classmethod
    def skip_checks(cls):
        super(NovaAvailabilityZoneRbacTest, cls).skip_checks()
        if not utils.is_extension_enabled('os-availability-zone', 'compute'):
            msg = ("%s skipped as os-availability-zone not "
                   "enabled." % cls.__name__)
            raise cls.skipException(msg)

    @rbac_rule_validation.action(
        service="nova",
        rules=["os_compute_api:os-availability-zone:list"])
    @decorators.idempotent_id('cd34e7ea-d26e-4fa3-a8d0-f8883726ce3d')
    def test_get_availability_zone_list_rbac(self):
        with self.override_role():
            self.availability_zone_client.list_availability_zones()

    @rbac_rule_validation.action(
        service="nova",
        rules=["os_compute_api:os-availability-zone:detail"])
    @decorators.idempotent_id('2f61c191-6ece-4f21-b487-39d749e3d38e')
    def test_get_availability_zone_list_detail_rbac(self):
        with self.override_role():
            self.availability_zone_client.list_availability_zones(detail=True)
