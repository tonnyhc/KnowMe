from django.urls import path

from knowme.accounts.views import ProfileDetailsView, SignInView, SignUpView, SignOutView, PasswordChangeView, \
    AccountEditView, account_delete_view, profile_edit_view, report_profile

urlpatterns = [
    path('details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('sign-in/', SignInView.as_view(), name='sign in'),
    path('sign-up/', SignUpView.as_view(), name='sign up'),
    path('sign-out/', SignOutView.as_view(), name='sign out'),
    path('change-password/', PasswordChangeView.as_view(), name='change password'),
    path('settings/<int:pk>', AccountEditView.as_view(), name='account edit'),
    path('delete/<int:pk>/', account_delete_view, name='account delete'),
    path('edit/<int:pk>/', profile_edit_view, name='profile edit'),
    path('report/<str:username>/', report_profile, name='report profile')
]