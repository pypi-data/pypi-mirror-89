# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
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
from __future__ import unicode_literals

import pickle
from unittest import TestCase

import ddt
import mock
from hamcrest import assert_that, calling, only_contains, instance_of, \
    contains_string, raises, none, has_item, is_not
from hamcrest import equal_to

from storops import UnitySystem, TieringPolicyEnum
from storops.exception import UnitySnapNameInUseError, \
    UnityLunNameInUseError, UnityLunShrinkNotSupportedError, \
    UnityNothingToModifyError, UnityPerfMonNotEnabledError, \
    UnityThinCloneLimitExceededError, UnityCGMemberActionNotSupportError, \
    UnityThinCloneNotAllowedError, UnityMigrationTimeoutException, \
    UnityMigrationSourceDestNotExistsError, JobStateError, \
    JobTimeoutException, UnityAdvancedDedupRequireCompressionEnabledError, \
    UnityCompressionRequireAllFlashPoolError, \
    UnityCompressionRequireLunIsThinError
from storops.unity.enums import HostLUNAccessEnum, NodeEnum, RaidTypeEnum, \
    ESXFilesystemBlockSizeEnum, ESXFilesystemMajorVersionEnum
from storops.unity.resource.disk import UnityDisk
from storops.unity.resource.host import UnityBlockHostAccessList, UnityHost
from storops.unity.resource.lun import UnityLun, UnityLunList
from storops.unity.resource.pool import UnityPool
from storops.unity.resource.port import UnityIoLimitPolicy, \
    UnityIoLimitRuleSetting
from storops.unity.resource.remote_system import UnityRemoteSystem
from storops.unity.resource.snap import UnitySnap
from storops.unity.resource.snap_schedule import UnitySnapSchedule
from storops.unity.resource.sp import UnityStorageProcessor
from storops.unity.resource.storage_resource import UnityStorageResource
from storops.unity.resp import RestResponse
from storops_test.unity.jh_mock import MockJobHelper
from storops_test.unity.rest_mock import t_rest, t_unity, patch_rest
from storops_test.utils import is_nan

__author__ = 'Cedric Zhuang'


