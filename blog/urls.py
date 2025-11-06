from django.urls import path
from .views import CategoryList, BlogPosts, BlogFeatured, BlogPostDetail, BlogPostsAdmin

app_name = "blog"

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="category_list"),
    path("posts/", BlogPosts.as_view(), name="blog_posts"),
    path("posts/featured/", BlogFeatured.as_view(), name="blog_featured"),
    path("posts/<slug:slug>/", BlogPostDetail.as_view(), name="blog_post_detail"),
    path("admin/posts/", BlogPostsAdmin.as_view(), name="admin_blog_posts"),
    path("admin/posts/<int:post_id>/", BlogPostsAdmin.as_view(), name="admin_blog_post_detail"),
]