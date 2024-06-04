# models.py
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Benhnhan(models.Model):
	hoten = models.CharField(max_length = 100)
	gioitinh = models.CharField(max_length = 100)
	namsinh = models.IntegerField()
	diachi = models.CharField(max_length = 100)
	ngaykham = models.DateField(default='2024-01-01')

class Hoadon(models.Model):
    benhnhan = models.OneToOneField(Benhnhan,on_delete=models.CASCADE)
    tienkham = models.IntegerField()
    tienthuoc = models.IntegerField()
    
class PhieuKB(models.Model):
    benhnhan = models.OneToOneField(Benhnhan,on_delete=models.CASCADE)
    trieuchung = models.CharField(max_length=100)
    dudoan = models.CharField(max_length=100)
    
class Thuoc(models.Model):
    tenThuoc = models.CharField(max_length=50)
    giatheovien = models.IntegerField()
    giatheochai = models.IntegerField()
    soviencon = models.IntegerField()
    sochaicon = models.IntegerField()

class PKBthuoc(models.Model):
    phieukb = models.ForeignKey(PhieuKB,on_delete=models.CASCADE)
    thuoc = models.ForeignKey(Thuoc,on_delete=models.CASCADE)
    donvi = models.CharField(max_length=50)
    soluong = models.IntegerField()
    cachdung = models.CharField(max_length=50)
    
class thietbiYte(models.Model):
    SUPPLIER_CHOICES = [
        ('Supplier A', 'Supplier A'),
        ('Supplier B', 'Supplier B'),
        ('Supplier C', 'Supplier C'),
        ('Supplier D', 'Supplier D'),
        ('Supplier E', 'Supplier E'),
    ]

    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=200, choices=SUPPLIER_CHOICES)
    import_date = models.DateField()
    price = models.IntegerField()
    purpose = models.TextField()

    def __str__(self):
        return self.name
    
