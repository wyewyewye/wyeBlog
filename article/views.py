from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from .models import ArticlePost
from .form import ArticlePostForm
from django.contrib.auth.models import User

import markdown

def print_request(req):
    print(f"""
        request method:{req.method}, headers: {req.headers}, body: {req.body}       
    """)

# Create your views here.
# @csrf_exempt
@require_http_methods(['GET'])
def article_list(request):
    print_request(request)
    articles = ArticlePost.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'article/list.html', context)

@require_http_methods(['GET', 'POST'])
def article_detail(request, id):
    print_request(request)
    if id <= 0:
        return HttpResponseNotFound()
    try:
        article = ArticlePost.objects.get(id=id)
    except Exception as e:
        return HttpResponseNotFound()
    text = article.body
    article.body = markdown.markdown(text,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
    context = {'article': article}
    return render(request, 'article/detail.html', context)

@require_http_methods(['GET', 'POST'])
def article_create(request):
    print_request(request)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse('表单内容有误，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)
    
@require_http_methods(['POST'])
def article_delete(request, id):
    print_request(request)
    if request.POST.get('password', '') != 'wye123':
        return HttpResponseForbidden()
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect('article:article_list')

@require_http_methods(['GET', 'POST'])
def article_update(request, id):
    print_request(request)
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        post_user = request.user.name
        print(f'post user: {post_user}')
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
    
    return HttpResponseServerError()

def test404(request):
    return HttpResponseNotFound()