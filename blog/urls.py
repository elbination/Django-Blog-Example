from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # Post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',
         views.post_detail, name='post_detail'),
    path('feed/', LatestPostsFeed(), name='post_feed')
]
