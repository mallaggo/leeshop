from django.urls import path
from . import views
app_name='shop'

urlpatterns=[
    path('sign_up/',views.sign_up,name='sign_up'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('<str:category_slug>/',views.product_list,name='product_list_category'),
    path('<int:id>/<str:slug>/',views.product_detail,name='product_detail'), #한글일때는 <str:slug>방식을 쓴다.
    path('',views.product_list,name='product_list'),
    path('test/',views.test,name='test'),
]