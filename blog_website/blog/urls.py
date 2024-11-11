from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_blog, name='create_blog'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('myblog/', views.my_blog, name='myblog'),
    path('blogs/<int:blog_id>/', views.view_blog, name='view_blog'),  # Added path for viewing a specific blog
    path('blog/<int:blog_id>/comment/', views.create_comment, name='create_comment'),
]
