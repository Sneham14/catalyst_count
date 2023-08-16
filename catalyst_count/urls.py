"""catalyst_count URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from catalyst_count_app.views import  users, result_count_api,home, register, add_user, query_builder, upload_data,  user_login, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', register, name='register'),
    path('home', home, name='home'),
    path('user_login', user_login, name="user_login"),
    path('add_user',add_user, name='add_user'),
    path('upload_data', upload_data, name='upload_data'),
    path('query_builder', query_builder, name='query_builder'),
    path('user_logout', user_logout, name='user_logout'),
    path('result_count_api/', result_count_api, name='result_count_api'),
    path('users',users,name="users"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)