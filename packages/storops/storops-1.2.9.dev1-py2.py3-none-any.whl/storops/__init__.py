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

import sys
import logging

from storops.lib.thinclone_helper import TCHelper  # noqa
from storops.unity.enums import *  # noqa
from storops.unity.resource.system import UnitySystem  # noqa
from storops.unity.resource.snap_schedule import UnitySnapScheduleRule  # noqa
from storops.vnx.enums import *  # noqa
from storops.vnx.resource.system import VNXSystem  # noqa
from storops.vnx.sg_cache import SGCache  # noqa

__author__ = 'Cedric Zhuang'


def enable_log(level=logging.DEBUG):
    """Enable console logging.

    This is a utils method for try run with storops.
    :param level: log level, default to DEBUG
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    if not logger.handlers:
        logger.info('enabling logging to console.')
        logger.addHandler(logging.StreamHandler(sys.stdout))


def disable_log():
    logger = logging.getLogger(__name__)
    logger.info('disabling logging to console.')
    logger.setLevel(logging.NOTSET)
    logger.handlers = []
    return logger
