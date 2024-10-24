from django.core.paginator import Paginator
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView

from forumApp.posts.forms import SearchForm, PostCreateForm, PostDeleteForm, CommentCreateForm, \
    CommentEditForm
from forumApp.posts.models import Post, Comment


# index page as ClassBasedView
class IndexView(TemplateView):
    # static solution
    template_name = 'posts/index.html'

# index page FunctionBasedView
# def index(request):
#
#     context = {
#         "my_form": "",
#     }
#
#     return render(request, 'posts/index.html', context)


# dashboard as ClassBasedView
class DashboardView(ListView, FormView):
    template_name = 'posts/dashboard.html'
    context_object_name = 'posts'
    form_class = SearchForm
    success_url = reverse_lazy('dash')
    model = Post

    def get_queryset(self):
        queryset = self.model.objects.all()

        if 'query' in self.request.GET:
            query = self.request.GET.get('query')
            queryset = self.queryset.filter(title__icontains=query)

        return queryset


# post_view as a ClassBasedView
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/details-post.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        print(PostDetailView.__mro__)
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentCreateForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('details-post', pk=post.id)

        context = self.get_context_data()
        context['form'] = form

        return self.render_to_response(context)


# dashboard as a FunctionBasedView
# def dashboard(request):
#     form = SearchForm(request.GET)
#     posts = Post.objects.all()
#
#     if request.method == "GET":
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             posts = posts.filter(title__icontains=query)
#
#     no_posts = not posts.exists()
#
#     context = {
#         "posts": posts,
#         "form": form,
#         "no_posts": no_posts,
#     }
#
#     return render(request, 'posts/dashboard.html', context)


# add_post as ClassBasedView
class AddPostView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('dash')


# add_post as FunctionBasedView
# def add_post(request):
#     form = PostCreateForm(request.POST or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('dash')
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'posts/add-post.html', context)

# edit_post as a ClassBasedView
class EditPostView(UpdateView):
    model = Post
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('dash')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields=('title', 'content', 'author', 'languages'))
        else:
            return modelform_factory(Post, fields=('content',))

# edit_post as FunctionBasedView
# def edit_post(request, pk: int):
#     post = Post.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         form = PostEditForm(request.POST, instance=post)
#         if form.is_valid():
#             post.save()
#             return redirect('dash')
#
#     else:
#         form = PostEditForm(instance=post)
#     context = {
#         "form": form,
#         "post": post,
#     }
#
#     return render(request, 'posts/edit-post.html', context)


# post_details FunctionBasedView
# def details_post(request, pk: int):
#     post = Post.objects.get(pk=pk)
#     form = CommentCreateForm(request.POST or None)
#
#     if request.method == 'POST' and form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()
#         return redirect('details-post', pk=post.pk)
#
#     context = {
#         "post": post,
#         "form": form,
#     }
#
#     return render(request, 'posts/details-post.html', context)


# delete_post FunctionBasedView
# def delete_post(request, pk: int):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == "POST":
#         post.delete()
#         return redirect('dash')
#
#     context = {
#         "form": form,
#         "post": post,
#     }
#
#     return render(request, 'posts/delete-template.html', context)

# delete_post as ClassBasedView
class DeletePostView(DeleteView, FormView):
    model = Post
    form_class = PostDeleteForm
    template_name = 'posts/delete-template.html'
    success_url = reverse_lazy('dash')

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = Post.objects.get(pk=pk)
        return post.__dict__

# add_comment FunctionBasedView
# def add_comment(request, pk: int):
#     post = Post.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         form = CommentCreateForm(request.POST or None)
#
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('details-post', pk=post.pk)
#
#     else:
#         form = CommentCreateForm()
#
#     context = {
#         'form': form,
#         'post': post,
#     }
#
#     return render(request, 'comments/add-comment.html', context)

# delete_comment FunctionBasedView
# def delete_comment(request, pk: int, comment_pk: int):
#     post = Post.objects.get(pk=pk)
#     comment = Comment.objects.get(pk=comment_pk)
#
#     if request.method == "POST":
#         comment.delete()
#         return redirect('details-post', pk=post.pk)
#
#     context = {
#         "post": post,
#         "comment": comment
#     }
#
#     return render(request, 'comments/delete-comment.html', context)


# delete_comment ClassBasedView
class DeleteCommentView(DeleteView, FormView):
    model = Comment
    template_name = 'comments/delete-comment.html'

    def get_object(self, query_set=None):
        # Override to use `comment_pk` instead of `pk`
        comment_pk = self.kwargs['comment_pk']
        return get_object_or_404(Comment, pk=comment_pk)

    def get_success_url(self):
        post = self.get_post()
        return reverse_lazy('details-post', kwargs={'pk': post.pk})

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        context['comment'] = self.get_object()
        return context


# add_comment as ClassBasedView
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'comments/add-comment.html'

    def get_success_url(self):
        post = self.get_post()
        form = CommentCreateForm
        return reverse_lazy('details-post', kwargs={'pk': post.pk})

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.post = self.get_post()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        return context


# edit_comment as ClassBasedView
class EditCommentView(UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = 'comments/edit-comment.html'

    def get_object(self, queryset=None):
        comment_pk = self.kwargs['comment_pk']
        return get_object_or_404(Comment, pk=comment_pk)

    def get_success_url(self):
        post = self.get_post()
        return reverse_lazy('details-post', kwargs={'pk': post.pk})

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        context['comment'] = self.get_object()
        return context

# edit_comment as FunctionBasedView
# def edit_comment(request, pk: int, comment_pk: int):
#     post = Post.objects.get(pk=pk)
#     comment = Comment.objects.get(pk=comment_pk)
#
#     if request.method == 'POST':
#         form = CommentEditForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('details-post', pk=post.pk)
#
#     else:
#         form = CommentEditForm(instance=comment)
#
#     context = {
#         "post": post,
#         "form": form,
#         "comment": comment,
#     }
#
#     return render(request, 'comments/edit-comment.html', context)
#
