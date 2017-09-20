from django.conf.urls import url
from .views import UserRegistraionView, UserDetailView, LoginView, RegistrationView


urlpatterns = [
    url(r'^users/$', UserRegistraionView.as_view(), name='user_registration'),
    url(r'^users/(?P<pk>[\w-]+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration')
]