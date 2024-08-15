"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from SHOES.views import *
from django.conf import settings
from django.conf.urls.static import static
from USER.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shoe/<pk>/", shoe_page_view, name = 'shoes-view'),
    path('tag/<slug:tag>/', tag_view, name='tag'),
    path('brand/<slug:brand>/', brand_view, name='brand'),
    path('accounts/', include('allauth.urls')),
    path('',home_view,name= 'home'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name ='profile-edit'),
    path('profile/delete/',profile_delete_view, name ='profile-delete'),
    path('cart/', cart_view, name='cart-view'),
    path('cart/remove/<int:id>/', delete_cartitem, name='delete-cart-item'),  
    path('confirm_checkout/', confirm_checkout, name='confirm-checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
