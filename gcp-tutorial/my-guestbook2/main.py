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
        return cls.query().order(cls.type)


class Guestbook(ndb.Model):
    """Models an entry with each guestbook's name"""
    name = ndb.StringProperty()
    tag = ndb.KeyProperty(kind=Tag, repeated=True)

    @classmethod
    def query_book(cls):
        return cls.query().order(cls.name)


class GuestbookPage(webapp2.RequestHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        ancestor_key = guestbook.key
        greetings = Greeting.query_greeting(ancestor_key)

        # create {blockquote}
        greeting_blockquotes = []
        for greeting in greetings:
            print(greeting.date)
            greeting_blockquotes.append(
                '%s<blockquote>%s</blockquote>' % (cgi.escape(greeting.date.strftime("%Y/%m/%d %H:%M:%S")), cgi.escape(greeting.content)))

        self.response.out.write(textwrap.dedent("""
            <html>
                <body>
                    <h1>{guestbook_name}</h1>
                    <form action="/renamebook?%s" method="post">
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
        # create {books}
        guestbooks = Guestbook.query_book()
        guestbook_links = []
        for guestbook in guestbooks:
            ancestor_key = guestbook.key
            greetings = Greeting.query_greeting(ancestor_key)
            guestbook_links.append('''
                <tr>
                    <td><a href="/books/%s">%s</a></td>
                    <td>(%s)</td>
                </tr>''' % (guestbook.key.id(), cgi.escape(guestbook.name), len(greetings))
                                   )

        # create {tags}
        tags = Tag.query_tag()
        tag_links = []
        for tag in tags:
            tag_links.append('''
                <tr>
                    <td>%s</td>
                </tr>''' % cgi.escape(tag.type))

        self.response.out.write(textwrap.dedent("""
            <html>
                <body>
                    <h1>Guestbook List</h1>
                    <h2>books</h2>
                    <table>{books}</table>
                    <form action="/createbook" method="post">
                        <div>
                            <input type="text" name="guestbook_name" size="40" maxlength="20">
                            <input type="submit" value="Create New Guestbook">
                        </div>
                    </form>
                    <h2>tags</h2><table>{tags}
                    </table>
                    <form action="/createtag" method="post">
                        <div>
                            <input type="text" name="tag_type" size="40" maxlength="20">
                            <input type="submit" value="Create New Tag">
                        </div>
                    </form>
                </body>
            </html>""").format(
            books='\n'.join(guestbook_links),
            tags='\n'.join(tag_links)))


class SubmitForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        greeting = Greeting(parent=guestbook.key,
                            content=self.request.get('content'))
        greeting.put()
        self.redirect('/books/' + str(guestbook_id))


class CreatebookForm(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        guestbooks = Guestbook.query_book()

        # get list of every guestbook's name
        guestbooknames = []
        for guestbook in guestbooks:
            guestbooknames.append(guestbook.name)

        if guestbook_name == '':
            guestbook_name = 'New Guestbook'

        if guestbook_name in guestbooknames:
            # when the name has been used, add number to the name like [name N]
            number = 1
            guestbook_name_n = guestbook_name
            while guestbook_name_n in guestbooknames:
                number += 1
                guestbook_name_n = guestbook_name + (' %d' % number)
            guestbook_name = guestbook_name_n

        guestbook = Guestbook(name=guestbook_name)
        guestbook.put()

        time.sleep(0.1)  # wait for put() have finished
        self.redirect('/')


class RenamebookForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        newguestbook_name = self.request.get('newguestbook_name')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        guestbook.name = newguestbook_name
        guestbook.put()
        self.redirect('/books/' + str(guestbook_id))


class CreatetagForm(webapp2.RequestHandler):
    def post(self):
        type = self.request.get('tag_type')
        if Tag.query(Tag.type == type).get() or type == '':
            pass
        else:
            tag = Tag(type=type)
            tag.put()
            time.sleep(0.1) # wait for put() have finished
        self.redirect('/')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/books/<guestbook_id:\d+>', handler=GuestbookPage, name='book'),
    webapp2.Route(r'/', handler=ListPage, name='book-list'),
    webapp2.Route(r'/sign', handler=SubmitForm, name='sign'),
    webapp2.Route(r'/createbook', handler=CreatebookForm, name='createbook'),
    webapp2.Route(r'/renamebook', handler=RenamebookForm, name='renamebook'),
    webapp2.Route(r'/createtag', handler=CreatetagForm, name='createtag')
])
