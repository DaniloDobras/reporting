from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False, allow_null=False)
    name = serializers.CharField(required=False, allow_null=True)
    manufacturer = serializers.CharField(required=False, allow_null=True)
    base_unit_content = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    no_of_base_units = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'manufacturer',
                  'base_unit_content',
                  'no_of_base_units'
                  )


class ManufacturerAggregateSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(required=False, allow_null=True)
    count = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ('manufacturer',
                  'count',
                  )


class ActiveAggregateSerializer(serializers.ModelSerializer):
    active = serializers.CharField(required=False, allow_null=True)
    count = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ('active',
                  'count',
                  )


