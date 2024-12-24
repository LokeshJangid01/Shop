from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)        
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    products = models.ManyToManyField(
        Product, through='OrderItem', related_name='orders'
    )
    total_order_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     # Calculate total_order_price
    #     self.total_order_price = sum(
    #         item.total_product_price for item in self.orderitem_set.all()
    #     )
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_product_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0.00
    )

    def save(self, *args, **kwargs):
        # Calculate total_product_price
        self.total_product_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    # Update total_order_price of the associated order
        order = self.order
        order.total_order_price = sum(
        item.total_product_price for item in order.orderitem_set.all()
    )

    def delete(self, *args, **kwargs):
        # Store the associated order before deleting the item
        order = self.order

        # Delete the item
        super().delete(*args, **kwargs)

        # Recalculate total_order_price for the order
        order.total_order_price = sum(
            item.total_product_price for item in order.orderitem_set.all()
        )
        order.save()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
    
# Signal to update total_order_price after saving OrderItem
@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    # Recalculate total_order_price for the order
    order.total_order_price = sum(
        item.total_product_price for item in order.orderitem_set.all()
    )
    order.save()
    
    

