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
from tempest.lib.common.utils import data_utils
from tempest.lib.common.utils import test_utils
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.compute import rbac_base

from tempest import config

CONF = config.CONF

if CONF.policy_feature_enabled.changed_nova_policies_victoria:
    _VOLUME_LIST = "os_compute_api:os-volumes:list"
    _VOLUME_CREATE = "os_compute_api:os-volumes:create"
    _VOLUME_SHOW = "os_compute_api:os-volumes:show"
    _VOLUME_DELETE = "os_compute_api:os-volumes:delete"
    _SNAPSHOT_LIST = "os_compute_api:os-volumes:snapshots:list"
    _SNAPSHOT_CREATE = "os_compute_api:os-volumes:snapshots:create"
    _SNAPSHOT_SHOW = "os_compute_api:os-volumes:snapshots:show"
    _SNAPSHOT_DELETE = "os_compute_api:os-volumes:snapshots:delete"
else:
    _VOLUME_LIST = "os_compute_api:os-volumes"
    _VOLUME_CREATE = "os_compute_api:os-volumes"
    _VOLUME_SHOW = "os_compute_api:os-volumes"
    _VOLUME_DELETE = "os_compute_api:os-volumes"
    _SNAPSHOT_LIST = "os_compute_api:os-volumes"
    _SNAPSHOT_CREATE = "os_compute_api:os-volumes"
    _SNAPSHOT_SHOW = "os_compute_api:os-volumes"
    _SNAPSHOT_DELETE = "os_compute_api:os-volumes"


class VolumeRbacTest(rbac_base.BaseV2ComputeRbacTest):
    """RBAC tests for the Nova Volume client."""

    # These tests will fail with a 404 starting from microversion 2.36.
    # For more information, see:
    # https://docs.openstack.org/api-ref/compute/#volume-extension-os-volumes-os-snapshots-deprecated
    max_microversion = '2.35'

    @classmethod
    def skip_checks(cls):
        super(VolumeRbacTest, cls).skip_checks()
        if not CONF.service_available.cinder:
            skip_msg = ("%s skipped as Cinder is not available" % cls.__name__)
            raise cls.skipException(skip_msg)
        if not CONF.volume_feature_enabled.snapshot:
            skip_msg = ("Cinder volume snapshots are disabled")
            raise cls.skipException(skip_msg)

    @classmethod
    def resource_setup(cls):
        super(VolumeRbacTest, cls).resource_setup()
        cls.volume = cls.create_volume()

    def _delete_snapshot(self, snapshot_id):
        waiters.wait_for_volume_resource_status(
            self.snapshots_extensions_client, snapshot_id,
            'available')
        self.snapshots_extensions_client.delete_snapshot(snapshot_id)
        self.snapshots_extensions_client.wait_for_resource_deletion(
            snapshot_id)

    @decorators.idempotent_id('2402013e-a624-43e3-9518-44a5d1dbb32d')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_VOLUME_CREATE])
    def test_create_volume(self):
        with self.override_role():
            volume = self.volumes_extensions_client.create_volume(
                size=CONF.volume.volume_size)['volume']
        waiters.wait_for_volume_resource_status(self.volumes_client,
                                                volume['id'], 'available')
        # Use non-deprecated volumes_client for deletion.
        self.addCleanup(self.volumes_client.delete_volume, volume['id'])

    @decorators.idempotent_id('69b3888c-dff2-47b0-9fa4-0672619c9054')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_VOLUME_LIST])
    def test_list_volumes(self):
        with self.override_role():
            self.volumes_extensions_client.list_volumes()

    @decorators.idempotent_id('4ba0a820-040f-488b-86bb-be2e920ea12c')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_VOLUME_SHOW])
    def test_show_volume(self):
        with self.override_role():
            self.volumes_extensions_client.show_volume(self.volume['id'])

    @decorators.idempotent_id('6e7870f2-1bb2-4b58-96f8-6782071ef327')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_VOLUME_DELETE])
    def test_delete_volume(self):
        volume = self.create_volume()
        with self.override_role():
            self.volumes_extensions_client.delete_volume(volume['id'])

    @decorators.idempotent_id('0c3eaa4f-69d6-4a13-9dda-19585f36b1c1')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_SNAPSHOT_CREATE])
    def test_create_snapshot(self):
        s_name = data_utils.rand_name(self.__class__.__name__ + '-Snapshot')
        with self.override_role():
            snapshot = self.snapshots_extensions_client.create_snapshot(
                volume_id=self.volume['id'], display_name=s_name)['snapshot']
        self.addCleanup(test_utils.call_and_ignore_notfound_exc,
                        self._delete_snapshot, snapshot['id'])

    @decorators.idempotent_id('e944e816-416c-11e7-a919-92ebcb67fe33')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_SNAPSHOT_LIST])
    def test_list_snapshots(self):
        with self.override_role():
            self.snapshots_extensions_client.list_snapshots()

    @decorators.idempotent_id('19c2e6bd-585b-472f-a8d7-71ea9299c655')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_SNAPSHOT_SHOW])
    def test_show_snapshot(self):
        s_name = data_utils.rand_name(self.__class__.__name__ + '-Snapshot')
        snapshot = self.snapshots_extensions_client.create_snapshot(
            volume_id=self.volume['id'], display_name=s_name)['snapshot']
        self.addCleanup(self._delete_snapshot, snapshot['id'])

        with self.override_role():
            self.snapshots_extensions_client.show_snapshot(snapshot['id'])

    @decorators.idempotent_id('f4f5635c-416c-11e7-a919-92ebcb67fe33')
    @rbac_rule_validation.action(
        service="nova",
        rules=[_SNAPSHOT_DELETE])
    def test_delete_snapshot(self):
        s_name = data_utils.rand_name(self.__class__.__name__ + '-Snapshot')
        snapshot = self.snapshots_extensions_client.create_snapshot(
            volume_id=self.volume['id'], display_name=s_name)['snapshot']
        self.addCleanup(test_utils.call_and_ignore_notfound_exc,
                        self._delete_snapshot, snapshot['id'])
        waiters.wait_for_volume_resource_status(
            self.snapshots_extensions_client, snapshot['id'],
            'available')

        with self.override_role():
            self.snapshots_extensions_client.delete_snapshot(snapshot['id'])
        self.snapshots_extensions_client.wait_for_resource_deletion(
            snapshot['id'])
