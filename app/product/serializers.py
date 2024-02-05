from rest_framework import serializers
from core.models import Product,Category,Cart,CartItem
from rest_framework.exceptions import ValidationError,PermissionDenied,NotAcceptable
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['name','id']
        read_only_fields=['id']
        

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']

    def _get_or_create_category(self, categories, product):
        for category in categories:
            category_obj, created = Category.objects.get_or_create(**category)
            product.categories.add(category_obj)

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        product = Product.objects.create(**validated_data)
        self._get_or_create_category(categories, product)
        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)

        if categories is not None:
            
            instance.categories.clear()
            self._get_or_create_category(categories, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# class CartSerializer(serializers.ModelSerializer):
#     product_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

#     class Meta:
#         model = Cart
#         fields = ['id', 'product_ids', 'count']

#     def create(self, validated_data):
#         product_ids = validated_data.pop('product_ids', [])
#         cart = Cart.objects.create(**validated_data)
#         cart.product.set(product_ids)
#         return cart
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "seller",
            "quantity",
            "price",
            "image",
        )       
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =CartItem
        fields=['product','quantity']
    
    def create(self, validated_data):
        user =self.context['request'].user
       
        product = Product.objects.get(pk=self.context['request'].data["product"])
        
            
        
        cart = Cart.objects.get(user=user)
        
        current_cart = CartItem.objects.filter(cart=cart).all()
        current_item = CartItem.objects.filter(cart=cart, product=product)
        
        try:
            quantity = int(self.context['request'].data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")
        if current_item.count()>0:
            raise NotAcceptable("You already have this item in your shopping cart")
        cart_item = CartItem(cart=cart,product=product,quantity=quantity)
        cart_item.save()
        total=0
        for item in current_cart:
            total =total+ float(item.product.price) * float(item.quantity)
            
        cart.total = total
        cart.save()
        return cart_item
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)
    class Meta:
        models=CartItem
        fields=['product','quantity']
        
        
class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields=['product','quantity']
        
        