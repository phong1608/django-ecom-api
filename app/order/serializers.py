from core.models import Order,OrderItem,Address,Product,Cart,CartItem
from rest_framework import serializers
from address.serializers import AddressSerializer
from user.serializers import UserSerializer
from product.serializers import ProductSerializer




class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields='__all__'
        
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
class OrderMiniSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Order
        fields=['cart','shippingPrice']
    
    def create(self,validated_data):
        user =self.context['request'].user
        user_address = Address.objects.get(user=user)
        user_cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        
        order =Order().create_order(buyer=user,address=user_address,cart=user_cart,is_paid=True)
        for item in cart_items:
            order_items= OrderItem().create_order_item(order,item.product,item.quantity)
            order_items.save()
            item.delete()
            item.save()
            
            
        order.save()
        return order
                
        
