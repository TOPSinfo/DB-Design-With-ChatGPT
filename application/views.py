import requests, json, os
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from .openai_helper import *
from AuthApp.costum_decorator import is_logged_in
from .models import Projects

@is_logged_in
def home_view(request):
    context = {}
    projects = None

    projects = Projects.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(projects, 5)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context['data'] = projects
    return render(request, 'home.html', context=context)

def add_project_data(project_title, project_feature, id, file_type, user, content):
    try:
        if(id):
            project = Projects.objects.get(id = id)
            project.project_title = project_title
            project.project_feature = project_feature
            project.save()
            return id, project
        else:
            project = Projects(
                project_title = project_title,
                project_feature = project_feature,
                file_type = file_type,
                user = user,
                response = content
            )
            project.save()
            return project.pk, project
    except IntegrityError:
        return -1, 0
    except Exception as ex:
        return 0, 0
    
def generate_output_file(file_type, project_response, project_title):
    res = None

    if file_type == 'excel':
        res = myExcl({})
        response = HttpResponse(res)
        response['Content-Disposition'] = f'attachment; filename={project_title}.xlsx'
        return response
    elif file_type == 'sql':
        res = myExcl({}, True)
        response = HttpResponse(res)
        response['Content-Disposition'] = f'attachment; filename={project_title}.sql'
        return response
    else:
        return None    

@is_logged_in
def project_feature_add_view(request):
    response = {}
    if request.method == 'POST':
        project_title = request.POST.get('project_title')
        project_feature = request.POST.get('project_feature')
        if("project_id" in request.POST):
            project_id = request.POST.get('project_id')
        else:
            project_id = None
        
        try:
            project_created, project = add_project_data(project_title, project_feature, project_id, 'json', request.user, '')
            
            if project_created == 0:
                response = {
                    'status': False,
                    'message': "Something went wrong!",
                    'data': []
                }
                return JsonResponse(response, safe=False)
            elif project_created == -1:
                response = {
                    'status': False,
                    'message': "Duplicate title exists!",
                    'data': []
                }
                return JsonResponse(response, safe=False)
            else:
                res = myJson({
                    'project_title': project_title,
                    'project_feature': project_feature
                })
                project.response = json.dumps(res)
                project.save()
                response = {
                    'status': True,
                    'message': "Response generated successfully!",
                    'data': res,
                    'project_id': project_created
                }
                return JsonResponse(response, safe=False)
        except Exception as e:
            response = {
                'status': False,
                'message': "Something went wrong!",
                'data': [],
                'project_id': 0
            }
            return JsonResponse(response, safe=False)
    
    return render(request, 'project_details_add.html')

@is_logged_in
def edit_view(request, id):
    context = {}
    project = None

    try:
        project = Projects.objects.get(id=id)
    except Projects.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('application:home')
    
    if request.method == 'POST':
        project_title = request.POST.get('project_title')
        project_feature = request.POST.get('project_feature')

        try:
            res = myJson({
                'project_title': project_title,
                'project_feature': project_feature
            })

            project.project_title = project_title
            project.project_feature = project_feature
            project.save()

            response = {
                'status': True,
                'message': "Response generated successfully!",
                'data': res,
            }
            return JsonResponse(response, safe=False)
        except Exception as e:
            response = {
                'status': False,
                'message': "Something went wrong!",
                'data': []
            }
            return JsonResponse(response, safe=False)

    context['project'] = project
    return render(request, 'project_details_edit.html', context)

@is_logged_in
def delete_view(request, id):
    try:
        project = Projects.objects.get(id=id)
    except Projects.DoesNotExist:
        messages.error(request, 'Project not found')
        return redirect('application:home')
    
    project.delete()
    messages.success(request, 'Project deleted')
    return redirect('application:home')

@csrf_exempt
@is_logged_in
def download_view(request):
    response = {}
    projectId = None
    myProject = {}

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    file_type = body['file_type']
    
    try:
        projectId = body['project_id']
        myProject = Projects.objects.get(id = projectId)
    except:
        pass

    res = None
    
    if(file_type == 'json_excel' and "pure_json" in body.keys()):
        res = jsonToExcel({
            "title": 'title',
            "json_obj": body['pure_json']
        })
    elif(file_type == 'json_sql' and "pure_json" in body.keys()):
        res = jsonToSql({
            "title": 'title',
            "json_obj": body['pure_json']
        })
    elif(file_type == 'json_p_models' and "pure_json" in body.keys()):
        res = jsonToPythonModels({
            "json_obj": body['pure_json']
        })
    elif(file_type == 'json_s_models' and "pure_json" in body.keys()):
        res = jsonToSequelizeModels({
            "json_obj": body['pure_json']
        })
    elif(file_type == "excel"):
        res = jsonToExcel({
            "title": 'title',
            "json_obj": myProject.response
        })
    elif(file_type == "json"):
        res = jsonToExcel({
            "title": 'title',
            "json_obj": myProject.response
        })
    else:
        res = jsonToSql({
            "title": 'title',
            "json_obj": myProject.response
        })
        
    if(res):
        return HttpResponse(res)
    else:
        return JsonResponse({"success": False, "message": "Something went wrong.!"})
  
@is_logged_in
def correctDB_view(request):
    if(request.method == "POST"):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        SQL_Content = body['sql_file']
        Feature_Changes = body['feature_change']
        
        if("feature_change" not in body.keys()):
            return JsonResponse({"success": False, "message": "Feature Changes are required"}, safe=False)

        AIData = correctExistingDB({
            "sql_file": SQL_Content,
            "feature_change": Feature_Changes
        })
        
        return HttpResponse(AIData)
    else:
        return render(request, 'correct_db.html')

@is_logged_in
def save_response(request):
    try:
        if(request.method == "POST"):
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            content = body['content']
            p = Projects.objects.get(id = body['project_id'])
            p.response = json.dumps(content)
            p.save()
            
            return JsonResponse({'success': True, 'message': "Data saved"})
    except Exception as ex:
        return JsonResponse({'success': False, 'message': str(ex)})