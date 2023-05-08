from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def user_profile(request):
    return render(request, './user/profile.html')


def user_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.POST.get('register'):
            return redirect('register')
        if request.POST.get('login'):
            if username == '' or password == '':
                message = '帳號或密碼不能為空!'
            else:
                user = authenticate(request,
                                    username=username,
                                    password=password)
                print(user)
                if user is None:
                    is_user = User.objects.filter(username=username)
                    print(is_user)
                    if not is_user:
                        message = '帳號錯誤!'
                    else:
                        message = '密碼錯誤!'
                else:
                    login(request, user)
                    message = '登入成功!'
                    redirect('profile')

    return render(request, './user/login.html', {'message': message, 'user': request.user})


def user_register(request):
    message = ''
    username = ''
    form = UserCreationForm()
    if request.method == 'GET':
        print('GET')

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(username, password1, password2)

            if len(password1) < 8:
                message = '密碼過短'
            elif password1 != password2:
                message = '兩次密碼不同'
            else:
                if User.objects.filter(username=username).exists():
                    message = '帳號重複'
                else:
                    User.objects.create_user(
                        username=username, password=password1).save()
                    message = '註冊成功!'
                #　帳號重複檢查
        except Exception as e:
            print(e)
            message = '註冊失敗'

    return render(request, 'user/register.html', {'form': form, 'message': message})
