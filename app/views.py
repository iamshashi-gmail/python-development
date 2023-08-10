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

auth = ('awxusername', 'awxpassword')
host_ip = "http://awxhostip"

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
