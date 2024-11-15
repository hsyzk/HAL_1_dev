from django.urls import path
from . import tests
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import login
from .views import LikeHome, LikeHome_Mu, MylistHome

app_name = 'myapp'
urlpatterns = [
    path('', tests.test, name='test'),
    
    path('index/', views.Login, name='Login'),
    path('logout', views.Logout,name="Logout"),
    path('home/', views.Home.as_view(), name='home'),
    path('home_mu/', views.Home_Mu.as_view(), name='home_mu'),
    path('post/', views.CreatePost.as_view(), name='post'),
    path('post_mu/', views.CreatePost_Mu.as_view(), name='post_mu'),
    path('createac/', views.AccountRegistration.as_view(), name='register'),
    path('search/', views.search, name='search'),
    path('search_mu/', views.search_mu, name='search_mu'),
    path('shop/', views.Views_shop.as_view(), name='shop'),
    path('profile/', views.MyPost.as_view(), name='profile'),
    path('notice/', views.Views_notice.as_view(), name='notice'),
    path('message/', views.Views_message.as_view(), name='message'),
    path('ri_ru/', views.Views_ri_ru.as_view(), name='ri_ru'),
    path('mylist/', views.mylist, name='mylist'),
    path('like-home_mu/<int:pk>', LikeHome_Mu.as_view(), name='like-home_mu'),
    path('like-home/<int:pk>', LikeHome.as_view(), name='like-home'),
    # path('like-search/<int:pk>', LikeSearch.as_view(), name='like-search'),
    path('like-mylist/<int:pk>', MylistHome.as_view(), name='mylist-home'),
    # path('like-profile/<int:pk>', LikeProfile.as_view(), name='like-profile'),
    
    
]

