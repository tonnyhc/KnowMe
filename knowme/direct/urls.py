from django.urls import path

from knowme.direct.views import inbox, direct, send_direct

urlpatterns = [
    path('', inbox, name='inbox'),
    path('<str:username>/', direct, name='direct'),
    path('<str:username>/<int:pk>/', send_direct, name='send direct')

]
