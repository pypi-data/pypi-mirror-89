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
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.volume import rbac_base


class CapabilitiesV3RbacTest(rbac_base.BaseVolumeRbacTest):

    @classmethod
    def skip_checks(cls):
        super(CapabilitiesV3RbacTest, cls).skip_checks()
        if not utils.is_extension_enabled('capabilities', 'volume'):
            msg = "%s skipped as capabilities not enabled." % cls.__name__
            raise cls.skipException(msg)

    @classmethod
    def setup_clients(cls):
        super(CapabilitiesV3RbacTest, cls).setup_clients()
        cls.capabilities_client = \
            cls.os_primary.volume_capabilities_client_latest
        cls.hosts_client = cls.os_primary.volume_hosts_client_latest

    @rbac_rule_validation.action(service="cinder",
                                 rules=["volume_extension:capabilities"])
    @decorators.idempotent_id('40928b74-2141-11e7-93ae-92361f002671')
    def test_show_back_end_capabilities(self):
        host = self.hosts_client.list_hosts()['hosts'][0]['host_name']
        with self.override_role():
            self.capabilities_client.show_backend_capabilities(host)
