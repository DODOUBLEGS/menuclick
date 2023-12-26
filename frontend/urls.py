from django.urls import path,include
from .import views

urlpatterns = [
    path('user_login',views.user_login,name='user_login'),
    path('user_signup',views.user_signup,name='user_signup'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('',views.home,name='home'),
    path('add_shop',views.add_shop,name='add_shop')
    
]