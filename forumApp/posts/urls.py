from django.urls import path, include
from forumApp.posts.views import IndexView, DashboardView, AddPostView, EditPostView, DeletePostView, DeleteCommentView, \
    AddCommentView, EditCommentView, PostDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dash'),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('<int:pk>/', include([
        path('delete-post/', DeletePostView.as_view(), name='delete-post'),
        path('details-post/', PostDetailView.as_view(), name='details-post'),
        path('edit-post/', EditPostView.as_view(), name='edit-post'),
        path('add-comment/', AddCommentView.as_view(), name='add-comment'),
        path('edit-comment/<int:comment_pk>/', EditCommentView.as_view(), name='edit-comment'),
        path('delete-comment/<int:comment_pk>/', DeleteCommentView.as_view(), name='delete-comment')
    ]))
]
