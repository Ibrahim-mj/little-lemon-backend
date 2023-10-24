from rest_framework import generics

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class CategoriesView(generics.ListCreateAPIView):
    """
    API endpoint that allows categories to be viewed or created.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    """
    API endpoint that allows menu items to be viewed or created.
    """

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "inventory"]
    filter_fields = ["price", "inventory"]
    search_fields = ["category__title", "title"]
