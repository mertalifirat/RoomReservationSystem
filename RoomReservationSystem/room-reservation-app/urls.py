"""
URL configuration for RoomReservationSystem project.

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
from django.urls import path

from views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Home.as_view(), name="home"),
    path('login', Login.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
    # path('sign-up', SignUp.as_view(), name="signup"),
    # path('upload-photo', UploadPhoto.as_view(), name="upload_photo"),
    # path('photo', PhotoView.as_view(), name="update_photo"),
    # path('photos', PhotoView.as_view(), name="photos"),
    # path('collections', CollectionView.as_view(), name="collections"),
    # path('collection/<int:id>', CollectionDetail.as_view(), name="collection_detail"),
    # path('views', Filter.as_view(), name="views"),
    # path('view/<int:id>', FilterViewDetail.as_view(), name="view_detail"),

]