from django.contrib import admin #import admin untuk url admin
from django.urls import path, include,re_path #re_path untuk Regular Expression
from django.views.static import serve
from . import views #import semua views
from django.conf import settings #untuk import dari setting import static dan media
from django.conf.urls.static import static #untuk fungsi import url static


urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', include('blog.urls')),
    path('kontak/', include('kontak.urls', namespace='kontak')),
    path('accounts/', include('account.urls', namespace='accounts')),
    
    # fungsi url auth bawaan django dan akan load url berikut:
        # /accounts/login/ dengan templatenya registration/login.html
        # /accounts/logout/ dengan templatenya registration/logged_out.html dll seperti changepassword dll
        # file seperti login.html, logout.html, dan lainnya harus berada di templates/registration/
    # path('accounts/', include('django.contrib.auth.urls')),
    
    # re_path,serve, digunakan untuk kondisi DEBUG = True yg ada di settings
    # r'^media/(?P<path>.*)$' adalah reguler expression
    #serve adalah Fungsi view yang dipanggil.
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #fungsi untuk load file media seperti gambar dll

handler404 = "mysite.views.handler404" #custom error view ketika user akses url yang tidak ada