# Copyright 2015 Google Inc. All rights reserved.
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

"""Cloud Datastore NDB API guestbook sample.

This sample is used on this page:
    https://cloud.google.com/appengine/docs/python/ndb/

For more information, see README.md
"""

# [START all]
import cgi
import textwrap
import urllib

from google.appengine.ext import ndb

import webapp2


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)


class Guestbook(ndb.Model):
    """Models an entry with each guestbook's name"""
    name = ndb.StringProperty()

    @classmethod
    def query_book(cls):
        return cls.query().order(cls.name)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
        greetings = Greeting.query_book(ancestor_key).fetch(20)

        greeting_blockquotes = []
        for greeting in greetings:
            greeting_blockquotes.append(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        self.response.out.write(textwrap.dedent("""\
            <html>
              <body>
                <h1>{guestbook_name}</h1>
                {blockquotes}
                <form action="/sign?{sign}" method="post">
                  <div>
                    <textarea name="content" rows="3" cols="60">
                    </textarea>
                  </div>
                  <div>
                    <input type="submit" value="Sign Guestbook">
                  </div>
                </form>
                <hr>
                <input type="button" value="back to list" onClick="location.href='/list'">
              </body>
            </html>""").format(
            blockquotes='\n'.join(greeting_blockquotes),
            sign=urllib.urlencode({'guestbook_name': guestbook_name}),
            guestbook_name=cgi.escape(guestbook_name)))

class ListPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
        greetings = Greeting.query_book(ancestor_key).fetch(20)

        greeting_blockquotes = []
        for greeting in greetings:
            greeting_blockquotes.append(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        self.response.out.write(textwrap.dedent("""\
            <html>
              <body>
              <h1>Guestbook List</h1>
                {blockquotes}
                <form action="/create" method="post">
                  <div>
                    <textarea name="content" rows="1" cols="60">
                    </textarea>
                  </div>
                  <div>
                    <input type="submit" value="Create New Guestbook">
                  </div>
                </form>
              </body>
            </html>""").format(
            blockquotes='\n'.join(greeting_blockquotes),
            create=urllib.urlencode({'guestbook_name': guestbook_name}),
            guestbook_name=cgi.escape(guestbook_name)))


class SubmitForm(webapp2.RequestHandler):
    def post(self):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=ndb.Key("Book",
                                           guestbook_name or "*notitle*"),
                            content=self.request.get('content'))
        greeting.put()
        self.redirect('/?' + urllib.urlencode(
            {'guestbook_name': guestbook_name}))

class CreateForm(webapp2.RequestHandler):
    def post(self):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        guestbook_name = self.request.get('guestbook_name')
        guestbook = Guestbook(name=guestbook_name)
        guestbook.put()
        self.redirect('/list')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/list', ListPage),
    ('/sign', SubmitForm),
    ('/create', CreateForm)
])
