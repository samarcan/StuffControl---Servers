from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import json
import requests



# Create your views here.

from userprofiles.models import User_Profile
from .models import Thing, Controller, Sensor, Value, AutomaticController


@login_required()
def new_thing(request):
	profile = User_Profile.objects.get(user=request.user)

	return render(request,'new_thing.html',{'profile':profile})

@login_required()
def create_new_thing(request):
	profile = User_Profile.objects.get(user=request.user)

	if request.method == 'POST':
		POST = request.POST
		thing = Thing()
		thing.name = POST['name']
		thing.save()
		profile.things.add(thing)

		for i in POST:
			print i
			print POST[i]
			if i.find('control_identifier') != -1:
				iden = i[19:]
				control = Controller()
				control.identifier = POST['control_identifier_'+iden]
				control.value_range = POST['control_range_'+iden]
				control.save()
				thing.controllers.add(control)
				control = None
			elif i.find('sensor_identifier') != -1:
				iden = i[18:]
				sensor = Sensor()
				sensor.identifier = POST['sensor_identifier_'+iden]
				sensor.value_range = POST['sensor_range_'+iden]
				sensor.save()
				thing.sensors.add(sensor)
				sensor = None

		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/newthing')

@login_required()
def delete_thing(request,offset):
	thing_id = int(offset)
	thing = Thing.objects.get(id = thing_id)
	for sensor in thing.sensors.all():
		sensor.delete()
	for control in thing.controllers.all():
		control.delete()
	thing.delete()
	return HttpResponseRedirect('/')


@login_required()
def thing(request,id):
	thing_id = int(id)
	thing  = Thing.objects.get(id = thing_id)
	profile = User_Profile.objects.get(user=request.user)
	if thing in profile.things.all():
		return render(request,'thing.html',{'profile':profile,'thing':thing})
	else:
		return HttpResponseRedirect('/')




@csrf_exempt
def order_controller(request):
	if request.method == 'POST':
		POST = request.POST
		key = POST['key']
		value = POST['value']
		identifier = POST['identifier']

		thing = Thing.objects.get(key = key)

		controller = Controller()

		for cont in thing.controllers.all():
			if cont.identifier == identifier:
				controller = Controller.objects.get(id = cont.id)
				break

		controller_value = Value()
		controller_value.value = value
		controller_value.save()
		controller.log_control.add(controller_value)

		data = {'key': key, 'identifier': identifier,'value':value}
		r = requests.post("http://localhost:8000/order_controller/", data=data)
		print r.text

	data = {}
	data['check'] = 'OK'
	return HttpResponse(json.dumps(data), content_type = "application/json")





@csrf_exempt
def sensor_value(request):
	if request.method == 'POST':
		POST = request.POST
		cont = len(POST)/3

		for i in range(cont):
			key = POST['key']
			value = POST['value']
			identifier = POST['identifier']
			print identifier

			int_value = int(round(float(value)))
			print int_value

			thing = Thing.objects.get(key = key)

			sensor = Sensor()

			for sens in thing.sensors.all():
				if sens.identifier == identifier:
					sensor = Sensor.objects.get(id = sens.id)
					break
			automatic_controll(sensor.id,key,int_value)
			sensor_value = Value()
			sensor_value.value = value
			sensor_value.save()
			sensor.log_sensor.add(sensor_value)

			#data = {'key': key, 'identifier': identifier,'value':value}
			#r = requests.post("http://localhost:8000/sensor_value/", data=data)
			#print r.text
	data = {}
	data['check'] = 'OK'
	return HttpResponse(json.dumps(data), content_type = "application/json")


def automatic_controll(sensor,key,int_value):

	profile = User_Profile()
	for prof in User_Profile.objects.all():
		for thing in prof.things.all():
			if thing.key == key:
				profile = prof
	sensor = int(sensor)
	for automatic in profile.automaticcontrollers.all():
		if automatic.sensor.id == sensor and automatic.active:
			minim = int(automatic.value_range.split('-')[0])
			maxim = int(automatic.value_range.split('-')[1])
			
			print minim
			print maxim
			print int_value
			print sensor
			print int_value

			if (int_value <= maxim) and (int_value >=minim):
				key = automatic.controllerthing.key
				identifier = automatic.controller.identifier

				thing = Thing.objects.get(key = key)

				controller = Controller()

				for cont in thing.controllers.all():
					if cont.identifier == identifier:
						controller = Controller.objects.get(id = cont.id)
						break

				controller_value = Value()
				controller_value.value = automatic.value
				controller_value.save()
				controller.log_control.add(controller_value)

				data = {'key': key, 'identifier': identifier,'value':automatic.value}
				print "CONTROL AUTOMATICO"
				r = requests.post("http://localhost:8000/order_controller/", data=data)
				print r



