# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START all]

from google.appengine.ext import ndb
import webapp2
import time


COUNTER_KEY = 'default counter'


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


class UpdateCounterHandler(webapp2.RequestHandler):
    def post(self):
        amount = int(self.request.get('amount'))

        # This task should run at most once per second because of the datastore
        # transaction write throughput.
        @ndb.transactional
        def update_counter():
            counter = Counter.get_or_insert(COUNTER_KEY, count=0)
            counter.count += amount
            counter.put()

        update_counter()

class hoge(webapp2.RequestHandler):
    def post(self):

        # This task should run at most once per second because of the datastore
        # transaction write throughput.
        @ndb.transactional
        def increment10_after_60s():
            time.sleep(60)
            counter = Counter.get_or_insert(COUNTER_KEY, count=0)
            counter.count += 10
            counter.put()

        increment10_after_60s()


app = webapp2.WSGIApplication([
    ('/update_counter', UpdateCounterHandler),
    ('/hoge', hoge)
], debug=True)
# [END all]
