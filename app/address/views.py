from rest_framework import viewsets,mixins,status
from core.models import Address
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import CartItem, Product,Category,Cart
from product import serializers
from rest_framework.response import Response
from address import serializers
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView
)
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied



class AddressViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddressSerializer
    queryset = Address.objects.all()
    def get_queryset(self):
        user = self.request.user
        queryset= Address.objects.filter(user=user)
        return queryset
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
    