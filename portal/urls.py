from django.urls import path
from . import views
from . import crawlpage
from . import ordering
urlpatterns = [
    path('category/<int:pk>/', views.category, name='portal-category'),
    path('', views.home, name='portal-home'),
    path('about/', views.about, name='portal-about'),
    path("reorder/", ordering.reorder, name='reorder')
]
