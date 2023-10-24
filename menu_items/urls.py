from django.urls import path

from . import views

urlpatterns = [
    path("category", views.CategoriesView.as_view(), name="category"),
    path("menu-items", views.MenuItemsView.as_view(), name="menu_items"),
]
