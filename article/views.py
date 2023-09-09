from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from .models import ArticlePost

def print_request(req):
    print(f"""
        request method:{req.method}, headers: {req.headers}, body: {req.body}       
    """)

# Create your views here.
@csrf_exempt
@require_http_methods(['GET'])
def article_list(request):
    print_request(request)
    articles = ArticlePost.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'article/list.html', context)

@require_http_methods(['GET'])
def article_detail(request, id):
    print_request(request)
    if id <= 0 or id > ArticlePost.objects.count():
        return HttpResponseNotFound()
    article = ArticlePost.objects.get(id=id)
    context = {'article': article}
    return render(request, 'article/detail.html', context)

def test404(request):
    return HttpResponseNotFound()