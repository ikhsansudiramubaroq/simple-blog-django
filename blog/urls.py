from django.urls import path

from . import views

app_name="blog"
urlpatterns = [
    path('', views.index, name='blog_index'),
    # slug diambil dari slug bawaan django berisi slug_input
    # slug_input adalah nama variabel yang akan diambil dari url
    path('detail/<slug:slug_input>/', views.detail_article,name='detail_article'),
    path('category/<slug:category_input>/', views.category,name='category'),
    path('tags/<slug:tags_input>/', views.tagged,name='tags'),
]