"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include

# ... the rest of your URLconf goes here ...


from django.contrib import admin
from django.urls import path
from pages.views import home_view, recipe_detail_view, register_view, catalogue_view, user_recipes_view
from django.contrib.auth import views as auth_views

# at this url tell which view you want to use
# you can also link to another "app" urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('catalogue/', catalogue_view, name='catalogue'),
    path('recipe/<int:pk>', recipe_detail_view, name='recipe_detail'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('myrecipes/', user_recipes_view, name='myrecipes')
]

urlpatterns += staticfiles_urlpatterns()

# Add Django site authentication urls (for login, logout, password management)

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
