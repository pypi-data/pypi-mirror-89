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
import re
from datetime import datetime, timedelta
from functools import partial
from operator import is_not

import bitmath
import dateutil.parser
import six

from storops.vnx import enums

__author__ = 'Cedric Zhuang'

log = logging.getLogger(__name__)

NAs = ['N/A', 'Unbound', 'None', 'Disabled',
       'This disk does not belong to a RAIDGroup']


def to_bool(str_input):
    ret = False
    if str_input.strip().lower() in ('yes', 'true', 'enabled', 'on'):
        ret = True
    return ret


def to_hex(number):
    if number is not None:
        h = hex(number)
        if h.endswith('L'):
            h = h[:-1]
    else:
        h = None
    return h


def to_wwn(str_input):
    str_input = str_input.upper()
    if ':' not in str_input:
        items = [str_input[i:i + 2] for i in range(0, len(str_input), 2)]
        ret = ':'.join(items)
    else:
        ret = str_input
    return ret


def to_int_arr(inputs):
    if inputs is not None:
        if isinstance(inputs, six.string_types):
            inputs = re.split(',| ', inputs)
        ints = map(to_int, inputs)
        ret = list(filter(partial(is_not, None), ints))
    else:
        ret = []
    return ret


def to_int_str_map(str_input):
    ret = {}
    for pair in re.findall(r'(\w+):\s*(\w+)', str_input):
        ret[to_int(pair[0])] = pair[1].strip()
    return ret


def to_int_int_map(str_input):
    ret = {}
    for pair in re.findall(r'(\w+):\s*(\w+)', str_input):
        ret[to_int(pair[0])] = to_int(pair[1])
    return ret


def arr_to_str(int_arr, sep=None):
    if sep is None:
        sep = ','
    return sep.join((six.text_type(i) for i in int_arr))


def to_str_arr(int_arr):
    return [six.text_type(i) for i in int_arr]


def to_float(value):
    ret = None
    if value is not None:
        if value.endswith('%'):
            value = value[:-1]
        try:
            ret = float(value)
        except ValueError:
            pass
    return ret


def to_int(value):
    ret = None
    if value is not None:
        try:
            if isinstance(value, six.integer_types):
                ret = value
            elif len(value) > 0:
                ret = int(value)
        except ValueError:
            if value not in NAs:
                log.warn('cannot convert "{}" to int.'.format(value))
    return ret


def to_alu_hlu_map(input_str):
    """Converter for alu hlu map

    Convert following input into a alu -> hlu map:
    Sample input:

    ```
      HLU Number     ALU Number
      ----------     ----------
        0               12
        1               23
    ```

    ALU stands for array LUN number
    hlu stands for host LUN number
    :param input_str: raw input from naviseccli
    :return: alu -> hlu map
    """
    ret = {}
    if input_str is not None:
        pattern = re.compile(r'(\d+)\s*(\d+)')
        for line in input_str.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue
            matched = re.search(pattern, line)
            if matched is None or len(matched.groups()) < 2:
                continue
            else:
                hlu = matched.group(1)
                alu = matched.group(2)
                ret[int(alu)] = int(hlu)
    return ret


def to_disk_indices(value):
    """Convert following input to disk indices

    Sample input:

    ```
    Disks:
    Bus 0 Enclosure 0 Disk 9
    Bus 1 Enclosure 0 Disk 12
    Bus 1 Enclosure 0 Disk 9
    Bus 0 Enclosure 0 Disk 4
    Bus 0 Enclosure 0 Disk 7
    ```

    :param value: disk list
    :return: disk indices in list
    """
    ret = []
    p = re.compile(r'Bus\s+(\w+)\s+Enclosure\s+(\w+)\s+Disk\s+(\w+)')
    if value is not None:
        for line in value.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue
            matched = re.search(p, line)
            if matched is None or len(matched.groups()) < 3:
                continue
            else:
                ret.append('{}_{}_{}'.format(*matched.groups()))
    return ret


def vnx_time_to_date(value):
    return datetime.utcfromtimestamp(value - 2177452800)


def to_datetime(value):
    return dateutil.parser.parse(value)


