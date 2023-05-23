from django.shortcuts import render
from todo.models import Todo
from django.http import HttpResponse
from datetime import datetime
import json


def todos_api(request):
    todo_list = []

    try:
        todos = Todo.objects.all()
        for todo in todos:
            todo_data = {
                'id': todo.id,
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
