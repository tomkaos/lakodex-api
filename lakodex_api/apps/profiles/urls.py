from django.conf.urls import url

from .views import ProfileDetailsView

app_name = 'profiles'

urlpatterns = [
    url(r'^$', ProfileDetailsView.as_view()),
]
