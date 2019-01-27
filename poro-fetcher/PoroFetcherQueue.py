# coding=utf-8
#
# MIT License
#
# Copyright (c) 2018 Sven Grübel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from Queue import Queue
from httplib import HTTPSConnection
from json import loads
from re import match
from threading import Thread
from time import sleep


class PoroFetcherQueue:
    def __init__(self, host, api_key):
        self._host = host
        self._api_key = api_key
        self._queue = Queue()
        t = Thread(target=self._daemon)
        t.setDaemon(True)
        t.start()

    def add(self, url, return_func):
        self._queue.put((url, return_func))

    def wait_all(self):
        self._queue.join()

    def set_api_key(self, api_key):
        self._api_key = api_key

    def _daemon(self):
        while True:
            url, return_func = self._queue.get()
            conn = HTTPSConnection(self._host)
            conn.request("GET", url, headers={
                "X-Riot-Token": self._api_key
            })
            res = conn.getresponse()

            # Get wait time from response headers
            wait_time = self._calculate_wait_time(res)

            status = res.status
            response = res.read()
            if response:
                response = loads(response)
            conn.close()
            return_func(response, status)
            self._queue.task_done()

            # Wait if necessary
            if wait_time != 0:
                print "[{}] Reaching rate limit, better pause for {} seconds".format(self._host, wait_time)
                sleep(wait_time)
                print "[{}] Continuing...".format(self._host)

    def _calculate_wait_time(self, response):
        def parse(header):
            # TODO Handle rate limit with only one limit
            header_content = response.getheader(header)
            if header_content is None or "," not in header_content:
                return None
            m = match("(?P<small_limit>\d+):(?P<small_timeframe>\d+),(?P<big_limit>\d+):(?P<big_timeframe>\d+)",
                      header_content)
            return m.groupdict()

        app_limit = parse("X-App-Rate-Limit")
        app_count = parse("X-App-Rate-Limit-Count")
        method_limit = parse("X-Method-Rate-Limit")
        method_count = parse("X-Method-Rate-Limit-Count")

        wait_time = 0
        wait_threshold = 4

        if app_limit is not None and app_count is not None:
            app_small = int(app_limit["small_limit"]) - int(app_count["small_limit"])
            if app_small < wait_threshold:
                wait_time = int(app_limit["small_timeframe"]) / wait_threshold

            app_big = int(app_limit["big_limit"]) - int(app_count["big_limit"])
            if app_big < wait_threshold:
                wait_time = max(wait_time, int(app_limit["big_timeframe"]) / wait_threshold)

        if method_limit is not None and method_count is not None:
            method_small = int(method_limit["small_limit"]) - int(method_count["small_limit"])
            if method_small < wait_threshold:
                wait_time = max(wait_time, int(method_limit["small_timeframe"]) / wait_threshold)

            method_big = int(method_limit["big_limit"]) - int(method_count["big_limit"])
            if method_big < wait_threshold:
                wait_time = max(wait_time, int(method_limit["big_timeframe"]) / wait_threshold)

        return wait_time
