"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [  
    path('todos/', views.todos_api, name='api-todos'),
    path('todos/<int:id>', views.todo_api, name='api-todo'),
    path('todos/user/<int:user_id>/',
         views.user_todos_api, name='api-user-todos'),
    path('users/',views.users_api,name='api-users'),
    path('users/<int:id>',views.user_api,name='api-user')
    

]
