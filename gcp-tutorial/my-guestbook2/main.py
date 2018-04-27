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

    @classmethod
    def query_type(cls, type):
        return cls.query(Tag.type == type).order(cls.type)


class Guestbook(ndb.Model):
    """Models an entry with each guestbook's name"""
    name = ndb.StringProperty()
    tag = ndb.KeyProperty(kind=Tag, repeated=True)

    @classmethod
    def query_book(cls):
        return cls.query().order(cls.name)

    @classmethod
    def query_tagkey(cls, key):
        return cls.query(Guestbook.tag == key).order(cls.name)


class GuestbookPage(webapp2.RequestHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(long(guestbook_id))

        greeting_blockquotes = self.__createGreetingBlockquotes(guestbook)
        tag_connected_blockquotes = self.__createTagConnectedBlockquotes(guestbook)
        tag_unconnected_blockquotes = self.__createTagUnonnectedBlockquotes(guestbook)

        self.response.out.write(textwrap.dedent("""
            <html>
                <body>
                    <h1>{guestbook_name}</h1>
                    <form action="/renamebook" method="post">
                        <div>
                            <input type="hidden" name="guestbook_id" value="{guestbook_id}">
                            <input type="text" name="newguestbook_name" value="{guestbook_name}" size="40" maxlength="20">
                            <input type="submit" value="Rename Guestbook">
                        </div>
                    </form>
                    <hr>
                    
                    <h2>Tag</h2>
                    <div>{tag_connected_blockquotes}</div>
                    <form action="/attachtag" method="post">
                        <div>
                            {tag_unconnected_blockquotes}
                            <input type="hidden" name="guestbook_id" value="{guestbook_id}">
                            <input type="submit" value="Add selected tag to this book">
                        </div>
                    </form>
                    <form action="/createtag" method="post">
                        <div>
                            <input type="text" name="tag_type" size="40" maxlength="20">
                            <input type="hidden" name="guestbook_id" value="{guestbook_id}">
                            <input type="submit" value="Create New Tag">
                        </div>
                    </form>
                    
                    <h2>Sign</h2>
                    <form action="/sign" method="post">
                        <div>
                            <textarea name="content" rows="5" cols="60"></textarea>
                            <input type="hidden" name="guestbook_id" value="{guestbook_id}">
                            <input type="submit" value="Sign Guestbook">
                        </div>
                    </form>
                    
                    {greeting_blockquotes}
                    <hr>
                    
                    <input type="button" value="back to list" onClick="location.href='/'">
                </body>
            </html>""").format(
            guestbook_id=guestbook_id,
            guestbook_name=cgi.escape(guestbook.name),
            greeting_blockquotes='\n'.join(greeting_blockquotes),
            tag_connected_blockquotes='\t'.join(tag_connected_blockquotes),
            tag_unconnected_blockquotes='\t'.join(tag_unconnected_blockquotes)
        ))

    def __createGreetingBlockquotes(self, guestbook):
        ancestor_key = guestbook.key
        greetings = Greeting.query_greeting(ancestor_key)
        greeting_blockquotes = []
        for greeting in greetings:
            greeting_blockquotes.append('''
            <form action="/delete" method="post">
                <div>
                    %s
                    <input type="hidden" name="guestbook_id" value="%s">
                    <input type="hidden" name="greeting_id" value="%s">
                    <input type="submit" value="delete">
                </div>
            </form>
            <blockquote>%s</blockquote>
            ''' % (
                cgi.escape(greeting.date.strftime("%Y/%m/%d %H:%M:%S")),
                guestbook.key.id(),
                greeting.key.id(),
                cgi.escape(greeting.content)))
        return greeting_blockquotes

    def __createTagConnectedBlockquotes(self, guestbook):
        tagkeys = guestbook.tag
        tag_blockquotes = []
        for key in tagkeys:
            tag_blockquotes.append(cgi.escape(key.get().type))
        return tag_blockquotes

    def __createTagUnonnectedBlockquotes(self, guestbook):
        type_all = []
        alltags = Tag.query_tag()
        for tag in alltags:
            type_all.append(cgi.escape(tag.type))

        type_connected = []
        tagkeys = guestbook.tag
        for key in tagkeys:
            type_connected.append(cgi.escape(key.get().type))

        type_all_set = set(type_all)
        type_connected_set = set(type_connected)
        type_unconnected = list(type_all_set - type_connected_set)

        type_blockquotes = []
        for type in type_unconnected:
            type_blockquotes.append('''
            <input type="checkbox" name="%s" value=true>%s
            ''' % (cgi.escape(type), cgi.escape(type)))

        return type_blockquotes


class ListPage(webapp2.RequestHandler):
    def get(self):
        tag_type = self.request.get('tag')
        if tag_type:
            guestbook_links = self.__createBookLinksWithTag(tag_type)
            self.response.out.write(textwrap.dedent("""
                <html>
                    <body>
                        <h1>Guestbook List (Tag: %s)</h1>
                        <table>{books}</table>
                        
                        <hr>
                        <input type="button" value="back to list" onClick="location.href='/'">
                    </body>
                </html>""" % tag_type).format(
                books='\n'.join(guestbook_links)))
        else:
            guestbook_links = self.__createBookLinks()
            tag_links = self.__createTagLinks()

            self.response.out.write(textwrap.dedent("""
                <html>
                    <body>
                        <h1>Guestbook List</h1>
                        <table>{books}</table>
                        <form action="/createbook" method="post">
                            <div>
                                <p>
                                <input type="text" name="guestbook_name" size="40" maxlength="20">
                                <input type="submit" value="Create New Guestbook">
                                </p>
                                <p>
                                <b>tag:</b> {tags}
                                </p>
                            </div>
                        </form>
                        <form action="/createtag" method="post">
                            <div>
                                <input type="text" name="tag_type" size="40" maxlength="20">
                                <input type="submit" value="Create New Tag">
                            </div>
                        </form>
                    </body>
                </html>""").format(
                books='\n'.join(guestbook_links),
                tags='\t'.join(tag_links)))

    def __createBookLinks(self):
        guestbooks = Guestbook.query_book()
        guestbook_links = []
        for guestbook in guestbooks:
            ancestor_key = guestbook.key
            greetings = Greeting.query_greeting(ancestor_key)
            guestbook_links.append('''
                <tr>
                    <td><a href="/books/%s">%s</a></td>
                    <td>(%s)</td>
                </tr>''' % (guestbook.key.id(),
                            cgi.escape(guestbook.name),
                            str(greetings.count())))
        return guestbook_links

    def __createBookLinksWithTag(self, tag_type):
        [tags] = Tag.query_type(type=tag_type)
        key = tags.key
        guestbooks = Guestbook.query_tagkey(key)
        guestbook_links = []
        for guestbook in guestbooks:
            ancestor_key = guestbook.key
            greetings = Greeting.query_greeting(ancestor_key)
            guestbook_links.append('''
                <tr>
                    <td><a href="/books/%s">%s</a></td>
                    <td>(%s)</td>
                </tr>''' % (guestbook.key.id(), cgi.escape(guestbook.name), str(greetings.count())))
        return guestbook_links

    def __createTagLinks(self):
        tags = Tag.query_tag()
        tag_links = []
        for tag in tags:
            tag_links.append('''
                <input type="checkbox" name="%s" value=true><a href="/?tag=%s">%s</a>
                ''' % (cgi.escape(tag.type),
                       cgi.escape(tag.type),
                       cgi.escape(tag.type)))
        return tag_links


class SubmitForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        greeting = Greeting(parent=guestbook.key,
                            content=self.request.get('content'))
        future = greeting.put_async()
        future.get_result()
        self.redirect('/books/' + str(guestbook_id))


class DeleteGreetingForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        greeting_id = self.request.get('greeting_id')
        greeting = Greeting.get_by_id(parent=guestbook.key,
                                      id=long(greeting_id))
        greeting.key.delete()
        guestbook_id = self.request.get('guestbook_id')
        self.redirect('/books/' + str(guestbook_id))


class CreatebookForm(webapp2.RequestHandler):
    def post(self):
        guestbook_name_candidate = self.request.get('guestbook_name')
        guestbook_name = self.__decideBookName(guestbook_name_candidate)

        guestbook = Guestbook(name=guestbook_name)
        future = guestbook.put_async()
        future.get_result()

        self.__attachTagToBook(guestbook)

        time.sleep(0.1)  # wait for put() have finished
        self.redirect('/')

    def __decideBookName(self, guestbook_name):
        """create guestbook name from inputted text"""
        guestbooks = Guestbook.query_book()

        # get list of every guestbook's name
        guestbookNames = []
        for guestbook in guestbooks:
            guestbookNames.append(guestbook.name)

        if guestbook_name == '':
            guestbook_name = 'New Guestbook'

        if guestbook_name in guestbookNames:
            # when the name has been used, add number to the name like [name N]
            number = 1
            guestbook_name_n = guestbook_name
            while guestbook_name_n in guestbookNames:
                number += 1
                guestbook_name_n = guestbook_name + (' %d' % number)
            guestbook_name = guestbook_name_n
        return guestbook_name

    def __attachTagToBook(self, guestbook):
        """ attach selected tag to the guestbook"""
        tags = Tag.query_tag()
        for tag in tags:
            if self.request.get(tag.type):
                guestbook.tag.append(tag.key)
        future = guestbook.put_async()
        future.get_result()


class RenamebookForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        newguestbook_name = self.request.get('newguestbook_name')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        guestbook.name = newguestbook_name
        future = guestbook.put_async()
        future.get_result()
        self.redirect('/books/' + str(guestbook_id))


class CreatetagForm(webapp2.RequestHandler):
    def post(self):
        type = self.request.get('tag_type')
        if Tag.query(Tag.type == type).get() or type == '':
            pass
        else:
            tag = Tag(type=type)
            future = tag.put_async()
            future.get_result()
            time.sleep(0.1)  # wait for put() have finished

        guestbook_id = self.request.get('guestbook_id')
        if guestbook_id:
            self.redirect('/books/' + str(guestbook_id))
        else:
            self.redirect('/')


class AttachtagForm(webapp2.RequestHandler):
    def post(self):
        guestbook_id = self.request.get('guestbook_id')
        guestbook = Guestbook.get_by_id(long(guestbook_id))
        tags = Tag.query_tag()
        for tag in tags:
            if self.request.get(tag.type):
                guestbook.tag.append(tag.key)
        future = guestbook.put_async()
        future.get_result()
        self.redirect('/books/' + str(guestbook_id))


app = webapp2.WSGIApplication([
    webapp2.Route(r'/books/<guestbook_id:\d+>', handler=GuestbookPage, name='book'),
    webapp2.Route(r'/', handler=ListPage, name='book-list'),
    webapp2.Route(r'/sign', handler=SubmitForm, name='sign'),
    webapp2.Route(r'/delete', handler=DeleteGreetingForm, name='deletegreeting'),
    webapp2.Route(r'/createbook', handler=CreatebookForm, name='createbook'),
    webapp2.Route(r'/renamebook', handler=RenamebookForm, name='renamebook'),
    webapp2.Route(r'/createtag', handler=CreatetagForm, name='createtag'),
    webapp2.Route(r'/attachtag', handler=AttachtagForm, name='attachtag')
])
