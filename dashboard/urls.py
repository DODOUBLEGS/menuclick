
from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.dashboard,name='dashboard'),

    

    path('login', views.login,name="login"),
    path('logout',views.logout,name='logout'),
    
    
    # shoptype
    path('shoptype',views.shoptype,name='shoptype'),
    path('shoptypesearch',views.shoptypesearch,name='shoptypesearch'),
    path('viewshoptype<int:pk>',views.viewshoptype,name='viewshoptype'),
    path('addshoptype',views.addshoptype,name='addshoptype'),
    path('editshoptype/<int:pk>' , views.editshoptype , name='editshoptype'),
    path('deleteshoptype<int:pk>', views.deleteshoptype,name='deleteshoptype'),

    path('shop-type/block/<int:pk>/', views.block_shop_type, name='block_shop_type'),
    path('shop-type/activate/<int:pk>/', views.activate_shop_type, name='activate_shop_type'),
    
    
    #  category
    path('category',views.category,name='category'),
    path('addcat',views.addcat,name='addcat'),
    path('editcat/<int:pk>',views.editcat,name='editcat'),


    # # shop
    path('shop',views.shop,name='shop'),
    path('block_shop/block/<int:pk>/', views.block_shop, name='block_shop'),
    path('activate_shop/activate/<int:pk>/', views.activate_shop, name='activate_shop'),
    # path('addshop',views.addshop,name='addshop'), # neded to swap
    
    path('create',views.create,name='create'),
    
    path('editshop/<int:pk>',views.editshop,name='editshop'),
    # path('editsha/<int:pk>',views.editsha,name='editsha'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

    path('menu/<str:shop_url>',views.shopmenu,name='shopmenu'),
    path('flipbook/<int:pk>',views.flipbook,name='flipbook'),

    path('renew_subscription/<int:list_id>/', views.renew_subscription, name='renew_subscription'),

    path('get_categories',views.get_categories,name='get_categories'),

    # # adduser
    path('viewuser',views.viewuser,name='viewuser'),
    
    path('addusers',views.addusers,name='addusers'),
    path('editusers/<int:pk>/',views.editusers,name='editusers'),
    path('shoped/<int:pk>',views.shoped,name='shoped'),

 
   
  


    # # api  
    path('api/shoptype/', views.ShoptypeList.as_view(), name='shoptype-api'),
    path('api/shoptype/<int:pk>', views.ShoptypeDetails.as_view(), name='shoptype-api-id'),
    path('api/shoplist/', views.ShopList.as_view(), name='category-list'),
    path('api/shoplist/<int:pk>', views.ShopDetails.as_view(), name='category-list-id'),

    # ///
    path('api/shop/category/<str:category_name>/',views.ShopByCategoryView.as_view(),name='shpet'),

    path('<path:unknown_path>', views.handle_404, name='handle_404'),

    path('shoped/<int:pk>',views.shoped,name='shoped'),
    
    
    ]
