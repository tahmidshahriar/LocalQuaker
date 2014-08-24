from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=4, unique=True)
    views = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
class Sell(models.Model):
    subject = models.ForeignKey(Subject)
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    book = models.CharField(max_length=128)
    course = models.IntegerField(default=0)
    userid = models.IntegerField(default=0)
    email = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now= True)
    price = models.IntegerField(default = 0)
    url = models.CharField(max_length=128)
    subjurl = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='Sell')
    def __unicode__(self):
        return self.name

class TicketSell(models.Model):
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    ticket = models.CharField(max_length=128)
    userid = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now= True)
    description = models.TextField()    
    price = models.IntegerField(default = 0)
    url = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='Ticket')
    def __unicode__(self):
        return self.ticket
    
class HouseholdSell(models.Model):
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    item = models.CharField(max_length=128)
    userid = models.CharField(max_length=128)
    description = models.TextField()
    time = models.DateTimeField(auto_now= True)
    price = models.IntegerField(default = 0)
    url = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='Household')
    def __unicode__(self):
        return self.item
 
class Term(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
class SubletsSell(models.Model):
    term = models.ForeignKey(Term)
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    userid = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now= True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.IntegerField(default = 0)
    url = models.CharField(max_length=128)
    termurl = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='Sublet')
    def __unicode__(self):
        return self.title
    
class Other(models.Model):
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    userid = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now= True)
    description = models.TextField()
    title = models.CharField(max_length=128)
    price = models.IntegerField(default = 0)
    url = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='Other')
    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)

    def __unicode__(self):
        return self.user.username
