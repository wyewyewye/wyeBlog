from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import ArticlePost

# Create your views here.
def article_list(request):
    articles = ArticlePost.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'article/article_list.html', context)

def test404(request):
    return HttpResponseNotFound()