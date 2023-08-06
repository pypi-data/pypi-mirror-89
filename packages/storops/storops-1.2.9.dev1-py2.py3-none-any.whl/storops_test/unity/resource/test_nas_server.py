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

import ddt

from unittest import TestCase

from hamcrest import assert_that, equal_to, instance_of, none, raises, \
    only_contains

from storops.exception import UnityNasServerNameUsedError, \
    UnityResourceNotFoundError, UnitySmbNameInUseError, \
    UnityCifsServiceNotEnabledError, UnityPolicyInvalidParametersError
from storops.unity.enums import ReplicationTypeEnum, \
    NasServerUnixDirectoryServiceEnum, FileInterfaceRoleEnum, \
    NodeEnum
from storops.unity.resource.cifs_server import UnityCifsServerList
from storops.unity.resource.dns_server import UnityFileDnsServer
from storops.unity.resource.health import UnityHealth
from storops.unity.resource.interface import UnityPreferredInterfaceSettings, \
    UnityFileInterfaceList
from storops.unity.resource.nas_server import UnityNasServer, \
    UnityNasServerList
from storops.unity.resource.pool import UnityPool
from storops.unity.resource.sp import UnityStorageProcessor
from storops.unity.resource.system import UnityVirusChecker
from storops.unity.resource.remote_system import UnityRemoteSystem
from storops_test.unity.rest_mock import t_rest, patch_rest

__author__ = 'Cedric Zhuang'


