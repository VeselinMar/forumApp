from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from forumApp.posts.forms import SearchForm, PostCreateForm, PostDeleteForm, PostEditForm
from forumApp.posts.models import Post


def index(request):

    context = {
        "my_form": "",
    }

    return render(request, 'posts/index.html', context)


def dashboard(request):
    form = SearchForm(request.GET)
    posts = Post.objects.all()

    if request.method == "GET":
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = posts.filter(title__icontains=query)

    no_posts = not posts.exists()

    context = {
        "posts": posts,
        "form": form,
        "no_posts": no_posts,
    }

    return render(request, 'posts/dashboard.html', context)


def add_post(request):
    form = PostCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('dash')

    context = {
        "form": form,
    }

    return render(request, 'posts/add-post.html', context)


def edit_post(request, pk: int):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('dash')

    else:
        form = PostEditForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }

    return render(request, 'posts/edit-post.html', context)


def details_post(request, pk: int):
    post = Post.objects.get(pk=pk)

    context = {
        "post": post
    }

    return render(request, 'posts/details-post.html', context)


def delete_post(request, pk: int):
    post = Post.objects.get(pk=pk)
    form = PostDeleteForm(instance=post)

    if request.method == "POST":
        post.delete()
        return redirect('dash')

    context = {
        "form": form,
        "post": post,
    }

    return render(request, 'posts/delete-template.html', context)
