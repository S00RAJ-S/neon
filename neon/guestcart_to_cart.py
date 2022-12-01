from neonuser.models import guestcart,cart,neonlogin
from neonadmin.models import products
from django.contrib import messages

def guestcart_to_cart(request):
    try:
        device = request.COOKIES['device']
        userid = neonlogin(request.session['id'])
        gc = guestcart.objects.filter(uid = device)
        for c in gc:
            try:
                cart.objects.get(uid = userid,pid = c.pid.id)
                # messages.warning(request,"Product Already Exist in Cart")
            except: 
                if products.objects.get(id = c.pid.id).stock < 1 :
                    qty = 0
                else:
                    qty = 1
                cart(uid = userid, pid = products(c.pid.id),quantity = qty).save()
                # print('nearcart')
                # messages.success(request,"Product added to Cart")
        guestcart.objects.filter(uid = device).delete()
        return True
    except:
        return False