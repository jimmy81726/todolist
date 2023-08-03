from django.shortcuts import render
from todo.models import Todo
from django.contrib.auth.models import User
# Create your views here.
from django.http import JsonResponse,HttpResponse
import json


def user_api(request,id):
    user_data = {}
    try:
        user = User.objects.get(pk=id)       
        if user is not None: 
            user_data = {
                'id': user.id,
                'username': user.username,         
                'password':user.password,  
                'is_superuser':user.is_superuser,  
                'user.last_login':user.last_login.strftime('%Y-%m-%d \
                                                           %H:%M:%S:%f')
            }
    except Exception as e:
        print(e)
        
    user_data = json.dumps(user_data, ensure_ascii=False)
      
    return HttpResponse(user_data,content_type='application/json')

def users_api(request):
    user_list = {}
    datas=[]
    try:
        users = User.objects.all()      
        for user in users:
            data = {
                'id': user.id,
                'username': user.username,         
                'password':user.password,  
                'is_superuser':user.is_superuser,  
                'user.last_login':user.last_login.strftime('%Y-%m-%d \
                                                           %H:%M:%S:%f')
            }
            print(user.last_login,type(user.last_login))
            datas.append(data)
    except Exception as e:
        print(e)
          
    user_list['total']=len(users)
    user_list['result']=datas
    
    datas = json.dumps(user_list, ensure_ascii=False)
      
    return HttpResponse(datas,content_type='application/json')



def user_todos_api(request, user_id):
    todo_list = []
    try:
        user = User.objects.get(id=user_id)
        todos = Todo.objects.filter(user=user)        
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'title': todo.title,
                'text': todo.text,
                'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_completed': todo.date_completed.strftime('%Y-%m-%d %H:%M:%S') if todo.date_completed else None,
                'important': todo.important,
                'completed': todo.completed,
                'user': todo.user.username,
            }
            todo_list.append(todo_data)
    except Exception as e:
        print(e)
          
    todo_data = json.dumps(todo_list, ensure_ascii=False)
      
    return HttpResponse(todo_data,content_type='application/json')


def todo_api(request,id):
    todo_data = {}
    try:
        todo = Todo.objects.get(pk=id)       
        if todo is not None: 
            todo_data = {
                'id': todo.id,
                'title': todo.title,
                'text': todo.text,
                'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_completed': todo.date_completed.strftime('%Y-%m-%d %H:%M:%S') if todo.date_completed else None,
                'important': todo.important,
                'completed': todo.completed,
                'user': todo.user.username,
            }
    except Exception as e:
        print(e)
        
    todo_data = json.dumps(todo_data, ensure_ascii=False)
      
    return HttpResponse(todo_data,content_type='application/json')

def todos_api(request):
    todo_json=[]
    try:
        todos = Todo.objects.all()
        todo_list = []
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'title': todo.title,
                'text': todo.text,
                'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_completed': todo.date_completed.strftime('%Y-%m-%d %H:%M:%S') if todo.completed else None,
                'important': todo.important,
                'completed': todo.completed,
                'user': todo.user.username,
            }
            todo_list.append(todo_data)
            
        todo_json = json.dumps(todo_list, ensure_ascii=False)
    except Exception as e:
        print(e)
    print(todo_json)
    return HttpResponse(todo_json,content_type='application/json')
    



