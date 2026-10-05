"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ---------- Endpoints catalogue ----------
    path("api/catalogue/", include("apps.catalogue.urls")),
    path("api/admin/catalogue/", include(("apps.catalogue.urls_admin", "catalogue"))),

    # --------- Endpoints configurateur ----------
    path("api/configurateur/", include("apps.configurateur.urls")),

    # -------- Endpoints commercial ----------
    path("api/admin/commercial/", include("apps.commercial.urls")),

    # -------- Endpoints reprise ----------
    path("api/reprise/", include("apps.reprise.urls")),
    path("api/admin/reprise/", include("apps.reprise.urls_admin")),

    # ------- Endpoints reseau ----------
    path("api/reseau/", include("apps.reseau.urls")),

    # ------- Endpoints comptes ----------
    path("api/comptes/", include("apps.comptes.urls")),
    
    # ------ Endpoints paiement ----------
    path("api/paiement/", include("apps.paiement.urls")),
]
