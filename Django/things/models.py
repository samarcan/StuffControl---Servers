from django.db import models
import string
import random



def key_generator():
	size=15
	chars=string.ascii_uppercase + string.digits+string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))

# Create your models here.

class Value(models.Model):
	value = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True, blank=True)


class Controller(models.Model):


	identifier = models.CharField(max_length=100)
	value_range = models.CharField(max_length=100)
	log_control = models.ManyToManyField(Value,null=True,blank=True)

	def __unicode__(self):
		return self.identifier

	def get_last(self):
		try:
			return self.log_control.all().order_by('-id')[0]
		except IndexError:
			pass
		
class Sensor(models.Model):

	identifier = models.CharField(max_length=100)
	value_range = models.CharField(max_length=100)
	log_sensor = models.ManyToManyField(Value,null=True,blank=True)

	def __unicode__(self):
		return self.identifier



class Thing(models.Model):
	name = models.CharField(max_length=100)
	key = models.CharField(max_length=100,default=key_generator())
	controllers = models.ManyToManyField(Controller, null=True,blank=True)
	sensors = models.ManyToManyField(Sensor, null=True,blank=True)

	def __unicode__(self):
		return self.name

class AutomaticController(models.Model):

	sensorthing = models.ForeignKey(Thing ,related_name="sensor_%(app_label)s_%(class)s_related")
	sensor = models.ForeignKey(Sensor)
	value_range =models.CharField(max_length=100)
	controllerthing = models.ForeignKey(Thing,related_name="controller_%(app_label)s_%(class)s_related")
	controller = models.ForeignKey(Controller)
	value = models.CharField(max_length=100)
	active = models.BooleanField(default=True)

