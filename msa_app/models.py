from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null = True, blank = True, default = "")
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField('DOB')
    gender = models.CharField(max_length=10)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=200)
    is_admin = models.BooleanField(default = False, null=True, blank=True)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "employee_data"

    def __str__(self):
        return self.first_name + " " + self.last_name

class Medicine(models.Model):
    trade_name = models.CharField(max_length=50, default="default trade name")
    generic_name = models.CharField(max_length=50, default="default generic name")
    unit_sell_price = models.DecimalField(decimal_places = 2, max_digits = 7, default=0)
    unit_purchase_price = models.DecimalField(decimal_places = 2, max_digits = 7, default=0)
    medicine_id = models.CharField(max_length=10, null=True, default="MED")

    class Meta:
        db_table = "medicine_data"

    def __str__(self):
        return self.generic_name

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=50, default="default vendor")
    email = models.EmailField(null=True)
    mobile = models.BigIntegerField(default=0)
    address = models.CharField(max_length=200, null=True)
    vendor_id = models.CharField(max_length=10, null=True, default="VEN")
    medicine_ids = models.CharField(max_length=100, default="MED")

    class Meta:
        db_table = "vendor_data"
    
    def __str__(self):
        return self.vendor_name

class MedicineToVendor(models.Model):
    medicine_id = models.CharField(max_length=10, default="MED")
    vendor_id = models.CharField(max_length=10, default="VEN")

    class Meta:
        db_table = "vendor_to_medicine"

class Stock(models.Model):
    vendor_id = models.CharField(max_length=10, default="VEN")
    medicine_id = models.CharField(max_length=10, default="MED")
    batch_id = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True)

    class Meta:
        db_table = "stock_data"

class Sales(models.Model):
    medicine_id = models.CharField(max_length=100, default="MED")
    quantity = models.IntegerField(default=0)
    date = models.DateField(null=True)
    sale_id = models.IntegerField(default=0)

    class Meta:
        db_table = "sales_data"
    
class Bill(models.Model):
    customer_name = models.CharField(max_length=100, default = "default customer")
    customer_number = models.BigIntegerField(null=True)
    amount = models.IntegerField(null=True)
    bill_id = models.IntegerField(default=0)
    bill_copy = models.CharField(max_length=50, null=True, default="Not available")

    class Meta:
        db_table = "bill_data"

class MedicineStock(models.Model):
    medicine_id = models.CharField(max_length=100, default="MED")
    stock = models.IntegerField(default=0)
    threshold = models.IntegerField(default = 50, null=True)

    class Meta:
        db_table = "medicine_stock"

class ExpiredMedicines(models.Model):
    medicine_id = models.CharField(max_length=100, default="MED")
    quantity = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True)

    class Meta:
        db_table = "expired_medicines"