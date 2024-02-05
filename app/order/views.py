from rest_framework import viewsets,mixins,status
from core.models import Address
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import CartItem, Product,Category,Cart,OrderItem,Order
from product import serializers
from rest_framework.response import Response
from order import serializers
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView
)
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied


class OrderMiniViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderMiniSerializer
    queryset = Order.objects.all()
    def get_queryset(self):
        user = self.request.user
        queryset= Order.objects.filter(user=user)
        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
        
        
class OrderItemViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = serializers.OrderItemSerializer
    queryset = OrderItem.objects.all()
    def get_queryset(self):
        order_id = self.request.query_params.get('id')

        order = Order.objects.get(id=order_id)
        queryset= OrderItem.objects.filter(order=order)
        return queryset

class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class= serializers.OrderSerializer
    def get_queryset(self):
        user = self.request.user
        queryset= Order.objects.filter(user=user)
        return queryset
    