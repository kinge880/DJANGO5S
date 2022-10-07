"""fiveS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from sectors.api import viewsets as sectorviewsets
from accounts.api import viewsets as userviewsets
from fiveForms.api import viewsets as formviewsets

route = routers.DefaultRouter()
route.register(r'sectors', sectorviewsets.sectorsViewset, basename='sectors')
route.register(r'sectorsGroup', sectorviewsets.sectorsGroupViewset, basename='sectorsgroup')
route.register(r'sectorshome', sectorviewsets.sectorsHomeViewset, basename='sectors home')
route.register(r'sectorsgrouphome', sectorviewsets.sectorsGroupHomeViewset, basename='sectors group home')
route.register(r'imagesectors', sectorviewsets.imageSectorsViewset, basename = "ImageSectors")
route.register(r'branch', sectorviewsets.branchViewset, basename='branch')
route.register(r'formr', formviewsets.fiveFormViewset, basename = "Formulário 5s")
route.register(r'formrask', formviewsets.askViewset, basename = "Pergunta dos formulários")
route.register(r'formresponse', formviewsets.responseViewset, basename = "Resposta dos formulários")
route.register(r'formresponseimage', formviewsets.responseImageViewset, basename = "Imagem das respostas dos formulários")
route.register(r'metrics/form', formviewsets.Forms5sRelatoryViewset, basename = "formularios dos relatorios")
route.register(r'metrics/relatory', formviewsets.Relatory5SViewset, basename = "resposta para os relatorios'")
route.register(r'usersectors', sectorviewsets.userSectorsViewset, basename = "userSetor")
route.register(r'user', userviewsets.userManageViewset, basename = "user")
route.register(r'auth/login', userviewsets.LoginViewSet, basename='auth-login')
route.register(r'auth/register', userviewsets.RegistrationViewSet, basename='auth-register')
route.register(r'auth/refresh', userviewsets.RefreshViewSet, basename='auth-refresh')
#route.register(r'usuarios/trocarsenha', userviewsets.ChangePasswordView, basename = "Trocar senha")
route.register(r'office/manage', userviewsets.officeViewset, basename = "Cargos")
route.register(r'office', userviewsets.officeGetViewset, basename = "getCargos")
route.register(r'users/profile', userviewsets.ProfileAPI, basename = "profile")
route.register(r'users/profileEdit', userviewsets.ProfileAPIEdit, basename = "profileEdit")
route.register(r'users/profile/changepassword', userviewsets.ChangePasswordView, basename = "changepassword"),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(route.urls)),
    path('users/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
