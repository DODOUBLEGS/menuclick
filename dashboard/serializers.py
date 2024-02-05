from rest_framework import serializers
from .models import ShopType,Category,Shop
from django.utils import timezone

class ShopTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopType
        fields = ('__all__')
from .models import Icon

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('__all__')


