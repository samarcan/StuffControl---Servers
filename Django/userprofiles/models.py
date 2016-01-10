from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
from things.models import Thing, AutomaticController
from cameras.models import Camera


class User_Profile(models.Model):
	user = models.OneToOneField(User)
	image = models.ImageField(upload_to='image_profile',null=True, blank = True)
	things = models.ManyToManyField(Thing,null=True, blank=True)
	cameras = models.ManyToManyField(Camera,null=True, blank=True)
	automaticcontrollers = models.ManyToManyField(AutomaticController,null=True,blank=True)

	def __unicode__(self):
		return self.user.username