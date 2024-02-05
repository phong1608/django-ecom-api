from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    categories = models.ManyToManyField('Category')
    image = models.TextField(max_length=255, blank=True) 
    price = models.IntegerField()
    rating = models.DecimalField(max_digits=7, decimal_places=2,blank=True,default=0)
    numReviews = models.IntegerField(null=True, blank=True,default=0)
    stock=models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)


    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    
    

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="address", on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number =  models.TextField(null=True, blank=True)

    
    
class Order(models.Model):
    PENDING_STATE = "p"
    COMPLETED_STATE = "c"

    ORDER_CHOICES = ((PENDING_STATE, "pending"), (COMPLETED_STATE, "completed"))
    create_date = models.DateTimeField(auto_now_add=True,null=True)
    delivered_date = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='order')
    
    status = models.CharField(
        max_length=1, choices=ORDER_CHOICES, default=PENDING_STATE
    )
    is_paid = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart,related_name='order_cart',on_delete=models.CASCADE,null=True)
    address = models.ForeignKey(
        Address, related_name="order_address", on_delete=models.CASCADE
    )
    @staticmethod
    def create_order(buyer, address,cart, is_paid=False):
        order = Order()
        order.user = buyer
        order.address = address
        order.is_paid = is_paid
        order.cart = cart
        order.save()
        return order   


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_order", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(blank=True,default=1)
    
    @staticmethod
    def create_order_item(order, product, quantity):
        order_item = OrderItem()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        
        order_item.save()
        return order_item