from datetime import datetime
from django.utils import timezone
from django.db import models
from neonadmin.models import products,coupens

class neonlogin(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True)
    password = models.CharField(max_length = 500)
    blocked = models.CharField(max_length = 1, default = 'F')
    twofakey = models.CharField(max_length=150,null=True)
    twofa = models.CharField(max_length=1,default='F')

class wishlist(models.Model):
    uid = models.ForeignKey(neonlogin,on_delete = models.CASCADE)
    pid = models.ForeignKey(products,on_delete = models.CASCADE)

class cart(models.Model):
    uid = models.ForeignKey(neonlogin,on_delete = models.CASCADE)
    pid = models.ForeignKey(products,on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    discounts = models.ForeignKey(coupens,on_delete = models.DO_NOTHING,default = '',null = True)
    less = models.FloatField(default = 0,blank =True)
    finalamt = models.FloatField(default = 0)

    def setfimalamt(self):
        self.finalamt = (self.pid.price * self.quantity) - self.less

class address(models.Model):
    uid = models.ForeignKey(neonlogin,on_delete = models.CASCADE)
    name = models.CharField(max_length = 50)
    phone = models.BigIntegerField()
    pincode = models.IntegerField()
    locality = models.CharField(max_length = 150)
    addres = models.CharField(max_length = 500)
    state = models.CharField(max_length = 60)
    city = models.CharField(max_length = 50)
    landmark = models.CharField(max_length = 50,default='')
    alternatephone = models.BigIntegerField(default=0)

    
class orders(models.Model):
    uid = models.ForeignKey(neonlogin,on_delete = models.CASCADE)
    pid = models.ForeignKey(products,on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    paymentMethod = models.CharField(max_length = 150)
    paymentId = models.CharField(max_length = 200)
    ShippingAddress = models.ForeignKey(address,on_delete = models.DO_NOTHING)
    orderStatus = models.CharField(max_length = 60)
    amount = models.FloatField()
    orderedtime = models.DateTimeField(default = datetime.now(), blank=True)
    discounts = models.ForeignKey(coupens,on_delete = models.DO_NOTHING,default = '',null = True)
    less = models.FloatField(default = 0,blank =True)


    def calcfinalamt(self):
        return (self.amount - self.less)

#Guest Cart

class guestcart(models.Model):
    uid = models.CharField(max_length=250)
    pid = models.ForeignKey(products,on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)