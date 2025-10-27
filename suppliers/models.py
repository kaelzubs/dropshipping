from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=120)
    base_url = models.URLField()
    api_key = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self): return self.name

class SupplierOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    local_order_id = models.IntegerField()  # reference to Order.id
    remote_order_id = models.CharField(max_length=120, blank=True)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=50, default='created')
    created_at = models.DateTimeField(auto_now_add=True)