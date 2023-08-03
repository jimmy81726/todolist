from django.shortcuts import render,redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import json
from django.http import JsonResponse,HttpResponse
from .models import Todo


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
    



# Create your views here.
@login_required
def comoleted_todo(request,id):
    todo=Todo.objects.get(pk=id)
    todo.completed=True
    todo.date_completed=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    todo.save()

    return redirect('todolist')


@login_required
def delete_todo(request,id):
    todo=Todo.objects.get(pk=id)
    todo.delete()

    return redirect('todolist')

@login_required
def completed_todolist(request):
    todos=None
    user=request.user
    if user.is_authenticated:
        todos=Todo.objects.filter(user=user).order_by('-date_completed')

    return render(request,'todo/completed_todo.html',{'todos':todos})

@login_required
def create_todo(request):
    message=''
    form=TodoForm()
    try:
        if request.method=='POST':
            print(request.POST)
            form=TodoForm(request.POST)
            todo=form.save(commit=False)
            if todo.completed:
                todo.date_completed=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            todo.user=request.user        
            todo.save()
            #message='建立todo成功!'
            return redirect('todolist')
    except Exception as e:
        print(e)
        message='建立todo失敗!'

    return render(request,'todo/create_todo.html',{'form':form,'message':message})

@login_required
def todo(request,id):
    todo,form=None,None    
    message=''
    try:
        todo=Todo.objects.get(id=id)
        # 只能檢視自己的代辦事項
        if todo.user.id!=request.user.id:
             todo=None                 

        elif request.method=='GET':          
            # 將取得的todo實例給表單
            form=TodoForm(instance=todo)

        elif request.method=='POST':
            if request.POST.get('update'):
                form=TodoForm(request.POST,instance=todo)
                if form.is_valid():                  
                    todo=form.save(commit=False)
                    if todo.completed:
                        todo.date_completed=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    todo.user=request.user
                    todo.save()  
                    message='更新成功!'       
            if request.POST.get('delete'):                 
                todo.delete()
                return redirect('todolist')
                         

    except Exception as e:
        print(e)
        if request.method=='POST':
            message='更新失敗!'
    return render(request,'todo/todo.html',{'todo':todo,'form':form,'message':message})

@login_required
def todolist(request):
    todos=None
    user=request.user
    if user.is_authenticated:
        todos=Todo.objects.filter(user=user).order_by('-created')

    return render(request,'todo/todolist.html',{'todos':todos})