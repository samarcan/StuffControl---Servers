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
from .models import Camera

@login_required()
def new_camera(request):
	profile = User_Profile.objects.get(user=request.user)

	return render(request,'new_camera.html',{'profile':profile})

@login_required()
def create_new_camera(request):
	profile = User_Profile.objects.get(user=request.user)

	if request.method == 'POST':
		POST = request.POST
		camera = Camera()
		camera.name = POST['name']
		camera.save()
		profile.cameras.add(camera)

		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/newthing')

@login_required()
def delete_camera(request,offset):
	camera_id = int(offset)
	camera = Camera.objects.get(id = camera_id)
	camera.delete()
	return HttpResponseRedirect('/')


@login_required()
def camera(request,id):
	camera_id = int(id)
	camera  = Camera.objects.get(id = camera_id)
	profile = User_Profile.objects.get(user=request.user)
	if camera in profile.cameras.all():
		return render(request,'camera.html',{'profile':profile,'camera':camera})
	else:
		return HttpResponseRedirect('/')

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def getcameras(request):
	profile = User_Profile.objects.get(user = request.user)
	data = []
	for camera in profile.cameras.all():
		elem = {'name':camera.name, 'key':camera.key}
		data.append(elem)

	return HttpResponse(json.dumps(data), content_type = "application/json")