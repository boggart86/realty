from django.urls import path
from . import views

app_name = 'realty'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('realty/<int:pk>/', views.realty_detail, name='detail'),
    path('realty/create/', views.realty_create, name='create'),
    path('realty/<int:pk>/edit/', views.realty_edit, name='edit'),
    path('realty/<int:pk>/delete/', views.realty_delete, name='delete'),
    path('realty/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('realty/photo/<int:photo_pk>/delete/', views.delete_photo, name='delete_photo'),
    path('favorites/', views.favorites, name='favorites'),
]