@ddt.ddt
class UnityLunTest(TestCase):
    @patch_rest
    def test_get_lun_sv2_simple_property(self):
        lun = UnityLun(_id='sv_2', cli=t_rest())
        assert_that(lun.existed, equal_to(True))
        assert_that(lun.id, equal_to('sv_2'))
        assert_that(lun.name, equal_to('openstack_lun'))
        assert_that(lun.description, equal_to('sample'))
        assert_that(lun.size_total, equal_to(107374182400))
        assert_that(lun.total_size_gb, equal_to(100))
        assert_that(lun.size_allocated, equal_to(0))
        assert_that(lun.per_tier_size_used, only_contains(2952790016, 0, 0))
        assert_that(lun.is_thin_enabled, equal_to(True))
        assert_that(lun.wwn, equal_to(
            '60:06:01:60:17:50:3C:00:C2:0A:D5:56:92:D1:BA:12'))
        assert_that(lun.is_replication_destination, equal_to(False))
        assert_that(lun.is_snap_schedule_paused, equal_to(False))
        assert_that(lun.metadata_size, equal_to(5100273664))
        assert_that(lun.metadata_size_allocated, equal_to(2684354560))
        assert_that(lun.snap_wwn, equal_to(
            '60:06:01:60:17:50:3C:00:C4:0A:D5:56:00:95:DE:11'))
        assert_that(lun.snaps_size, equal_to(0))
        assert_that(lun.snaps_size_allocated, equal_to(0))
        assert_that(lun.snap_count, equal_to(0))
        assert_that(lun.storage_resource, instance_of(UnityStorageResource))
        assert_that(lun.pool, instance_of(UnityPool))
        assert_that(lun.io_limit_rule, none())
        assert_that(lun.is_compression_enabled, equal_to(False))
        assert_that(lun.is_data_reduction_enabled, equal_to(False))
        assert_that(lun.is_advanced_dedup_enabled, equal_to(False))
        assert_that(lun.data_reduction_size_saved, equal_to(0))
        assert_that(lun.data_reduction_percent, equal_to(0))
        assert_that(lun.data_reduction_ratio, equal_to(1.0))

    @patch_rest
    def test_lun_modify_host_access(self):
        host = UnityHost(_id="Host_1", cli=t_rest())
        lun = UnityLun(_id='sv_4', cli=t_rest())
        host_access = [{'host': host, 'accessMask': HostLUNAccessEnum.BOTH}]
        lun.modify(host_access=host_access)
        lun.update()
        assert_that(lun.host_access[0].host, equal_to(host))
        assert_that(lun.host_access[0].access_mask,
                    equal_to(HostLUNAccessEnum.BOTH))

    @patch_rest
    def test_lun_modify_sp(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        sp = UnityStorageProcessor(_id='spb', cli=t_rest())
        lun.modify(sp=sp)
        lun.update()
        assert_that(sp.to_node_enum(), equal_to(NodeEnum.SPB))

    @patch_rest
    def test_lun_modify_sp_with_id(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.modify(sp=1)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_modify_sp_with_enum(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.modify(sp=NodeEnum.SPB)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_modify_none(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.modify(host_access=None)
        lun.update()
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_modify_wipe_host_access(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.modify(host_access=[])
        lun.update()
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_modify_muitl_property_except_sp(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        lun.modify(name="RestLun100", is_compression=True,
                   description="Lun description")
        lun.update()
        assert_that(lun.name, equal_to('RestLun100'))
        assert_that(lun.description, equal_to('Lun description'))

    @patch_rest
    def test_lun_modify_compression_enabled_v4_2(self):
        lun = UnityLun(_id='sv_17', cli=t_rest(version='4.2'))
        lun.modify(is_compression=True)
        lun.update()
        assert_that(lun.is_compression_enabled, equal_to(True))

    @patch_rest
    def test_lun_modify_compression_enabled(self):
        lun = UnityLun(_id='sv_18', cli=t_rest(version='4.3'))
        lun.modify(is_compression=True)
        lun.update()
        assert_that(lun.is_data_reduction_enabled, equal_to(True))

    @patch_rest
    def test_lun_modify_dedup_enabled(self):
        lun = UnityLun(_id='sv_19', cli=t_rest(version='5.0.0'))
        lun.modify(is_advanced_dedup_enabled=True)
        lun.update()
        assert_that(lun.is_advanced_dedup_enabled, equal_to(True))

    @mock.patch(target='storops.lib.job_helper.JobHelper',
                new=MockJobHelper)
    @patch_rest
    def test_lun_delete_async(self):
        lun = UnityLun(_id='sv_1535', cli=t_rest())
        resp = lun.delete(force_snap_delete=True, force_vvol_delete=True)
        lun.update()
        assert_that(resp.is_ok(), equal_to(True))
        assert_that(resp.job.existed, equal_to(True))
        assert_that(resp.job.state.index, equal_to(4))

    @patch_rest
    def test_lun_delete_sync(self):
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.delete(async_mode=False, force_snap_delete=True,
                          force_vvol_delete=True)
        lun.update()
        assert_that(resp.is_ok(), equal_to(True))
        assert_that(resp.job.existed, equal_to(False))

    @patch_rest
    def test_lun_delete_thinclone(self):
        lun = UnityLun(_id='sv_5604', cli=t_rest())
        resp = lun.delete(async_mode=False, force_snap_delete=True,
                          force_vvol_delete=True)
        lun.update()
        assert_that(resp.is_ok(), equal_to(True))
        assert_that(resp.job.existed, equal_to(False))

    @patch_rest
    def test_lun_delete_has_thinclone(self):
        lun = UnityLun(_id='sv_5605', cli=t_rest())
        resp = lun.delete(force_snap_delete=True, force_vvol_delete=True)
        lun.update()
        assert_that(resp.is_ok(), equal_to(True))
        assert_that(resp.job.existed, equal_to(False))

    @mock.patch(target='storops.lib.job_helper.JobHelper',
                new=MockJobHelper)
    @patch_rest
    def test_lun_delete_async_job_state_error(self):
        def f():
            lun = UnityLun(_id='sv_1536', cli=t_rest())
            lun.delete(force_snap_delete=True, force_vvol_delete=True)

        assert_that(f, raises(JobStateError))

    @mock.patch(target='storops.lib.job_helper.JobHelper',
                new=MockJobHelper)
    @patch_rest
    def test_lun_delete_async_job_timeout(self):
        def f():
            lun = UnityLun(_id='sv_1537', cli=t_rest())
            lun.delete(force_snap_delete=True, force_vvol_delete=True,
                       async_timeout=3, async_interval=1)

        assert_that(f, raises(JobTimeoutException))

    @patch_rest
    def test_lun_attach_to_new_host(self):
        host = UnityHost(_id="Host_10", cli=t_rest())
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.attach_to(host)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_attach_to_same_host(self):
        host = UnityHost(_id="Host_1", cli=t_rest())
        lun = UnityLun(_id='sv_4', cli=t_rest())
        resp = lun.attach_to(host, access_mask=HostLUNAccessEnum.BOTH)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_attach_to_with_hlu(self):
        host = UnityHost(_id="Host_1", cli=t_rest())
        lun = UnityLun(_id='sv_6', cli=t_rest(version='4.4.0'))
        resp = lun.attach_to(host, access_mask=HostLUNAccessEnum.BOTH,
                             hlu=1655)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_attach_to_without_hlu(self):
        host = UnityHost(_id="Host_1", cli=t_rest())
        lun = UnityLun(_id='sv_7', cli=t_rest(version='4.4.0'))
        resp = lun.attach_to(host, access_mask=HostLUNAccessEnum.BOTH)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_detach_from_host(self):
        host = UnityHost(_id="Host_1", cli=t_rest())
        lun = UnityLun(_id='sv_16', cli=t_rest())
        resp = lun.detach_from(host)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_lun_detach_from_all_hosts(self):
        lun = UnityLun(_id='sv_5', cli=t_rest())
        lun.is_cg_member = False
        resp = lun.detach_from(host=None)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_get_lun_sv2_nested_property_update_property(self):
        lun = UnityLun(_id='sv_2', cli=t_rest())
        sr = lun.storage_resource
        assert_that(sr._cli, equal_to(t_rest()))
        assert_that(sr.size_total, equal_to(107374182400))

    @patch_rest
    def test_get_lun_sv3_nested_property_no_update(self):
        lun = UnityLunList.get(_id='sv_3', cli=t_rest())
        sr = lun.storage_resource
        assert_that(sr._cli, equal_to(t_rest()))

    @patch_rest
    def test_get_lun_all_0(self):
        lun_list = UnityLunList.get(cli=t_rest())
        assert_that(len(lun_list), equal_to(5))

    @patch_rest
    def test_get_lun_doc(self):
        lun = UnityLun(_id='sv_2', cli=t_rest())
        doc = lun.doc
        assert_that(doc,
                    contains_string('Represents Volume, LUN, Virtual Disk.'))
        assert_that(doc, contains_string('current_node'))
        assert_that(doc, contains_string('Current SP'))

    @patch_rest
    def test_get_lun_with_host_access(self):
        unity = UnitySystem('10.109.22.101', 'admin', 'Password123!')
        lun = unity.get_lun(_id='sv_567')
        assert_that(lun.host_access, instance_of(UnityBlockHostAccessList))
        access = lun.host_access[0]
        assert_that(access.access_mask, equal_to(HostLUNAccessEnum.PRODUCTION))
        assert_that(access.host, instance_of(UnityHost))
        assert_that(access.host.id, equal_to('Host_1'))
        assert_that(lun.host_access.get_host_id(), equal_to([access.host.id]))

    @patch_rest
    def test_lun_snap_create(self):
        lun = UnityLun(_id='sv_8', cli=t_rest())
        snap = lun.create_snap(name='lun_snap_1')
        assert_that(snap, instance_of(UnitySnap))

    @patch_rest
    def test_lun_snapshots(self):
        lun = UnityLun(_id='sv_8', cli=t_rest())
        assert_that(len(lun.snapshots), equal_to(3))

    @patch_rest
    def test_lun_snap_create_existing(self):
        lun = UnityLun(_id='sv_9', cli=t_rest())
        assert_that(lambda: lun.create_snap(name='lun_snap_1'),
                    raises(UnitySnapNameInUseError))

    @patch_rest
    def test_lun_rename(self):
        def f():
            lun = UnityLun(_id='sv_2', cli=t_rest())
            lun.name = 'Europa'

        assert_that(f, raises(UnityLunNameInUseError, 'already exists'))

    @patch_rest
    def test_lun_max_iops_property(self):
        lun = UnityLun(_id='sv_10', cli=t_rest())
        assert_that(lun.max_iops, equal_to(3600))
        assert_that(lun.max_kbps, none())

    @patch_rest
    def test_lun_max_kbps_property(self):
        lun = UnityLun(_id='sv_11', cli=t_rest())
        assert_that(lun.max_iops, none())
        assert_that(lun.max_kbps, equal_to(11000))

    @patch_rest
    def test_create_with_io_limit(self):
        cli = t_rest()
        policy = UnityIoLimitPolicy('qp_4', cli=cli)
        pool = UnityPool('pool_1', cli=cli)
        lun = pool.create_lun('Himalia', io_limit_policy=policy)
        assert_that(lun.name, equal_to('Himalia'))
        assert_that(lun.io_limit_policy.get_id(), equal_to('qp_4'))
        rule = lun.io_limit_rule
        assert_that(rule, instance_of(UnityIoLimitRuleSetting))
        assert_that(rule.max_kbps_density, equal_to(1100))
        assert_that(rule.name, equal_to('Density_1100_KBPS_rule'))

    @patch_rest
    def test_create_with_dedup_enabled_compression_enabled(self):
        cli = t_rest(version='5.0.0')
        pool = UnityPool('pool_1', cli=cli)
        lun = pool.create_lun('lun_1',
                              is_compression=True,
                              is_advanced_dedup_enabled=True)
        assert_that(lun.name, equal_to('lun_1'))
        assert_that(lun.is_data_reduction_enabled, equal_to(True))
        assert_that(lun.is_advanced_dedup_enabled, equal_to(True))

    @patch_rest
    def test_create_with_dedup_enabled_compression_disabled(self):
        def f():
            cli = t_rest(version='5.0.0')
            pool = UnityPool('pool_1', cli=cli)
            pool.create_lun('lun_2',
                            is_compression=False,
                            is_advanced_dedup_enabled=True)

        assert_that(f,
                    raises(UnityAdvancedDedupRequireCompressionEnabledError))

    @patch_rest
    def test_create_with_dedup_enabled_in_non_all_flash_pool(self):
        def f():
            cli = t_rest(version='5.0.0')
            pool = UnityPool('pool_1', cli=cli)
            pool.is_all_flash = False
            pool.create_lun('lun_3',
                            is_compression=True,
                            is_advanced_dedup_enabled=True)

        assert_that(f,
                    raises(UnityCompressionRequireAllFlashPoolError))

    @patch_rest
    def test_create_with_compressed_enabled_thin_disabled(self):
        def f():
            cli = t_rest(version='5.0.0')
            pool = UnityPool('pool_1', cli=cli)
            pool.is_all_flash = False
            pool.create_lun('lun_3',
                            is_thin=False,
                            is_compression=True)

        assert_that(f,
                    raises(UnityCompressionRequireLunIsThinError))

    @patch_rest
    def test_expand_lun_success(self):
        lun = UnityLun('sv_2', cli=t_rest())
        original_size = lun.expand(101 * 1024 ** 3)
        assert_that(original_size / 1024 ** 3, equal_to(100))

    @patch_rest
    def test_expand_lun_too_small(self):
        def f():
            lun = UnityLun('sv_2', cli=t_rest())
            lun.total_size_gb = 1

        assert_that(f, raises(UnityLunShrinkNotSupportedError, 'shrink'))

    @patch_rest
    def test_expand_lun_equal_size(self):
        def f():
            lun = UnityLun('sv_2', cli=t_rest())
            lun.total_size_gb = 100

        assert_that(f, raises(UnityNothingToModifyError, 'nothing to modify'))

    @patch_rest
    def test_lun_read_iops(self):
        lun = t_unity().get_lun(_id='sv_2')
        assert_that(lun.read_iops, equal_to(1.5))

    @patch_rest
    def test_lun_write_iops(self):
        lun = t_unity().get_lun(_id='sv_2')
        assert_that(lun.write_iops, equal_to(3.0))

    @patch_rest
    def test_lun_perf_disabled_exception(self):
        unity = UnitySystem('10.244.223.61', 'a', 'a')
        unity.disable_perf_stats()

        def f():
            return unity.get_lun(_id='sv_2').read_iops

        assert_that(f, raises(UnityPerfMonNotEnabledError, 'not enabled'))

    @patch_rest
    def test_thin_clone(self):
        lun = UnityLun.get(_id='sv_2', cli=t_rest(version='4.2.0'))
        clone = lun.thin_clone(name='test_thin_clone',
                               description='This is description.',
                               io_limit_policy=None)
        assert_that(clone.id, equal_to('sv_4678'))

    @patch_rest
    def test_thin_clone_limit_exceeded(self):
        lun = UnityLun.get(_id='sv_2', cli=t_rest(version='4.2.0'))

        def _inner():
            lun.thin_clone(name='test_thin_clone_limit_exceeded',
                           description='This is description.',
                           io_limit_policy=None)

        assert_that(_inner, raises(UnityThinCloneLimitExceededError))

    @patch_rest
    def test_update_hosts(self):
        lun = UnityLun.get(cli=t_rest(), _id="sv_4")
        r = lun.update_hosts(host_names=["ubuntu-server7"])
        assert_that(r, instance_of(RestResponse))

    @patch_rest
    def test_update_hosts_no_change(self):
        lun = UnityLun.get(cli=t_rest(), _id="sv_4")
        r = lun.update_hosts(host_names=["10.244.209.90"])
        assert_that(r, none())

    @patch_rest
    def test_migrate_lun_success(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_4', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(True))

    @patch_rest
    def test_migrate_thick_lun_success(self):
        lun = UnityLun('sv_5608', cli=t_rest())
        dest_pool = UnityPool('pool_5', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(True))

    @patch_rest
    def test_migrate_compressed_lun_success(self):
        lun = UnityLun('sv_18', cli=t_rest())
        dest_pool = UnityPool('pool_5', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(True))

    @patch_rest
    def test_migrate_deduplicated_lun_success(self):
        with mock.patch.object(UnitySystem, 'model', create=True,
                               return_value='Unity 650F',
                               new_callable=mock.PropertyMock):
            lun = UnityLun('sv_5620', cli=t_rest('4.5'))
            dest_pool = UnityPool('pool_5', cli=t_rest('4.5'))
            r = lun.migrate(dest_pool)
            assert_that(r, equal_to(True))

    @patch_rest
    def test_migrate_lun_source_thin_dest_thick(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_4', cli=t_rest())
        # If dest LUN is thick (is_thin == False), is_compressed and
        # is_advanced_dedup_enabled parameters will be changed to
        # False in lun.migrate()
        r = lun.migrate(dest_pool, is_thin=False, is_compressed=True,
                        is_advanced_dedup_enabled=True)
        assert_that(r, equal_to(True))

    @patch_rest
    def test_migrate_lun_source_deduplicated_dest_thin(self):
        lun = UnityLun('sv_5621', cli=t_rest('4.5'))
        dest_pool = UnityPool('pool_5', cli=t_rest('4.5'))
        # If dest LUN is not compressed (is_compressed == False),
        # is_advanced_dedup_enabled parameter will be changed to
        # False in lun.migrate()
        r = lun.migrate(dest_pool, is_thin=True, is_compressed=False,
                        is_advanced_dedup_enabled=True)
        assert_that(r, equal_to(True))

    @patch_rest
    def test_migrate_lun_source_is_thin_clone(self):
        lun = UnityLun('sv_5606', cli=t_rest())
        dest_pool = UnityPool('pool_4', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(False))

    @patch_rest
    def test_migrate_lun_source_compressed_dest_not_supported(self):
        lun = UnityLun('sv_18', cli=t_rest())
        dest_pool = UnityPool('pool_4', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(False))

    @patch_rest
    def test_migrate_lun_source_deduplicated_dest_not_supported(self):
        lun = UnityLun('sv_5620', cli=t_rest())
        dest_pool = UnityPool('pool_5', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(False))

    @patch_rest
    def test_migrate_lun_has_thin_clone(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_6', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(False))

    @patch_rest
    def test_migrate_lun_pool_does_not_exist(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_does_not_exist', cli=t_rest())
        assert_that(calling(lun.migrate).with_args(dest_pool),
                    raises(UnityMigrationSourceDestNotExistsError))

    @patch_rest
    def test_migrate_lun_failed(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_7', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(False))

    @patch_rest
    def test_migrate_lun_cancelled(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_8', cli=t_rest())
        r = lun.migrate(dest_pool)
        assert_that(r, equal_to(False))

    @patch_rest
    def test_migrate_lun_timeout(self):
        lun = UnityLun('sv_2', cli=t_rest())
        dest_pool = UnityPool('pool_5', cli=t_rest())
        assert_that(calling(lun.migrate).with_args(dest_pool, timeout=10),
                    raises(UnityMigrationTimeoutException))

    @patch_rest
    @ddt.data(
        {'rep_name': None, 'rep_existing_snaps': None, 'remote_system': None},
        {'rep_name': 'remote-sv_2498-sv_5',
         'rep_existing_snaps': False, 'remote_system': 'RS_4'},
    )
    @ddt.unpack
    def test_replicate(self, rep_name, rep_existing_snaps, remote_system):
        if remote_system:
            remote_system = UnityRemoteSystem(_id=remote_system, cli=t_rest())
        lun = UnityLun.get(cli=t_rest(), _id='sv_2498')
        rep_session = lun.replicate(
            'sv_5', 60, replication_name=rep_name,
            replicate_existing_snaps=rep_existing_snaps,
            remote_system=remote_system
        )
        assert_that(rep_session.name, equal_to('remote-sv_2498-sv_5'))

    @patch_rest
    @ddt.data(
        {'dst_lun_name': None, 'remote_system': None, 'rep_name': None,
         'dst_size': None, 'dst_sp': None, 'is_dst_thin': None,
         'dst_tiering_policy': None, 'is_dst_compression': None},
        {'dst_lun_name': 'lun-rep-src3-liangr', 'remote_system': 'RS_4',
         'rep_name': 'remote-rep3', 'dst_size': 10737418240,
         'dst_sp': NodeEnum.SPA, 'is_dst_thin': True,
         'dst_tiering_policy': TieringPolicyEnum.AUTOTIER_HIGH,
         'is_dst_compression': False},
    )
    @ddt.unpack
    def test_replicate_with_dst_resource_provisioning(self,
                                                      dst_lun_name,
                                                      remote_system,
                                                      rep_name,
                                                      dst_size,
                                                      dst_sp,
                                                      is_dst_thin,
                                                      dst_tiering_policy,
                                                      is_dst_compression):
        lun = UnityLun.get(cli=t_rest(), _id='sv_1876')
        if remote_system:
            remote_system = UnityRemoteSystem(_id=remote_system, cli=t_rest())
        rep_session = lun.replicate_with_dst_resource_provisioning(
            60, 'pool_2', dst_lun_name=dst_lun_name,
            remote_system=remote_system, replication_name=rep_name,
            dst_size=dst_size, dst_sp=dst_sp, is_dst_thin=is_dst_thin,
            dst_tiering_policy=dst_tiering_policy,
            is_dst_compression=is_dst_compression)
        assert_that(rep_session.id, equal_to(
            '42949675780_FNM00150600267_0000_42949678642_FNM00152000052_0000'))

    @patch_rest
    def test_is_vmware_vmfs_false(self):
        vmfs = UnityLun.get(cli=t_rest(), _id='sv_4')
        assert_that(vmfs.is_vmware_vmfs, equal_to(False))

    @patch_rest
    def test_is_vmware_vmfs_true(self):
        vmfs = UnityLun.get(cli=t_rest(), _id='sv_5613')
        assert_that(vmfs.is_vmware_vmfs, equal_to(True))

    @patch_rest
    def test_modify_vmfs_name_major_version_block_size(self):
        vmfs = UnityLun.get(cli=t_rest(), _id='sv_5613')
        resp = vmfs.modify(name='vmfs_new_name', sp=1,
                           major_version=ESXFilesystemMajorVersionEnum.VMFS_6,
                           block_size=ESXFilesystemBlockSizeEnum._4MB)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_delete_vmfs(self):
        vmfs = UnityLun.get(cli=t_rest(), _id='sv_5613')
        resp = vmfs.delete(async_mode=False)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_create_with_snap_schedule(self):
        cli = t_rest()
        schedule = UnitySnapSchedule(_id='snapSch_1', cli=cli)
        pool = UnityPool('pool_1', cli=cli)
        lun = pool.create_lun('lun-with-snap-schedule', snap_schedule=schedule)
        assert_that(lun.name, equal_to('lun-with-snap-schedule'))
        assert_that(lun.snap_schedule.get_id(), equal_to('snapSch_1'))

    @patch_rest
    def test_modify_snap_schedule(self):
        cli = t_rest()
        new_schedule = UnitySnapSchedule(_id='snapSch_4', cli=cli)
        lun = UnityLun(_id='sv_16455', cli=cli)
        resp = lun.modify(snap_schedule=new_schedule)
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_remove_snap_schedule(self):
        cli = t_rest()
        lun = UnityLun(_id='sv_16455', cli=cli)
        resp = lun.remove_snap_schedule()
        assert_that(resp.is_ok(), equal_to(True))

    @patch_rest
    def test_picklable(self):
        cli = t_rest()
        lun = UnityLun(_id='sv_16455', cli=cli)
        lun.update()
        lun_new = pickle.loads(pickle.dumps(lun))
        assert_that(lun_new.name, equal_to(lun.name))


class UnityLunEnablePerfStatsTest(TestCase):
    @patch_rest
    def setUp(self):
        self.unity = UnitySystem('10.244.223.61', 'a', 'a')
        self.unity.enable_perf_stats(1, [UnityDisk])

    @patch_rest
    def tearDown(self):
        self.unity.disable_perf_stats()

    @patch_rest
    def test_lun_perf_not_enabled_exception(self):
        disk = self.unity.get_disk(_id='dae_0_1_disk_0')
        assert_that(disk.read_iops, is_nan())

        def f():
            return self.unity.get_lun(_id='sv_2').read_iops

        assert_that(f, raises(UnityPerfMonNotEnabledError, 'not enabled'))

    @patch_rest
    def test_lun_properties_perf_not_enabled(self):
        lun = self.unity.get_lun(_id='sv_2')
        assert_that(lun.property_names, is_not(has_item('read_iops')))
        disk = self.unity.get_disk(_id='dae_0_1_disk_0')
        assert_that(disk.property_names(), has_item('read_iops'))

    @patch_rest
    def test_nested_properties(self):
        lun = self.unity.get_lun(_id='sv_12')
        assert_that(lun.pool.raid_type, equal_to(RaidTypeEnum.RAID10))
        assert_that(lun.pool.is_fast_cache_enabled, equal_to(False))
        assert_that(lun.host_access[0].host.name,
                    equal_to('Virtual_Machine_12'))

    @patch_rest
    def test_create_snap_of_member_snap_not_support(self):
        lun = UnityLun(cli=t_rest(), _id='sv_58')
        assert_that(calling(lun.create_snap).with_args(name='not-support'),
                    raises(UnityCGMemberActionNotSupportError))

    @patch_rest
    def test_thinclone_of_member_snap_not_support(self):
        lun = UnityLun(cli=t_rest(version='4.3'), _id='sv_58')
        assert_that(calling(lun.thin_clone).with_args('not-support'),
                    raises(UnityCGMemberActionNotSupportError))

    @patch_rest
    def test_thinclone_of_thick_lun_not_allowed(self):
        lun = UnityLun(cli=t_rest(version='4.3'), _id='sv_59')
        assert_that(calling(lun.thin_clone).with_args('not-allowed'),
                    raises(UnityThinCloneNotAllowedError))
