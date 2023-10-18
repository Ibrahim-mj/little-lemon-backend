from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer (serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Serializes the 'id' and 'title' fields of the Category model.
    """
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for the MenuItem model.

    This serializer includes fields for the MenuItem's id, title, price, inventory,
    category, and category_id. The category field is read-only, while the category_id
    field is write-only.

    Attributes:
        category: A CategorySerializer instance representing the MenuItem's category.
        category_id: An integer representing the ID of the MenuItem's category.
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory', 'category', 'category_id']