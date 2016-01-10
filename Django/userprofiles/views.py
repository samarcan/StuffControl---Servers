from django.shortcuts import render
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
import json
import requests


# Create your views here.
from .forms import UserCreationEmailForm, EmailAuthenticationForm, UserProfileCreationForm
from .models import User_Profile
from things.models import *
from cameras.models import *



def entry(request):
	user_form = UserCreationEmailForm(request.POST or None)
	profile_form = UserProfileCreationForm(request.POST,request.FILES or None)
	signin_form = EmailAuthenticationForm(request.POST or None)
	
	if user_form.is_valid() and profile_form.is_valid():
		profile_form.save(user_form.save())
		return HttpResponseRedirect('/signin')

	if signin_form.is_valid():
		login(request,signin_form.get_user())
		return HttpResponseRedirect('/')

	return render(request, 'entry.html', {'user_form': user_form,'profile_form':profile_form,'signin_form':signin_form})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/entry')



@login_required()
def home(request):
	profile = User_Profile.objects.get(user=request.user)

	return render(request,'home.html',{'profile':profile})


@csrf_exempt
def Rest_Login(request):
	if request.method == "OPTIONS": 
		response = HttpResponse()
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		response['Access-Control-Max-Age'] = 1000
		# note that '*' is not valid for Access-Control-Allow-Headers
		response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
		return response

	if request.method == "POST":

		requestJsonData = bytes.decode(request.body)
		requestData = json.loads(requestJsonData)
		user_cache = authenticate(username=requestData['username'],password=requestData["password"])
		data = {}

		if not user_cache is None:
			data['token'] = Token.objects.get(user=user_cache).key
			data['username'] = user_cache.username
		else:
			data['success'] =False
		return HttpResponse(json.dumps(data), content_type = "application/json")


@api_view(['GET', 'OPTIONS',])
def Rest_Get_Things(request):
	if request.method == "OPTIONS": 
		response = HttpResponse()
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		response['Access-Control-Max-Age'] = 1000
		# note that '*' is not valid for Access-Control-Allow-Headers
		response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
		return response

	if request.method == "GET": 
		user = TokenAuth(request)
		if not user is None:
			profile = User_Profile.objects.get(user = user)
			data = []
			for thing in profile.things.all():
				data.append({
					'id': thing.id,
					'name': thing.name,
					'key': thing .key, 
					})
			print data
			return HttpResponse(json.dumps(data), content_type = "application/json")
		return HttpResponse(json.dumps({'success': False}), content_type = "application/json")

@api_view(['GET', 'OPTIONS',])
def Rest_Get_Thing_Elements(request, id):
	if request.method == "OPTIONS": 
		response = HttpResponse()
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		response['Access-Control-Max-Age'] = 1000
		# note that '*' is not valid for Access-Control-Allow-Headers
		response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
		return response

	if request.method == "GET": 
		user = TokenAuth(request)
		if not user is None:
			profile = User_Profile.objects.get(user = user)
			thing = Thing.objects.get(id = int(id))
			if thing in profile.things.all():
				data = {
					'id': thing.id,
					'name': thing.name,
					'key': thing.key,
					'controllers': [{'id': controller.id, 'identifier': controller.identifier} for controller in thing.controllers.all()],
					'sensors': [{'id': sensor.id, 'identifier': sensor.identifier} for sensor in thing.sensors.all()],
				}
				return HttpResponse(json.dumps(data), content_type = "application/json")
		return HttpResponse(json.dumps({'success': False}), content_type = "application/json")



@api_view(['GET', 'OPTIONS',])
def Rest_Get_Cameras(request):

	if request.method == "OPTIONS": 
			response = HttpResponse()
			response['Access-Control-Allow-Origin'] = '*'
			response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
			response['Access-Control-Max-Age'] = 1000
			# note that '*' is not valid for Access-Control-Allow-Headers
			response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
			return response

	if request.method == "GET": 
		user = TokenAuth(request)
		if not user is None:
			profile = User_Profile.objects.get(user = user)
			data = []
			for camera in profile.cameras.all():
				data.append({
					'id': camera.id,
					'name': camera.name,
					'key': camera.key, 
					})
			print data
			return HttpResponse(json.dumps(data), content_type = "application/json")
		return HttpResponse(json.dumps({'success': False}), content_type = "application/json")

@api_view(['POST', 'OPTIONS',])
def rest_order_controller(request):
	if request.method == "OPTIONS": 
		response = HttpResponse()
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		response['Access-Control-Max-Age'] = 1000
		# note that '*' is not valid for Access-Control-Allow-Headers
		response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
		return response

	if request.method == 'POST':
		user = TokenAuth(request)
		if not user is None:
			profile = User_Profile.objects.get(user = user)
			requestJsonData = bytes.decode(request.body)
			requestData = json.loads(requestJsonData)
			print requestData
			key = requestData['key']
			value = requestData['value']
			identifier = requestData['identifier']
			thing = Thing.objects.get(key = key)

			if thing in profile.things.all():
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
				return HttpResponse(json.dumps({'success': True}), content_type = "application/json")
		return HttpResponse(json.dumps({'success': False}), content_type = "application/json")

def TokenAuth(request):
	token = request.META['HTTP_AUTHORIZATION'].split()[1]
	for tok in Token.objects.all():
		if tok.key == token:
			return tok.user
	return None