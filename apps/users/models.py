from django.db import models
import re, bcrypt, datetime
from datetime import date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PSWD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$')

class ShowManager(models.Manager):
    def register_validator(self, postData):
        errors={}
        if len(postData['first_name']) < 2:
            errors['first_name_error'] = "At least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name_error'] = "At least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_error'] = "Not a valid email address"
        if self.filter(email=postData['email']):
            errors['email_error'] = "Email already exists"
        if not PSWD_REGEX.match(postData['password']):
            errors['password_error'] = "Not a valid password"
        if postData['password'] != postData['conf_pswd']:
            errors['conf_pswd_error'] = "Confirmation Password doesn't match Password"
        return errors

    def register_user(self, postData):
        hashed_pswd = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_pswd
        ).id

    def login_validator(self, postData):
        errors={}
        exists = self.filter(email=postData['email'])
        if not exists:
            errors['login_email_error'] = "Email does not exist"
            return errors
        if not bcrypt.checkpw(postData['password'].encode(), exists[0].password.encode()):
            errors['login_pswd_error'] = "Password does not match"
            return errors
        return errors
    
    def hash_id(self, uid):
        return bcrypt.hashpw(str(uid).encode(), bcrypt.gensalt())

    # def user_validator(self, uid, hashed_uid):
    #     return bcrypt.checkpw(uid.encode(), hashed_uid.encode())

    def get_user_info(self, uid):
        return self.get(id=uid)

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()