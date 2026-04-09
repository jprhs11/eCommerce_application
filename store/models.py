from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends the base User model to include specific roles.
    """
    ROLE_CHOICES = (
        ('vendor', 'Vendor'),
        ('buyer', 'Buyer'),
    )

    # One-to-one link ensures each User has exactly one Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Store the user's role; defaults to 'buyer' for safety
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='buyer'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Store(models.Model):
    """
    Represents a digital storefront owned by a vendor.
    """
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stores'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents an item listed for sale within a specific store.
    """
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.store.name})"


class Order(models.Model):
    """
    Tracks a purchase made by a buyer.
    """
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    """
    Individual products tied to a specific order.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    """
    Model representing a customer review for a specific product.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    # Distinguishes between purchase-based reviews and others
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = 'Verified' if self.is_verified else 'Unverified'
        return f"{self.user.username} - {self.product.name} ({status})"
