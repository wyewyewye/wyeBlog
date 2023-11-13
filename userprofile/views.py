from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .form import UserLoginForm

# Create your views here.

@require_http_methods(['GET', 'POST'])
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('用户名或密码错误')
        else:
            return HttpResponse('用户登录表单错误')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请求方式错误')
    
def user_logout(request):
    logout(request)
    return redirect('article:article_list')