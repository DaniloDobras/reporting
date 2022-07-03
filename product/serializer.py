from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False, allow_null=False)
    name = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  )
