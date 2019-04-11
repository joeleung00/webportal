from django.urls import path
from . import views
from . import crawlpage
from . import google_calendar

from . import ordering
urlpatterns = [
    path('category/<int:pk>/', views.category, name='portal-category'),
    path('', views.home, name='portal-home'),
    path('about/', views.about, name='portal-about'),
    path('recommendation/', views.recommend, name='portal-recommend'),
    #path("crawl/", crawlpage.crawlpage, name='crawl')
    path('calendar/', google_calendar.calendar),
    path("reorder/", ordering.reorder, name='reorder'),
]
