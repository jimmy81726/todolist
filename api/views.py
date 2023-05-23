from django.shortcuts import render
from todo.models import Todo
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from datetime import datetime

# 取得單一使用者所有代辦事項
def user_todos_api(request,id):
    todo_list = []  
    result='success'
    user=None
    try:
        user=User.objects.get(pk=id)
        todos=Todo.objects.filter(user=user)
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'title':todo.title,
                'text': todo.text,
                'important': todo.important,
                'completed': todo.completed,
                'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_completed': todo.date_completed.strftime('%Y-%m-%d %H:%M:%S')
                if todo.completed else None,
                'user': todo.user.username
            }

            todo_list.append(todo_data)
        print(todo_list)
        user=user.username
    except Exception as e:
        print(e)
        result='error'

    json_data= json.dumps({
      'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),        
      'result':result,
      'user':user,
      'data':todo_list
      },ensure_ascii=False)

    return HttpResponse(json_data, content_type='application/json')
  


# 取得所有代辦事項
def todos_api(request):
    todo_list = []
    try:
        todos = Todo.objects.all()
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'title':todo.title,
                'text': todo.text,
                'important': todo.important,
                'completed': todo.completed,
                'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_completed': todo.date_completed.strftime('%Y-%m-%d %H:%M:%S')
                if todo.completed else None,
                'user': todo.user.username
            }

            todo_list.append(todo_data)
        print(todo_list)
    except Exception as e:
        print(e)

    todo_list = json.dumps(todo_list, ensure_ascii=False)

    return HttpResponse(todo_list, content_type='application/json')


# 取得單一代辦事項
def todo_api(request,id):
    todo_data={}
    result='success'
    try:
        todo=Todo.objects.get(id=id)
        todo_data = {
                'id': todo.id,
                'title':todo.title,
                'text': todo.text,
                'important': todo.important,
                'completed': todo.completed,
                'created': todo.created.strftime('%Y-%m-%d %H:%M:%S'),
                'date_completed': todo.date_completed.strftime('%Y-%m-%d %H:%M:%S')
                if todo.completed else None,
                'user': todo.user.username
            }

    except Exception as e:
        print(e)
        result='error'
        
    json_data= json.dumps({
        'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),        
        'result':result,
        'data':todo_data
        },ensure_ascii=False)

    return HttpResponse(json_data, content_type='application/json')