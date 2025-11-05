from django.urls import path
from .views import CategoryList, PostList, PostDetail, post_search, featured_posts

app_name = "blog"

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="category_list"),
    path("posts/", PostList.as_view(), name="post_list"),
    path("posts/<str:lang>/<slug:slug>/", PostDetail.as_view(), name="post_detail"),
    path("search/", post_search, name="post_search"),
    path("featured/", featured_posts, name="featured_posts"),
]