def to_time_delta(value):
    hours, minutes, seconds = map(float, value.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def _to_enum(enum_class):
    def _enum_converter(value):
        return enum_class.parse(value)

    return _enum_converter


to_sp_enum = _to_enum(enums.VNXSPEnum)
to_mirror_view_recovery_policy = _to_enum(enums.VNXMirrorViewRecoveryPolicy)
to_mirror_view_sync_rate = _to_enum(enums.VNXMirrorViewSyncRate)
to_mirror_group_recovery_policy = _to_enum(enums.VNXMirrorGroupRecoveryPolicy)
to_raid_type = _to_enum(enums.VNXRaidType)
to_pool_raid_type = _to_enum(enums.VNXPoolRaidType)
to_port_type = _to_enum(enums.VNXPortType)
to_migration_rate_enum = _to_enum(enums.VNXMigrationRate)


def to_raid_type_list(value):
    return [to_raid_type(x) for x in value.split()]


def boolean_to_str(value, true_str='true', false_str='false'):
    if value:
        ret = true_str
    else:
        ret = false_str
    return ret


def url_to_host(url):
    """convert a url to a host (ip or domain)

    :param url: url string
    :returns: host: domain name or ipv4/v6 address
    :rtype: str
    :raises: ValueError: given an illegal url that without a ip or domain name
    """

    regex_url = r"([a-z][a-z0-9+\-.]*://)?" + \
                r"([a-z0-9\-._~%!$&'()*+,;=]+@)?" + \
                r"([a-z0-9\-._~%]+" + \
                r"|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])?" + \
                r"(:(?P<port>[0-9]+))?"

    m = re.match(regex_url, url, re.IGNORECASE)
    if m and m.group(3):
        return url[m.start(3): m.end(3)]
    else:
        raise ValueError("URL without a valid host or ip")


def parse_host_address(addr):
    """
    parse host address to get domain name or ipv4/v6 address,
    cidr prefix and net mask code string if given a subnet address

    :param addr:
    :type addr: str
    :return: parsed domain name/ipv4 address/ipv6 address,
             cidr prefix if there is,
             net mask code string if there is
    :rtype: (string, int, string)
    """

    if addr.startswith('[') and addr.endswith(']'):
        addr = addr[1:-1]

    parts = addr.split('/')
    if len(parts) == 1:
        return parts[0], None, None
    if len(parts) > 2:
        raise ValueError("Illegal host address")
    else:
        domain_or_ip, prefix = parts
        prefix = int(prefix)
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", domain_or_ip):
            return domain_or_ip, prefix, ipv4_prefix_to_mask(prefix)
        elif ':' in domain_or_ip:
            return domain_or_ip, prefix, ipv6_prefix_to_mask(prefix)
        else:
            return domain_or_ip, None, None


def ipv4_prefix_to_mask(prefix):
    """
    ipv4 cidr prefix to net mask

    :param prefix: cidr prefix , rang in (0, 32)
    :type prefix: int
    :return: dot separated ipv4 net mask code, eg: 255.255.255.0
    :rtype: str
    """
    if prefix > 32 or prefix < 0:
        raise ValueError("invalid cidr prefix for ipv4")
    else:
        mask = ((1 << 32) - 1) ^ ((1 << (32 - prefix)) - 1)
        eight_ones = 255  # 0b11111111
        mask_str = ''
        for i in range(0, 4):
            mask_str = str(mask & eight_ones) + mask_str
            mask = mask >> 8
            if i != 3:
                mask_str = '.' + mask_str
        return mask_str


def ipv6_prefix_to_mask(prefix):
    """
    ipv6 cidr prefix to net mask

    :param prefix: cidr prefix, rang in (0, 128)
    :type prefix: int
    :return: comma separated ipv6 net mask code,
             eg: ffff:ffff:ffff:ffff:0000:0000:0000:0000
    :rtype: str
    """
    if prefix > 128 or prefix < 0:
        raise ValueError("invalid cidr prefix for ipv6")
    else:
        mask = ((1 << 128) - 1) ^ ((1 << (128 - prefix)) - 1)
        f = 15  # 0xf or 0b1111
        hex_mask_str = ''
        for i in range(0, 32):
            hex_mask_str = format((mask & f), 'x') + hex_mask_str
            mask = mask >> 4
            if i != 31 and i & 3 == 3:
                hex_mask_str = ':' + hex_mask_str
        return hex_mask_str


def mb_to_gb(mib):
    return bitmath.MiB(mib).to_GiB().value


def block_to_gb(block):
    return bitmath.Byte(block * 512).to_GiB().value


def to_minute(minute_str):
    ret = None
    if minute_str:
        m = re.match(r"00:(\d+):00.000$", minute_str)
        if m:
            ret = int(m.group(1))
    return ret


def from_minute(minute_in_int):
    if minute_in_int:
        if 1 <= minute_in_int <= 60:
            ret = "00:%02d:00.000" % minute_in_int
        else:
            raise ValueError("Value for minute must be 1 - 60.")
    else:
        ret = None
    return ret


def to_hour(hour_str):
    ret = None
    if hour_str:
        m = re.match(r"(\d+):00:00.000$", hour_str)
        if m:
            ret = int(m.group(1))
    return ret


def from_hour(hour_in_int):
    if hour_in_int:
        if 1 <= hour_in_int <= 24:
            ret = "%02d:00:00.000" % hour_in_int
        else:
            raise ValueError("Value for hour must be 1 - 24.")
    else:
        ret = None
    return ret
