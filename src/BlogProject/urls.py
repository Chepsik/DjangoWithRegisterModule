from django.contrib import admin
from blogApp import views as blogApp_views
from django.urls import include, path
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', include('blogApp.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

handler404 = blogApp_views.error_404
handler500 = blogApp_views.error_500
