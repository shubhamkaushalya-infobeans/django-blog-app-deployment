from django.urls import path
from . import views

app_name = 'blog_app_name'
urlpatterns = [
     path('add-blog/', views.CreateBlog.as_view(), name='add-blog'),
     path('blog-list/', views.BlogList.as_view(), name='blog-list'),
     path('draft-blogs/', views.DraftBlogList.as_view(), name='draft-blogs'),
     path('blog-detail/<int:pk>',views.BlogDetails.as_view(), name="blog-details"),
     path('blog-publish/<int:pk>',views.blog_publish, name="blog-publish"),
     path('add-comment/<int:pk>',views.add_comment, name="add-comment"),
     path('login',views.login_user, name='login'),
     path('logout',views.logout_user, name='logout'),
     path('approve-comment/',views.approve_comment, name="approve-comment"),
     path('remove-comment/<int:pk>',views.remove_comment, name="remove-comment"),
]