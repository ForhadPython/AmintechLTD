from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contactus, name='contactus'),
    path('product/', views.product, name="product"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # User account manage urls
    path('login/', views.login_form, name='login_form'),
    path('logout/', views.logout_func, name='logout_func'),
    path('signup/', views.signup_form, name='signup_form'),

    # User Profile manage urls
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('favourite_post/<int:id>', views.favourite_post, name="favourite_post"),
    path('favourites', views.post_favourite_list, name="post_favourite_list"),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
]
