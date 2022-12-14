from django.urls import path, include

from knowme.common.views import index, add_comment, delete_comment, comment_report_view, like_post, save_post, \
    follow_profile, notifications_view, search_view, about_page

urlpatterns = [
    path('', index, name='index'),
    path('comments/', include([
        path('add/<int:post_id>/', add_comment, name='add_comment'),
        path('delete/<int:comment_id>', delete_comment, name='delete_comment'),
        path('report/<int:comment_id>', comment_report_view, name='report comment'),
    ])),
    path('like/<int:post_id>', like_post, name='like_post'),
    path('save/<int:post_id>', save_post, name='save_post'),
    path('follow/<int:profile_id>', follow_profile, name='follow'),
    path('notifications/', notifications_view, name='notifications'),
    path('search/', search_view, name='search'),
    path('about/', about_page, name='about')
]
