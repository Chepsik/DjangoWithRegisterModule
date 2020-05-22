from django.urls import path, include
from .views import *

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', SignUpView.as_view(), name='signup'),
    path('accounts/activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('article/create', createArticleView.as_view(), name='article_create'),
    path('article/<int:post_id>/', ArticleView.as_view(), name='article_view'),
    path(r'article/preview/<int:post_id>', views.previewArticle, name='article_preview'),
    path('profile/<str:user>/', profileView.as_view(), name='profile'),
    path('article/categories', CategoriesView.as_view(), name='categories')
]
