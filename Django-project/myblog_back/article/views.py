# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.urls import reverse

from article.forms import ArticleForm, CategoryForm
from article.models import Article, Category, Comment


def article(request):
    """文章"""
    if request.method == 'GET':
        # 当前管理员
        current_user = request.user
        articles = current_user.article_set.all()
        return render(request, 'article.html', {'articles': articles})

    if request.method == 'POST':
        """删除选中的文章"""
        article_ids = request.POST.getlist('checkbox[]')
        Article.objects.filter(id__in=article_ids).delete()
        return HttpResponseRedirect(reverse('article:article'))


def add_article(request):
    """添加文章"""
    if request.method == 'GET':
        categorys = Category.objects.all()
        return render(request, 'add-article.html', {'categorys': categorys})
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data['author'] = request.user
            Article.objects.create(**data)
            return HttpResponseRedirect(reverse('article:article'))
        else:
            categorys = Category.objects.all()
            return render(request, 'add-article.html', {'form': form, 'categorys': categorys})


def update_article(request, id):
    """修改文章"""
    if request.method == 'GET':
        article = Article.objects.filter(id=id).first()
        categorys = Category.objects.all()
        return render(request, 'update-article.html', {'article': article, 'categorys': categorys})
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Article.objects.filter(id=id).update(**data)

            return HttpResponseRedirect(reverse('article:article'))
        else:
            categorys = Category.objects.all()
            return render(request, 'update-article.html', {'form': form, 'categorys': categorys})


def delete_article(request):
    """删除文章"""
    if request.method == 'POST':
        id = request.POST.get('id')
        Article.objects.filter(id=id).delete()
        return JsonResponse({'code': 200})


def comment(request):
    """评论"""
    if request.method == 'GET':
        comments = Comment.objects.all()
        return render(request, 'comment.html', {'comments': comments})

    if request.method == 'POST':
        """删除选中的评论"""
        comment_ids = request.POST.getlist('checkbox[]')
        Comment.objects.filter(id__in=comment_ids).delete()
        return HttpResponseRedirect(reverse('article:comment'))


def category(request):
    """栏目"""
    if request.method == 'GET':
        categorys = Category.objects.all()
        return render(request, 'category.html', {'categorys': categorys})
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Category.objects.create(**data)
            return HttpResponseRedirect(reverse('article:category'))
        else:
            categorys = Category.objects.all()
            return render(request, 'category.html', {'categorys': categorys, 'form': form})


def category_delete(request):
    """删除指定的栏目"""
    if request.method == 'POST':
        id = request.POST.get('id')
        category = Category.objects.filter(pk=id).first()
        category.article_set.all().delete()
        category.delete()
        return JsonResponse({'code': 200})


def category_update(request, id):
    """修改栏目"""
    if request.method == 'GET':
        category = Category.objects.filter(pk=id).first()
        return render(request, 'update-category.html', {'category': category})
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Category.objects.filter(pk=id).update(**data)
            return HttpResponseRedirect(reverse('article:category'))
        else:
            categorys = Category.objects.all()
            return render(request, 'category.html', {'categorys': categorys, 'form': form})
