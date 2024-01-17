from django.shortcuts import get_object_or_404
from rest_framework import viewsets,mixins,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import CartItem, Product,Category,Cart
from product import serializers
from rest_framework.response import Response

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView
)
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
class ProductViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
     
     
class CategoryViewSet(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

class CartItemViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=serializers.CartItemSerializer
    queryset=CartItem.objects.all()
    def get_queryset(self):
        user = self.request.user
        queryset=CartItem.objects.filter(cart__user=user)
        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)       
        

        