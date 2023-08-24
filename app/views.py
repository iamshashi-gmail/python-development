# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.shortcuts import render
import requests
from rest_framework.views import APIView

auth = ('awxusername', 'awxpassword')
host_ip = "http://awxhostip"

#first rest api to communicate with react ui
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        print(request.data)
        #todos = Todo.objects.filter(auto_increment_id = 1)
        todos = Todo.objects.all()
        print(todos)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'language': request.data.get('language')
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#end 

# Detailed Views Start
class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self,request, id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Todo.objects.get(auto_increment_id=id)
        except Todo.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request,id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        print('this values  ',request,id)
        todo_instance = self.get_object(request,id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(request,id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'language': request.data.get('language')
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(request,id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
#
@login_required(login_url="/login")
def home(request):
    apiurl = host_ip + '/api/v2/projects'
    r = requests.get(apiurl, auth=auth)
    data= r.json()
    print(data)
    return render(request, 'home.html', {'data':data})

def hellow(request):

    return HttpResponse('my first page')

@login_required(login_url="/login")
def executePlaybook(request):
    apiurl = host_ip + '/api/v2/job_templates/47/launch/'
    body = {
    "extra_vars": {
        "FS_MOUNTPOINT":"/var"
        }
    }
    response = requests.post(apiurl, json=body, auth= auth)
    postdata= response.json()
    urlobj = postdata['url']
    statusurl = host_ip + urlobj
    st = requests.get(statusurl, auth= auth)
    statusdata= st.json()
    updatedstatus = statusdata['status']
    return render(request, 'home.html', {'postdata':updatedstatus})

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


#code for upload files

def file_handler_upload(f,request):
    """this function is besically backend chunking function"""
    os.system("mkdir {1}/core/media/user_{0}".format(fine_username(request),os.getcwd()))
    with open('{2}/core/media/user_{0}/{1}'.format(fine_username(request),f.name,os.getcwd()),'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

# @ms_identity_web.login_required
def file_upload(request):
    request.user.username = fine_username(request)
    if request.method == "GET":
        return render(request,'file_upload.html')
    else:
        try:
            print("removing folder")
            os.system("rm -rf {1}/core/media/user_{0}".format(fine_username(request),os.getcwd()))
        except Exception as e:
            file_name_id = request.FILES.get('sql_file',None)
            file_handler_upload(file_name_id,request)
            return render(request,'file_upload.html')

# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
        
#         load_template      = request.path.split('/')[-1]
#         context['segment'] = load_template
        
#         html_template = loader.get_template( load_template )
#         return HttpResponse(html_template.render(context, request))
        
#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template( 'page-404.html' )
#         return HttpResponse(html_template.render(context, request))

#     except:
    
#         html_template = loader.get_template( 'page-500.html' )
#         return HttpResponse(html_template.render(context, request))
