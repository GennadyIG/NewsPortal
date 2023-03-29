from django.urls import path
from .views import ShowProfileView, ProfileEdit

urlpatterns = [
    path('<int:pk>', ShowProfileView.as_view(), name='profile'),
    path('<int:pk>/edit/', ProfileEdit.as_view(), name='edit_profile'),
]
