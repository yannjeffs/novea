from django.urls import path

from .views import ProfilView

urlpatterns = [
    path("moi/", ProfilView.as_view(), name="mon-profil"),
]