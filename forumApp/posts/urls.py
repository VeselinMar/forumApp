from django.urls import path, include
from forumApp.posts.views import dashboard, index, add_post, edit_post, details_post, delete_post, add_comment, \
    edit_comment, delete_comment

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dash'),
    path('add-post/', add_post, name='add-post'),
    path('<int:pk>/', include([
        path('delete-post/', delete_post, name='delete-post'),
        path('details-post/', details_post, name='details-post'),
        path('edit-post/', edit_post, name='edit-post'),
        path('add-comment/', add_comment, name='add-comment'),
        path('edit-comment/<int:comment_pk>/', edit_comment, name='edit-comment'),
        path('delete-comment/<int:comment_pk>/', delete_comment, name='delete-comment')
    ]))
]
