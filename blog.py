#!/usr/bin/python


################################################################################
#
# Created By : Egbie  
# Name Of The Program : Blog.Py 
# Created on the 17/11/2015 at 02:45:04 hrs
# This is version : 1 
#
#
# File description 
#
# A online blog that uses the google appengine as storage and the light weight
# module for the website creation
#
################################################################################


import jinja2
import os
import webapp2
from database import PostsDb, Users
from security import Secure
from json_maker import Json

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    """BaseHandler handles all web request and responses"""

    def write(self,*a, **kw):
        """write(*a, **kw) -> returns(void)
        Writes output to screen
        """
        self.response.out.write(*a, **kw)

    def _render_template(self, template, **kw):
        """_render_template(str, dict) -> returns(val)
        A wrapper function that renders a template to the screen
        """
        template = jinja_env.get_template(template)
        return template.render(kw)

    def render(self, template, **kw):
        """Takes a template and kw and render it to the user"""
        self.write(self._render_template(template, **kw))

class Cookies(BaseHandler):
    """The cookie class is responsible for setting and
       erasing cookies
    """

    def make_cookie(self, val):
        """makes a secure hash cookie"""
        return Secure.make_secure_val(val)

    def set_cookie(self, name, cookie):
        """set the cookie to user's computer"""
        self.response.set_cookie(name, cookie, path="/")

    def delete_cookie(self, val):
        self.response.delete_cookie(val)

    def read_secure_cookie(self, cookie_name):
        """read_secure_cookie(str) -> return(str)
        Verifies whether the user cookie has not
        been tampered with. Returns the cookie
        else returns False
        """
        cookie_val = self.request.cookies.get(cookie_name)
        return cookie_val and Secure.check_secure_val(cookie_val)

    def initialize(self, *a, **kw):
        """initialize the variables across the board"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user_cookie = uid and Users.get_id(int(uid))

class SignUp(Cookies):
    """SignUp class is responsible for allowing the user to
       signup.
    """
    def get(self):
        self.errors()

    def errors(self, name="", name_error="", passwd_error="", passwd2_error="", email_error=""):
        self.render("/signup.html", username=name, name_error=name_error,
                    invalid_password=passwd_error, 
                    verify_password=passwd2_error,
                    invalid_email=email_error)

    def post(self):
        """retreive the responses from the user"""

        self.user_name = Secure.valid_username(self.request.get('username'))
        self.passwd    = Secure.valid_passwd(self.request.get('password'))
        self.email     = self.request.get('email')

        if not (self.user_name and self.passwd):
            msg  = "username cannot be empty"
            msg2 = "password cannot be empty"
            self.errors(name_error=msg, passwd_error=msg2)
        else:
            if self.passwd.group() != self.request.get('verify'):
                msg = "Password do not match"
                self.errors(name=self.user_name.group(), passwd_error=msg, passwd2_error=msg)
            else:

                if self.email and not Secure.valid_email(self.request.get('email')):
                    self.errors(name=self.user_name.group(), email_error="email incorrect format")
                elif self.email:
                    self.done()
                else:
                    self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(SignUp):
    """Register class registers the user"""

    def done(self):

        username = self.user_name.group().lower()
        
        # Check if user already exists.
        if Users.by_name(username):
            self.errors(name_error="User already exists")
        else:

            password = self.passwd.group()
            email = None 

            if self.email:
                email = self.email

            # hash the password before storing in database
            passwd_hash = Secure.make_salt_password(username, password)
        
            # Add the user, hashed password or email to the database
            usr_obj = Users.add(username, passwd_hash, email)
            cookie_val = self.make_cookie(str(usr_obj.key().id()))
            self.set_cookie('user_id', cookie_val)
            self.redirect('/blog/newpost')
    
class LogIn(Cookies):
    """This class is responsible for allowing user to log in"""

    def error(self, invalid_name=""):
        self.render('/login.html', invalid_login=invalid_name)

    def get(self):
        self.render('/login.html')
        
    def login(self, user, password):

        # Takes a user and a password checks if it is correct. 
        # If so stores it in google appengine db and uses the 
        # obj id returned from the database as cookie val
        usr_obj = Secure.check_passwd(user.lower(), password, Users) # takes str, str, obj (google appengine)
        if usr_obj:
            cookie_val = self.make_cookie(str(usr_obj.key().id())) # get the int val for the val
            self.set_cookie('user_id', cookie_val)
            self.redirect('/blog/newpost')
            
        else:
            self.error("Invalid login")
        
    def post(self):
        self.user = self.request.get('username')
        self.passwd = self.request.get('password')
        self.login(self.user, self.passwd)

class LogOut(Cookies):
    """The LogOut deals with the issue of logging the user out"""

    def logout(self):
        """allows the user to logout"""
        self.delete_cookie('user_id')

    def get(self):
        self.logout()   
        self.redirect("/login")
        
class NewPost(Cookies):
    """The class is responsible for allowing the user
    to make new posts
    """

    def get(self):

        # check if the user has a cookie before redirecting to newpost page
        # or redirecting to the login page
        if self.user_cookie:
            self.render('/newpost.html', user=self.user_cookie)
        else:
            self.redirect('/login')

    def post(self):

        subject = self.request.get('subject')
        blog    = self.request.get('blog')

        if not subject and not blog:
            self.render("newpost.html", error="please enter a subject and a body.", user=self.user_cookie)
        elif not subject and blog:
            self.render("newpost.html", body=blog, body_err="Looks like you have forgotten the subject!",
                         user=self.user_cookie)
        elif subject and not blog:
            self.render("newpost.html", subject=subject, blog_err="Enter the blog content.", user=self.user_cookie)
        else:
            uid = PostsDb.add(subject, blog)       # add the latest blog to the database
            self.redirect('/blog/%s'%(str(uid)))   # redirect it to a permalink

class Posts(Cookies):
    """The class posts the newest link to a permalink"""

    def get(self, post_uid):

        post_obj = PostsDb.find_path(post_uid) # find the path of post

        if not post_obj:
            self.render('404')
        else:

            # check it there is a user cookie
            if self.user_cookie:
                self.render('/permalink.html', post=post_obj, user=self.user_cookie)

class Blog(Cookies):

    def get(self):
        if self.user_cookie:
            posts = PostsDb.get_all()
            self.render('/posts.html', user=self.user_cookie, posts=posts)
        else:
            self.redirect("/login")

class JsonAllPosts(Cookies):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        
        if not self.user_cookie:
            self.redirect("/login")
        else:
            post_obj = PostsDb.get_all()
            json_post = Json()

            for post in post_obj:
                sub  = post.subject
                cont = post.content
                created = post.created.strftime("%b %d, %Y")
                last_time = post.last_created.strftime("%b %d, %Y")

                json_post.set_variables(sub, cont, created, last_time)
                json_post.make_json_str()

            self.write(json_post.get_json())

class JsonPermalink(Cookies):

    def get(self, uid):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        
        if not self.user_cookie:
            self.redirect("/login")
        else:
            post_obj = PostsDb.find_path(uid)
            json_post = Json()

            sub  = post_obj.subject
            cont = post_obj.content
            created = post_obj.created.strftime("%b %d, %Y")
            last_time = post_obj.last_created.strftime("%b %d, %Y")

            json_post.set_variables(sub, cont, created, last_time)
            json_post.make_json_str()
            self.write(json_post.get_json())
                
app = webapp2.WSGIApplication([('/signup', Register),
                                ('/login', LogIn),
                                ('/logout', LogOut),
                                ('/blog/newpost', NewPost),
                                ('/blog/(\d+)', Posts),
                                ('/blog/?', Blog),
                                ('/blog.json', JsonAllPosts),
                                ('/blog/(\d+).json', JsonPermalink)],
                                debug=True)

