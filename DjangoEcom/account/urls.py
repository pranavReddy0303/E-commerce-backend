from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path('categories', ListCategory.as_view(), name='categorie'),
    path('categories/<int:pk>/', DetailCategory.as_view(), name='singlecategory'),
    

    path('products', ListProduct.as_view(), name='products'),
    path('account/products/<int:pk>/', DetailProduct.as_view(), name='singleproduct'),
    path('user/listproduct',UserListProduct.as_view(),name='userlistproduct'),
    path('user/getproduct/<int:pk>/',UserDetailProduct.as_view(),name='userdetailproduct'),

    path('users', ListUser.as_view(), name='users'),
    path('users/<int:pk>/', DetailUser.as_view(), name='singleuser'),

    path('carts', ListCart.as_view(), name='allcarts'),
    path('carts/<int:pk>', DetailCart.as_view(), name='cartdetail'),

    path('cart_products', UserlistCart.as_view(), name='userlistcarts'),
    path('cart_products/<int:cart_id>/', UserdetailCart.as_view(), name='usercartdetail'),
   

    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),


    path('order', OrderDetail.as_view(), name='orderdetail'),
    path('order/item/', OrderItem.as_view(), name='userorderitem'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
   
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refreshtoken'),

   





]