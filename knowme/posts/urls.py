from django.urls import path

from knowme.common.views import share_post
from knowme.posts.views import PostDetailsView, post_edit_view, PostDeleteView, add_post_view, post_report_view

urlpatterns = [
    path('details/<int:pk>', PostDetailsView.as_view(), name='post details'),
    path('edit/<int:pk>', post_edit_view, name='post edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post delete'),
    path('add/', add_post_view, name='post add'),
    path('share/<int:pk>/', share_post, name='share post'),
    path('report/<int:pk>', post_report_view, name='report post'),
]