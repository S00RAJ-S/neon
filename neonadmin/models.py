from django.db import models

class categories(models.Model):
    category = models.CharField(max_length = 50,unique = True)


class subcategories(models.Model):
    category_id = models.ForeignKey(categories,on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=60)


class products(models.Model):
    name = models.CharField(max_length = 60)
    brand = models.CharField(max_length = 60)
    model_number = models.CharField(max_length = 60)
    price = models.FloatField()
    category_id = models.ForeignKey(categories,on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(subcategories,on_delete=models.CASCADE)
    ram = models.CharField(max_length=10,default='null')
    rom = models.CharField(max_length=10,default='null')
    processor = models.CharField(max_length=50,default='null')
    display = models.CharField(max_length=60,default='null')
    description = models.CharField(max_length = 500)
    stock = models.BigIntegerField()
    img1 = models.ImageField(upload_to="products/")
    img2 = models.ImageField(upload_to="products/")
    img3 = models.ImageField(upload_to="products/")
    img4 = models.ImageField(upload_to="products/")

    #Call this function to get the offered Price (Returns Offered Price)

    def calcofferprice(self):
        offerz = offers.objects.all()
        for o in offerz:
            try:
                if self.category_id == o.catid:
                    catoffer = o.offer
                    catlimit = o.max_limit
                    catofferprice = self.price * (catoffer/100)
                    if catofferprice > catlimit:
                        catofferprice = catlimit
            except:
                pass
            try:
                if o.pid.id == self.id :
                    poffer = o.offer
                    plimit = o.max_limit
                    pdtofferprice = self.price * (poffer/100)
                    if pdtofferprice > plimit:
                        pdtofferprice = plimit
            except:
                pass
        try:
            if catofferprice and pdtofferprice:
                if catofferprice > pdtofferprice:
                    finaloffer = catofferprice
                else:
                    finaloffer = pdtofferprice      
            return round((self.price - finaloffer),2)
        except:
            try:
                return round((self.price - catofferprice),2)
            except:
                try:
                    return round((self.price - pdtofferprice),2)
                except:
                    return None



class banner(models.Model):
    img = models.ImageField(upload_to = "banner/")


class coupens(models.Model):
    code = models.CharField(max_length = 60)
    discount = models.BigIntegerField()
    discount_limit = models.BigIntegerField()
    min_purchase_amt = models.BigIntegerField()


class offers(models.Model):
    catid = models.OneToOneField(categories,on_delete = models.CASCADE,null = True)
    pid = models.OneToOneField(products,on_delete = models.CASCADE,null = True)
    offer = models.FloatField()
    max_limit = models.FloatField()