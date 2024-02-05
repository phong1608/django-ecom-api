from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order import views

router= DefaultRouter()
router.register('order',views.OrderViewSet)
router.register('checkout',views.OrderMiniViewSet)
router.register('order-items',views.OrderItemViewSet)


app_name='order'

urlpatterns = [
    path('',include(router.urls)),
]