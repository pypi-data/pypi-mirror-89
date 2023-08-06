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

import logging

import bitmath

import storops.unity.resource.filesystem
from storops.lib.models import UnityModel
from storops.lib.version import version
from storops.unity.resource import UnityResource, \
    UnityAttributeResource, UnityResourceList
from storops.unity.resource.disk import UnityDiskGroup, UnityDiskList
from storops.unity.resource.lun import UnityLun

__author__ = 'Jay Xu, Peter Wang'

LOG = logging.getLogger(__name__)


class UnityPool(UnityResource):
    @classmethod
    def create(cls, cli, name, description=None, raid_groups=None,
               alert_threshold=None,
               is_harvest_enabled=None,
               is_snap_harvest_enabled=None,
               pool_harvest_high_threshold=None,
               pool_harvest_low_threshold=None,
               snap_harvest_high_threshold=None,
               snap_harvest_low_threshold=None,
               is_fast_cache_enabled=None,
               is_fastvp_enabled=None,
               pool_type=None):
        req_body = cls._compose_pool_parameter(
            cli, name=name, description=description,
            raid_groups=raid_groups, alert_threshold=alert_threshold,
            is_harvest_enabled=is_harvest_enabled,
            is_snap_harvest_enabled=is_snap_harvest_enabled,
            pool_harvest_high_threshold=pool_harvest_high_threshold,
            pool_harvest_low_threshold=pool_harvest_low_threshold,
            snap_harvest_high_threshold=snap_harvest_high_threshold,
            snap_harvest_low_threshold=snap_harvest_low_threshold,
            is_fast_cache_enabled=is_fast_cache_enabled,
            is_fastvp_enabled=is_fastvp_enabled,
            pool_type=pool_type)
        resp = cli.post(cls().resource_class, **req_body)
        resp.raise_if_err()
        pool = cls.get(cli, resp.resource_id)
        return pool

    def modify(self, name=None, description=None, raid_groups=None,
               alert_threshold=None,
               is_harvest_enabled=None,
               is_snap_harvest_enabled=None,
               pool_harvest_high_threshold=None,
               pool_harvest_low_threshold=None,
               snap_harvest_high_threshold=None,
               snap_harvest_low_threshold=None,
               is_fast_cache_enabled=None,
               is_fastvp_enabled=None):
        req_body = self._compose_pool_parameter(
            self._cli, name=name, description=description,
            raid_groups=raid_groups, alert_threshold=alert_threshold,
            is_harvest_enabled=is_harvest_enabled,
            is_snap_harvest_enabled=is_snap_harvest_enabled,
            pool_harvest_high_threshold=pool_harvest_high_threshold,
            pool_harvest_low_threshold=pool_harvest_low_threshold,
            snap_harvest_high_threshold=snap_harvest_high_threshold,
            snap_harvest_low_threshold=snap_harvest_low_threshold,
            is_fast_cache_enabled=is_fast_cache_enabled,
            is_fastvp_enabled=is_fastvp_enabled)
        resp = self.action('modify', **req_body)
        resp.raise_if_err()
        return resp

    def create_filesystem(self, nas_server, name, size, proto=None,
                          is_thin=None, tiering_policy=None, user_cap=False,
                          is_compression=None, access_policy=None,
                          locking_policy=None, description=None):
        clz = storops.unity.resource.filesystem.UnityFileSystem
        return clz.create(self._cli, self,
                          nas_server=nas_server,
                          name=name,
                          size=size,
                          proto=proto,
                          is_thin=is_thin,
                          tiering_policy=tiering_policy,
                          user_cap=user_cap,
                          is_compression=is_compression,
                          access_policy=access_policy,
                          locking_policy=locking_policy,
                          description=description)

    def create_lun(self, lun_name=None, size_gb=1, sp=None, host_access=None,
                   is_thin=None, description=None, tiering_policy=None,
                   is_repl_dst=None, snap_schedule=None,
                   is_snap_schedule_paused=None,
                   skip_sync_to_remote_system=None,
                   io_limit_policy=None, is_compression=None,
                   is_advanced_dedup_enabled=None):
        size = int(bitmath.GiB(size_gb).to_Byte().value)
        return UnityLun.create(
            self._cli, lun_name, self, size, sp=sp,
            host_access=host_access, is_thin=is_thin,
            description=description,
            is_repl_dst=is_repl_dst,
            tiering_policy=tiering_policy,
            snap_schedule=snap_schedule,
            is_snap_schedule_paused=is_snap_schedule_paused,
            skip_sync_to_remote_system=skip_sync_to_remote_system,
            io_limit_policy=io_limit_policy,
            is_compression=is_compression,
            is_advanced_dedup_enabled=is_advanced_dedup_enabled)

    def create_vmfs(self, vmfs_name=None, size_gb=1, sp=None, host_access=None,
                    is_thin=None, description=None, tiering_policy=None,
                    is_repl_dst=None, snap_schedule=None,
                    is_snap_schedule_paused=None,
                    skip_sync_to_remote_system=None, io_limit_policy=None,
                    is_compression=None, major_version=None, block_size=None):
        size = int(bitmath.GiB(size_gb).to_Byte().value)
        return UnityLun.create(
            self._cli, vmfs_name, self, size, sp=sp,
            host_access=host_access, is_thin=is_thin,
            description=description,
            is_repl_dst=is_repl_dst,
            tiering_policy=tiering_policy,
            snap_schedule=snap_schedule,
            is_snap_schedule_paused=is_snap_schedule_paused,
            skip_sync_to_remote_system=skip_sync_to_remote_system,
            io_limit_policy=io_limit_policy,
            is_compression=is_compression,
            create_vmfs=True,
            major_version=major_version,
            block_size=block_size)

    def create_nfs_share(self, nas_server, name, size, is_thin=None,
                         tiering_policy=None, user_cap=False, path=None,
                         default_access=None, min_security=None,
                         no_access_hosts=None, read_only_hosts=None,
                         read_write_hosts=None, root_access_hosts=None,
                         read_only_root_access_hosts=None,
                         no_access_hosts_string=None,
                         read_only_hosts_string=None,
                         read_write_hosts_string=None,
                         read_only_root_hosts_string=None,
                         root_access_hosts_string=None,
                         anonymous_uid=None, anonymous_gid=None,
                         export_option=None):
        clz = storops.unity.resource.job.UnityJob
        return clz.create_nfs_share(
            self._cli, self, nas_server, name, size,
            is_thin, tiering_policy, False,
            user_cap=user_cap, path=path,
            default_access=default_access,
            min_security=min_security,
            no_access_hosts=no_access_hosts,
            read_only_hosts=read_only_hosts,
            read_write_hosts=read_write_hosts,
            root_access_hosts=root_access_hosts,
            read_only_root_access_hosts=read_only_root_access_hosts,
            no_access_hosts_string=no_access_hosts_string,
            read_only_hosts_string=read_only_hosts_string,
            read_write_hosts_string=read_write_hosts_string,
            read_only_root_hosts_string=read_only_root_hosts_string,
            root_access_hosts_string=root_access_hosts_string,
            anonymous_uid=anonymous_uid,
            anonymous_gid=anonymous_gid,
            export_option=export_option)

    @staticmethod
    def _compose_pool_parameter(cli, **kwargs):
        name = kwargs.get('name')
        raid_groups = kwargs.get('raid_groups')
        req_body = cli.make_body(
            name=name,
            description=kwargs.get('description'),
            addRaidGroupParameters=UnityPool._compose_raid_group_parameter(
                cli, raid_groups),
            alertThreshold=kwargs.get('alert_threshold'),
            poolSpaceHarvestHighThreshold=kwargs.get(
                'pool_harvest_high_threshold'),
            poolSpaceHarvestLowThreshold=kwargs.get(
                'pool_harvest_low_threshold'),
            snapSpaceHarvestHighThreshold=kwargs.get(
                'snap_harvest_high_threshold'),
            snapSpaceHarvestLowThreshold=kwargs.get(
                'snap_harvest_low_threshold'),
            isHarvestEnabled=kwargs.get('is_harvest_enabled'),
            isSnapHarvestEnabled=kwargs.get('is_snap_harvest_enabled'),
            isFASTCacheEnabled=kwargs.get('is_fast_cache_enabled'),
            isFASTVpScheduleEnabled=kwargs.get('is_fastvp_enabled'),
            type=kwargs.get('pool_type'))
        return req_body

    @staticmethod
    def _compose_raid_group_parameter(cli, raid_groups):
        req_body = None
        if raid_groups:
            req_body = []
            for raid in raid_groups:
                each = cli.make_body(
                    dskGroup=raid.disk_group,
                    numDisks=raid.disk_num,
                    raidType=raid.raid_type,
                    stripeWidth=raid.stripe_width
                )
                req_body.append(each)

        return req_body

    @property
    def disk_groups(self):
        disks = self._get_unity_rsc(clz=UnityDiskList)
        pool_disks = [d for d in disks if
                      d.pool and d.pool.get_id() == self.get_id()]
        dgs = {}

        for pd in pool_disks:
            if pd.disk_group.get_id() in dgs:
                dgs[pd.disk_group.get_id()].append(pd)
            else:
                dgs[pd.disk_group.get_id()] = [pd]
        return dgs

    def is_compression_supported(self):
        return self.is_all_flash

    def _is_advanced_dedup_supported(self, support_matrix):
        from storops.unity.resource.system import UnitySystem
        unity_system = UnitySystem(cli=self._cli)
        supported = False
        for supported_model in support_matrix:
            if UnityModel(unity_system.model) >= UnityModel(supported_model):
                supported = True
                break
        return supported and self.is_all_flash

    @version('<4.5')
    def is_advanced_dedup_supported(self):
        return False

    @version('>=4.5')  # noqa
    def is_advanced_dedup_supported(self):
        support_matrix = ['450F', '550F', '650F']
        return self._is_advanced_dedup_supported(support_matrix)

    @version('>=5.0')  # noqa
    def is_advanced_dedup_supported(self):
        support_matrix = ['380', '480', '680', '880',
                          '380F', '450F', '550F', '650F', '880F']
        return self._is_advanced_dedup_supported(support_matrix)


class UnityPoolList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityPool


class UnityPoolTier(UnityAttributeResource):
    pass


class UnityPoolTierList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityPoolTier


class UnityPoolUnit(UnityResource):
    pass


class UnityPoolUnitList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityPoolUnit


class UnityPoolFastVp(UnityAttributeResource):
    pass


class RaidGroupParameter(object):
    def __init__(self, disk_group, disk_num, raid_type, stripe_width):
        """Object to store parameters needed by the UnityPool.create."""
        if not isinstance(disk_group, UnityResource):
            disk_group = UnityDiskGroup(_id=disk_group)
        self.disk_group = disk_group
        self.disk_num = disk_num
        self.raid_type = raid_type
        self.stripe_width = stripe_width
