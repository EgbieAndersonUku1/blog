
import hmac
from string import letters
from random import shuffle
from generate_secret_key import load_secret_key
import hashlib
import re
import os

SECRET = load_secret_key()

class Secure(object):
        """Verifies whether the values entered by the user is correct"""

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWD  = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        EMAIL   = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

        @classmethod
        def valid_username(cls, username):
                """validates the username"""
                return cls.USER_RE.match(username)

        @classmethod
        def valid_passwd(cls, password):
                """validates the password"""
                return cls.PASSWD.match(password)

        @classmethod
        def valid_email(cls, email):
                """validates the email"""
                return cls.EMAIL.match(email)

        @classmethod
        def hash_str(cls, s):
                """hash_str(str) -> return(str)
                Returns a hash version of  a string
                """
                return hmac.new(SECRET, s).hexdigest()

        @classmethod
        def make_secure_val(cls, s):
                """make_secure_val(str) -> return(str)
                Creates a string in the form of str|hash
                """
                return "%s|%s" %(s, cls.hash_str(s))

        @classmethod
        def check_secure_val(cls, h):
                """check_secure_val(str) -> return(str)
                Takes a string and returns the val only if the hash matches
                the string
                """
                val = h.split('|')[0]
                if h == cls.make_secure_val(val):
                        return val

        @classmethod
        def make_salt_password(cls, name=None, password=None, salt=None, val=26):
                """make_salt_password(str, str, str) -> return(str)
                makes a password using salt
                """
                if not salt:
                        salt = cls.get_salt(26)
                passwd_hash = hashlib.sha256(name + password + salt).hexdigest()
                return "%s,%s" %(salt, passwd_hash)
                
                        
        @classmethod
        def get_salt(cls, val):
                """creates a salt to be used with a password"""
                if  0 < val <= 26 and type(val) == int:
                       letter_list = list(letters)
                       shuffle(letter_list)
                       return "".join(letter_list)[:val]

        @classmethod
        def check_passwd(cls, user, password, class_obj):
            """check_passwd(user, passwd, class) 
            Verifies whether the user password is valid"""
            
            user = class_obj.by_name(user) # gets the user name obj

            # if the users exists takes the user password and hashes it, compares it
            # to the hash password that exists in the database. If it is a match
            # returns a user object.
            if user:
                passwd = user.passwd_hash
                salt = passwd.split(',')[0]
                if cls.make_salt_password(user.user_name, password, salt) == passwd:
                  return user
                       
                               
                

