# coding=utf-8
# Copyright (c) 2016 EMC Corporation.
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

import logging
import threading
import time

import persistqueue
from persistqueue import Empty

from storops.exception import StoropsException
from storops.exception import VNXObjectNotFoundError, \
    UnityResourceNotFoundError

__author__ = 'Peter Wang'

log = logging.getLogger(__name__)


class PQueue(object):
    DEFAULT_INTERVAL = 300
    MAX_RETRIES = 100

    def __init__(self, path, interval=None):
        self.path = path
        self._q = persistqueue.Queue(self.path, tempdir=self.path)
        self._interval = (
            self.DEFAULT_INTERVAL if interval is None else interval)
        self.started = False

    def put(self, func, **kwargs):
        item = {'object': func.__self__, 'method': func.__name__,
                'params': kwargs}
        self._q.put_nowait(item)

    def get(self, block=False):
        return self._q.get(block=block)

    def task_done(self):
        self._q.task_done()

    def start(self):
        if not self.started:
            self._run()
            self.started = True
        else:
            log.info("PQueue[{}] had already started.".format(self.path))

    def stop(self):
        self._interval = 0
        self.started = False

    def set_interval(self, interval):
        self._interval = interval

    def _run(self):
        self._t = threading.Thread(target=self._run_tasks)
        self._t.setDaemon(True)
        self._t.start()

    def re_enqueue(self, item):
        """Re-enqueue till reach max retries."""
        if 'retries' in item:
            retries = item['retries']
            if retries >= self.MAX_RETRIES:
                log.warn("Failed to execute {} after {} retries, give it "
                         " up.".format(item['method'], retries))
            else:
                retries += 1
                item['retries'] = retries
                self._q.put_nowait(item)
        else:
            item['retries'] = 1
            self._q.put_nowait(item)

    @staticmethod
    def _is_ignored_exception(ex):
        ignored_exceptions = (VNXObjectNotFoundError,
                              UnityResourceNotFoundError)
        for ignored in ignored_exceptions:
            if isinstance(ex, ignored):
                return True
        return False

    @staticmethod
    def _is_reenqueue_exception(ex):
        reenqueue_exceptions = (StoropsException, )
        for reenqueue in reenqueue_exceptions:
            if isinstance(ex, reenqueue):
                return True
        return False

    def _run_tasks(self):
        while self._interval > 0:
            log.debug("Running periodical check.")
            try:
                data = self.get()
            except Empty:
                log.debug("Queue is empty now.")
            else:
                method = getattr(data['object'], data['method'], None)
                try:
                    method(**data['params'])
                except Exception as ex:
                    log.debug("Failed to execute {}: {}, this message can be "
                              "safely ignored.".format(method.__name__,
                                                       ex))
                    if self._is_ignored_exception(ex):
                        log.info("Object had been deleted: {}, this message "
                                 "can be safely ignored.".format(ex))
                    elif self._is_reenqueue_exception(ex):
                        # Re-enqueue since failed to execute
                        self.re_enqueue(data)
                    else:
                        log.error("Unexpected error occurs when executing {}:"
                                  " {}, this job will not be executed"
                                  " again".format(method.__name__, ex))
                self.task_done()
            time.sleep(self._interval)
        log.info("{} with path {} has been "
                 "stopped.".format(self.__class__.__name__, self._q.path))
