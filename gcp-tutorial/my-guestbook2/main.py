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

import cgi
import textwrap
import urllib
import time

from google.appengine.ext import ndb

import webapp2

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_greeting(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)

class Tag(ndb.Model):
    """Models an individual Guestbook ently with name"""
    type = ndb.StringProperty()

    @classmethod
    def query_tag(cls):
        return cls.query().order(cls.name)

class Guestbook(ndb.Model):
    """Models an entry with each guestbook's name"""
    name = ndb.StringProperty()
    tag = ndb.KeyProperty(kind=Tag, required=True)

    @classmethod
    def query_book(cls):
        return cls.query().order(cls.name)


class GuestbookPage(webapp2.RequestHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = guestbook.key
        greetings = Greeting.query_book(ancestor_key).fetch(20)

        # create {blockquote}
        greeting_blockquotes = []
        for greeting in greetings:
            greeting_blockquotes.append(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        self.response.out.write(textwrap.dedent("""
            <html>
                <body>
                    <h1>{guestbook_name}</h1>
                    <form action="/rename?%s" method="post">
                        <div>
                            <input type="text" name="newguestbook_name" value="{guestbook_name}" size="40" maxlength="20">
                            <input type="submit" value="Rename Guestbook">
                        </div>
                    </form>
                    {blockquotes}
                    <form action="/sign?%s" method="post">
                        <div>
                            <textarea name="content" rows="5" cols="60"></textarea>
                        </div>
                        <div>
                            <input type="submit" value="Sign Guestbook">
                        </div>
                    </form>
                    <hr>
                    <input type="button" value="back to list" onClick="location.href='/'">
                </body>
            </html>""" % (
        urllib.urlencode({'guestbook_id': guestbook_id}), urllib.urlencode({'guestbook_id': guestbook_id}))).format(
            guestbook_name=cgi.escape(guestbook.name),
            blockquotes='\n'.join(greeting_blockquotes)
        ))


class ListPage(webapp2.RequestHandler):
    def get(self):
        guestbooks = Guestbook.query_book()

        # create {tablecontent}
        guestbook_links = []
        for guestbook in guestbooks:
            ancestor_key = guestbook.key
            greetings = Greeting.query_book(ancestor_key).fetch(20)
            guestbook_links.append('''
                <tr>
                    <td><a href="/books/%s">%s</a></td>
                    <td>(%s)</td>
                </tr>''' % (guestbook.key.id(), cgi.escape(guestbook.name), len(greetings))
                                   )

        self.response.out.write(textwrap.dedent("""
            <html>
                <body>
                    <h1>Guestbook List</h1>
                    <table>
                        {tablecontent}
                    </table>
                    <form action="/create" method="post">
                        <div>
                            <input type="text" name="guestbook_name" size="40" maxlength="20">
                            <input type="submit" value="Create New Guestbook">
                        </div>
                    </form>
                </body>
            </html>""").format(
            tablecontent='\n'.join(guestbook_links)))


class SubmitForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        greeting = Greeting(parent=guestbook.key,
                            content=self.request.get('content'))
        greeting.put()
        self.redirect('/books/' + str(guestbook_id))


class CreateForm(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        guestbook = Guestbook(name=guestbook_name)
        guestbook.put()
        time.sleep(0.1)  # wait for put() have finished
        self.redirect('/')


class RenameForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        newguestbook_name = self.request.get('newguestbook_name')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        guestbook.name = newguestbook_name
        guestbook.put()
        self.redirect('/books/' + str(guestbook_id))

class AddtagForm(webapp2.RequestHandler):
    def post(self):
        type = self.request.get('type')
        if Tag.query(Tag.type == type).get() == None:
            pass
        else:
            tag = Tag(type=type)
            tag.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/books/<guestbook_id:\d+>', handler=GuestbookPage, name='book'),
    webapp2.Route(r'/', handler=ListPage, name='book-list'),
    webapp2.Route(r'/sign', handler=SubmitForm, name='sign'),
    webapp2.Route(r'/create', handler=CreateForm, name='create'),
    webapp2.Route(r'/rename', handler=RenameForm, name='rename'),
    webapp2.Route(r'/addtag', handler=AddtagForm, name='addtag')
])