#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from webapp2_extras import sessions

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

# [START main_page]
class MainPage(BaseHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START guestbook]
class Guestbook(BaseHandler):

    def post(self):
        # we set the same parent key on the 'greeting' to ensure each
        # greeting is in the same entity group. queries across the
        # single entity group will be consistent. however, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          default_guestbook_name)
        greeting = greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]

class SignupPage(BaseHandler):
    def get(self):
        self.response.write("""
        <html><body>
            <h1>Sign Up</h1>
            <form action="/signupform" method="post">
                <div>
                    id: <input type="text" name="id" size="40" maxlength="20">
                    <br>
                    password: <input type="password" name="password" size="40" maxlength="20">
                    <hr>
                    <input type="submit" value="Sign Up">
                </div>
            </form>
            <a href="/login">or login</a>
        </body></html>"""
        )

class LoginPage(BaseHandler):
    def get(self):
        self.response.write("""
        <html><body>
            <h1>Login</h1>
            <form action="/loginform" method="post">
                <div>
                    id: <input type="text" name="id" size="40" maxlength="20">
                    <br>
                    password: <input type="password" name="password" size="40" maxlength="20">
                    <hr>
                    <input type="submit" value="Login">
                </div>
                <a href="/signup">or signup</a>
            </form>
        </body></html>
        """)

class SignupForm(BaseHandler):
    pass

class LoginForm(BaseHandler):
    pass

class LogoutForm(BaseHandler):
    pass

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/signup', SignupPage),
    ('/signupform', SignupForm),
    ('/login', LoginPage),
    ('/loginform', LoginForm),
    ('/logoutform', LogoutForm)
], debug=True, config=config)
# [END app]
