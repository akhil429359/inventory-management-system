from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    STATUS = [
        ('available','Available'),
        ('out_of_stock','Out of stock')
    ]
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=STATUS,default='available')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class StockLog(models.Model):
    STOCK_TYPE = [
        ('in','Stock In'),
        ('out','Stock Out')
    ]

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    change_type = models.CharField(max_length=5,choices=STOCK_TYPE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.change_type}"