@ddt.ddt
class UnityNasServerTest(TestCase):
    @patch_rest
    def test_properties(self):
        server = UnityNasServer(_id='nas_1', cli=t_rest())
        assert_that(server.existed, equal_to(True))
        assert_that(server.id, equal_to('nas_1'))
        assert_that(server.name, equal_to('esa_nasserver'))
        assert_that(server.health, instance_of(UnityHealth))
        assert_that(server.home_sp, instance_of(UnityStorageProcessor))
        assert_that(server.current_sp, instance_of(UnityStorageProcessor))
        assert_that(server.pool, instance_of(UnityPool))
        assert_that(server.size_allocated, equal_to(2952790016))
        assert_that(server.is_replication_enabled, equal_to(False))
        assert_that(server.is_replication_destination, equal_to(False))
        assert_that(server.replication_type,
                    equal_to(ReplicationTypeEnum.NONE))
        assert_that(server.default_unix_user, none())
        assert_that(server.default_windows_user, none())
        assert_that(server.current_unix_directory_service,
                    equal_to(NasServerUnixDirectoryServiceEnum.NONE))
        assert_that(server.is_multi_protocol_enabled, equal_to(False))
        assert_that(server.is_windows_to_unix_username_mapping_enabled, none())
        assert_that(server.allow_unmapped_user, none())
        assert_that(server.cifs_server, instance_of(UnityCifsServerList))
        assert_that(server.preferred_interface_settings,
                    instance_of(UnityPreferredInterfaceSettings))
        assert_that(server.file_dns_server, instance_of(UnityFileDnsServer))
        assert_that(server.file_interface, instance_of(UnityFileInterfaceList))
        assert_that(server.virus_checker, instance_of(UnityVirusChecker))
        assert_that(server.tenant, equal_to(None))

    @patch_rest
    def test_get_all(self):
        nas_servers = UnityNasServerList(cli=t_rest())
        assert_that(len(nas_servers), equal_to(3))

    @patch_rest
    def test_get_cifs_server_available(self):
        server = UnityNasServer(_id='nas_2', cli=t_rest())
        cifs_server = server.get_cifs_server()
        assert_that(cifs_server.domain, equal_to('win2012.dev'))

    @patch_rest
    def test_get_cifs_server_not_found(self):
        def f():
            server = UnityNasServer(_id='nas_3', cli=t_rest())
            server.get_cifs_server()

        assert_that(f, raises(UnityCifsServiceNotEnabledError, 'not enabled'))

    @ddt.data({'version': '3.0.1'},
              {'version': '4.1.0,3'})
    @ddt.unpack
    @patch_rest
    def test_create_nas3_success(self, version):
        ret = UnityNasServer.create(t_rest(version), 'nas3', 'spa', 'pool_1')
        assert_that(ret.name, equal_to('nas3'))
        assert_that(ret.existed, equal_to(True))

    @patch_rest
    def test_create_name_in_use(self):
        def f():
            UnityNasServer.create(t_rest(), 'nas4', 'spa', 'pool_1')

        assert_that(f, raises(UnityNasServerNameUsedError, 'in use'))

    @patch_rest
    def test_create_nas_server_in_tenant(self):
        UnityNasServer.create(t_rest('4.1.0'), 'nas5', 'spa',
                              'pool_1', tenant='tenant_1')

    @patch_rest
    def test_delete_not_found(self):
        def f():
            server = UnityNasServer(_id='not_found', cli=t_rest())
            server.delete()

        assert_that(f, raises(UnityResourceNotFoundError, 'not exist'))

    @patch_rest
    def test_delete_success(self):
        server = UnityNasServer(_id='nas_3', cli=t_rest())
        resp = server.delete()
        assert_that(resp.body, equal_to({}))

    @patch_rest
    def test_create_file_interface_success(self):
        server = UnityNasServer(_id='nas_2', cli=t_rest())
        fi = server.create_file_interface(
            'spa_eth2', '1.1.1.1', role=FileInterfaceRoleEnum.PRODUCTION)
        assert_that(fi.ip_address, equal_to('1.1.1.1'))

    @patch_rest
    def test_create_file_interface_ipv6_success(self):
        server = UnityNasServer(_id='nas_2', cli=t_rest())
        file_interface_ipv6 = server.create_file_interface(
            ip_port='spa_eth2',
            ip='2001:db8:0:1:f816:3eff:fe76:35c4',
            v6_prefix_length='64',
            gateway='2001:db8:0:1::1',
            role=FileInterfaceRoleEnum.PRODUCTION)
        assert_that(file_interface_ipv6.ip_address,
                    equal_to('2001:db8:0:1:f816:3eff:fe76:35c4'))
        assert_that(file_interface_ipv6.v6_prefix_length, equal_to(64))
        assert_that(file_interface_ipv6.netmask, equal_to(None))

    @patch_rest
    def test_create_cifs_server_success(self):
        server = UnityNasServer(_id='nas_5', cli=t_rest())
        cifs_server = server.create_cifs_server(name='c_server1',
                                                workgroup='CEDRIC',
                                                local_password='Password123!')
        assert_that(cifs_server.workgroup, equal_to('CEDRIC'))

    @patch_rest
    def test_enable_cifs_service_success(self):
        server = UnityNasServer(_id='nas_5', cli=t_rest())
        server.create_cifs_server(name='c_server1',
                                  workgroup='CEDRIC',
                                  local_password='Password123!')
        # no exception

    @patch_rest
    def test_create_nfs_server_success(self):
        server = UnityNasServer(_id='nas_5', cli=t_rest())
        nfs_server = server.create_nfs_server(nfs_v4_enabled=True)
        assert_that(nfs_server.id, equal_to('nfs_3'))
        assert_that(nfs_server.nfs_v4_enabled, equal_to(True))
        assert_that(nfs_server.host_name, none())

    @patch_rest
    def test_enable_nfs_service_success(self):
        server = UnityNasServer(_id='nas_5', cli=t_rest())
        server.create_nfs_server(nfs_v4_enabled=True)
        # no exception

    @patch_rest
    def test_create_dns_server_success(self):
        server = UnityNasServer.get(t_rest(), 'nas_4')
        dns = server.create_dns_server('emc.dev', '2.2.2.2', '3.3.3.3')
        assert_that(dns.addresses, only_contains('2.2.2.2', '3.3.3.3'))

    @patch_rest
    def test_create_dns_single_address(self):
        server = UnityNasServer.get(t_rest(), 'nas_6')
        dns = server.create_dns_server('emc.dev', '4.4.4.4')
        assert_that(dns.existed, equal_to(True))
        assert_that(dns.addresses, only_contains('4.4.4.4'))

    @patch_rest
    def test_enable_cifs_service_default_domain_name(self):
        server = UnityNasServer(_id='nas_2', cli=t_rest())
        server.enable_cifs_service(name='c_server2',
                                   domain_username='admin@vpshere.dev',
                                   domain_password='Password123!')

    @patch_rest
    def test_enable_cifs_service_name_in_use(self):
        def f():
            server = UnityNasServer(_id='nas_5', cli=t_rest())
            server.enable_cifs_service(name='c_server2',
                                       workgroup='CEDRIC',
                                       local_password='Password123!')

        assert_that(f, raises(UnitySmbNameInUseError, 'name already exists'))

    @patch_rest
    @ddt.data(
        {'dst_nas': 'nas_12', 'replication_name': None, 'remote_system': None,
         'expected_rep_name': 'rep_sess_nas_6_nas_12_local'},
        {'dst_nas': 'nas_6', 'replication_name': 'remote-nas_6-nas_6',
         'remote_system': 'RS_6', 'expected_rep_name': 'remote-nas_6-nas_6'},
    )
    @ddt.unpack
    def test_replicate(self, dst_nas, replication_name, remote_system,
                       expected_rep_name):
        if remote_system:
            remote_system = UnityRemoteSystem(_id=remote_system, cli=t_rest())
        nas = UnityNasServer.get(cli=t_rest(), _id='nas_6')
        rep_session = nas.replicate(dst_nas, 60,
                                    replication_name=replication_name,
                                    remote_system=remote_system)
        assert_that(rep_session.name, equal_to(expected_rep_name))

    @patch_rest
    @ddt.data(
        {'dst_nas_server_name': None, 'remote_system': None, 'rep_name': None,
         'dst_sp': None, 'is_backup_only': None,
         'expected_rep_session_id': '103079215112_APM00192210744_0000'
                                    '_103079215117_APM00192210744_0000'},
        {'dst_nas_server_name': 'nas-liangr', 'remote_system': 'RS_6',
         'rep_name': 'nas-server-rep',
         'dst_sp': NodeEnum.SPA, 'is_backup_only': False,
         'expected_rep_session_id': '103079215112_APM00192210744_0000'
                                    '_103079215110_FNM00184901113_0000'},
    )
    @ddt.unpack
    def test_replicate_with_dst_resource_provisioning(self,
                                                      dst_nas_server_name,
                                                      remote_system,
                                                      rep_name,
                                                      dst_sp,
                                                      is_backup_only,
                                                      expected_rep_session_id):
        nas_server = UnityNasServer.get(cli=t_rest(), _id='nas_6')
        if remote_system:
            remote_system = UnityRemoteSystem(_id=remote_system, cli=t_rest())
        rep_session = nas_server.replicate_with_dst_resource_provisioning(
            60, 'pool_1', dst_nas_server_name=dst_nas_server_name,
            remote_system=remote_system, replication_name=rep_name,
            dst_sp=dst_sp, is_backup_only=is_backup_only)
        assert_that(rep_session.id, equal_to(expected_rep_session_id))

    def test_replicate_with_dst_resource_provisioning_error(self):
        def f():
            nas_server = UnityNasServer.get(cli=t_rest(), _id='nas_6')
            remote_system = UnityRemoteSystem(_id='RS_6', cli=t_rest())
            nas_server.replicate_with_dst_resource_provisioning(
                60, 'pool_1', dst_nas_server_name='nas-liangr',
                remote_system=remote_system, replication_name='nas-server-rep',
                dst_sp=None, is_backup_only=False)
        assert_that(f,
                    raises(UnityPolicyInvalidParametersError,
                           ('Default storage processor is required to create '
                            'replication session with remote Unity system.')))

    @patch_rest
    def test_modify_nas_server(self):
        server = UnityNasServer(_id='nas_1', cli=t_rest())
        new_sp = UnityStorageProcessor(_id='spa', cli=t_rest())
        resp = server.modify(name='esa_nasserver', sp=new_sp)
        assert_that(resp.is_ok(), equal_to(True))
        server.update()
        assert_that(server.name, equal_to('esa_nasserver'))
        assert_that(server.home_sp.id, equal_to('spa'))


class UnityNasServerListTest(TestCase):
    @patch_rest
    def test_shadow_copy_home_sp(self):
        nas_servers = UnityNasServerList(cli=t_rest(), home_sp='spa')
        assert_that(len(nas_servers), equal_to(2))
        nas_servers = UnityNasServerList(cli=t_rest(), home_sp='spb')
        assert_that(len(nas_servers), equal_to(1))

    @patch_rest
    def test_shadow_copy_current_sp(self):
        nas_servers = UnityNasServerList(cli=t_rest(), current_sp='spa')
        assert_that(len(nas_servers), equal_to(1))
        nas_servers = UnityNasServerList(cli=t_rest(), current_sp='spb')
        assert_that(len(nas_servers), equal_to(2))
