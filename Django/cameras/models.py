from django.db import models
import string
import random



def key_generator():
	size=15
	chars=string.ascii_uppercase + string.digits+string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))
# Create your models here.


class Camera(models.Model):
	name = models.CharField(max_length=100)
	key = models.CharField(max_length=100,default=key_generator())

	def __unicode__(self):
		return self.name