@csrf_exempt
def add_automaticcontroller(request):
	if request.method == 'POST':
		profile = User_Profile.objects.get(user=request.user)
		automaticcontroller = AutomaticController()


		POST = request.POST
		for i in POST:
			print i+"    "+POST[i]
		automaticcontroller.sensorthing = Thing.objects.get(id = POST['thingsensor'])
		automaticcontroller.sensor = Sensor.objects.get(id = POST['sensor'])
		automaticcontroller.controllerthing = Thing.objects.get(id = POST['thingcontroller'])
		automaticcontroller.controller = Controller.objects.get(id = POST['controller'])
		automaticcontroller.value_range = POST['range']
		automaticcontroller.value = POST['value']

		automaticcontroller.save()

		profile.automaticcontrollers.add(automaticcontroller)

		lista=[]
		for automatic in profile.automaticcontrollers.all():
			dic={}
			dic['id'] = automatic.id
			dic['sensorthing_id']= automatic.sensorthing.id
			dic['sensorthing_name']= automatic.sensorthing.name
			dic['sensor_id']= automatic.sensor.id
			dic['sensor_name']= automatic.sensor.identifier
			dic['controllerthing_id'] = automatic.controllerthing.id
			dic['controllerthing_name'] = automatic.controllerthing.name
			dic['controller_id'] = automatic.controller.id
			dic['controller_name'] = automatic.controller.identifier
			dic['range']= automatic.value_range
			dic['value']= automatic.value
			dic['active'] = automatic.active

			lista.append(dic)

		return HttpResponse(json.dumps(lista), content_type="application/json")


	data = {}
	data['check'] = 'Error'
	return HttpResponse(json.dumps(data), content_type = "application/json")


def get_automaticcontroller(request):
	profile = User_Profile.objects.get(user=request.user)
	lista=[]
	for automatic in profile.automaticcontrollers.all():
		dic={}
		dic['id'] = automatic.id
		dic['sensorthing_id']= automatic.sensorthing.id
		dic['sensorthing_name']= automatic.sensorthing.name
		dic['sensor_id']= automatic.sensor.id
		dic['sensor_name']= automatic.sensor.identifier
		dic['controllerthing_id'] = automatic.controllerthing.id
		dic['controllerthing_name'] = automatic.controllerthing.name
		dic['controller_id'] = automatic.controller.id
		dic['controller_name'] = automatic.controller.identifier
		dic['range']= automatic.value_range
		dic['value']= automatic.value
		dic['active'] = automatic.active

		lista.append(dic)

	return HttpResponse(json.dumps(lista), content_type="application/json")


def change_check(request,value,ident):
	ident = int(ident)
	print value
	print ident

	automatic = AutomaticController.objects.get(id = ident)
	if value == '1':
		automatic.active = True
	elif value == '0':
		automatic.active = False

	automatic.save()

	data = {}
	data['check'] = automatic.active
	return HttpResponse(json.dumps(data), content_type = "application/json")


def delete_automatic(request,offset):
	automatic_id = int(offset)
	automatic = AutomaticController.objects.get(id = automatic_id)
	automatic.delete()
	data = {}
	data['check'] = 'OK'
	return HttpResponse(json.dumps(data), content_type = "application/json")


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def getthings(request):
	profile = User_Profile.objects.get(user = request.user)
	data = []
	for thing in profile.things.all():
		controllers = []
		sensors = []
		for controller in thing.controllers.all():
			controllers.append(controller.identifier)
		for sensor in thing.sensors.all():
			sensors.append(sensor.identifier)
		elem = {'name' : thing.name,
				'key' : thing.key,
				'sensors' : sensors,
				'controllers' : controllers,
				}
		data.append(elem)

	return HttpResponse(json.dumps(data), content_type = "application/json")

