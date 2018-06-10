from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Property, SaleOrder, SaleOrderLine


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class PropertySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False)

    class Meta:
        model = Property
        fields = ('product', 'name', 'value')


class ProductSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'properties', 'description', 'price')

    def create(self, validated_data):
        properties_data = validated_data.pop('properties')
        product = Product.objects.create(**validated_data)
        for property in properties_data:
            Property.objects.create(product=product, **property)
        return product

    def update(self, instance, validated_data):
        properties_data = validated_data.pop('properties')
        instance.save()
        prop_list = self.update_or_create_preperties(properties_data)
        self.check_and_delete_properties(instance, prop_list)
        return instance

    def update_or_create_preperties(self, properties_data):
        prop_list = []
        for property in properties_data:
            p = Property.objects.filter(product__pk=property['product'].id,
                                        name=property['name']).first()
            if p:
                if p.value != property['value']:
                    p.value = property['value']
                    p.save()
            else:
                p = Property.objects.create(**property)
            prop_list.append(p)
        return prop_list

    def check_and_delete_properties(self, product, new_prop_list):
        prod_prop = product.properties.all()
        prod_prop = list(prod_prop)
        to_delete = list(set(prod_prop) - set(new_prop_list))
        for item in to_delete:
            item.delete()


class SaleOrderLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = SaleOrderLine
        fields = ('product', 'quantity', 'total')

    def validate_quantity(self, value):
        """
            Check that the quantity is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be positive")
        return value


class SaleOrderSerializer(serializers.ModelSerializer):
    lines = SaleOrderLineSerializer(many=True)
    customer = UserSerializer(many=False)

    class Meta:
        model = SaleOrder
        fields = ('lines', 'customer', 'date', 'total_sale')
        ordering = ('date',)

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        order = SaleOrder.objects.create(**validated_data)
        for line in lines_data:
            SaleOrderLine.objects.create(sale_order=SaleOrder, **line)
        return order
