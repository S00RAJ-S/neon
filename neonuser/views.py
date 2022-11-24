from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import *
from django.views.decorators.cache import never_cache
from neonuser.models import *
from neonadmin.models import categories, products, banner, coupens
from django.contrib import messages
from neon.encryption import encrypt,decrypt
from neon.decorators import *
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from neon.pdfgenerator import render_to_pdf


@never_cache
def signup(request):
    if validationadmin(request):
        return redirect('/admin/')
    elif validationusr(request):
        return redirect('/user/')    
    else:
        return render(request,'signup.html')

@never_cache
def signupuser(request):
    if request.method == 'POST':
            e = request.POST.get('email')
            n = request.POST.get('name')
            pas = request.POST.get('password')
            password = encrypt(pas)
            phone = request.POST.get('phone')
            try:
                neonlogin(name=n,email=e,password=password,phone=phone).save()
                messages.success(request,'Account Created Successfully')
                return redirect('/login/')    
            except:
                messages.warning(request,'User Already Exist')
                return redirect('/user/signup/')
        
@never_cache
def userhome(request):
    if validationusr(request):
        uid = request.session['id']
        name = neonlogin.objects.get(id = uid).name
        cat = categories.objects.all()
        pdt = products.objects.all()
        b = banner.objects.all()
        cartcount = cart.objects.filter(uid = uid).count()
        return render(request,'user/index.html',{"name":name,"categories":cat,"products":pdt,"cartcount":cartcount,"banner":b})
    else:
        return redirect('/login/')


# Wishlist Views

def AddToWishlist(request,productid):
    if validationusr(request):
        userid = request.session['id']
        try:
            wishlist.objects.get(uid = userid,pid = productid)
            messages.warning(request,"Product Already Exist in Wishlist")
        except: 
            wishlist(uid = neonlogin(userid), pid = products(productid)).save()
            messages.success(request,"Product added to wishlist")
        return redirect('/user/')
    else:
        return redirect('/login/')

def Wishlist(request):
    if validationusr(request):
        now = timezone.now()
        # print(now)
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        try:
            w = wishlist.objects.filter(uid = userid)
            if w.count() == 0:
                raise Exception("Your Wishlist is Empty")
            else:
                cartcount = cart.objects.filter(uid = userid).count()
                ret = render(request,"user/wishlist.html",{"w":w,"cartcount":cartcount,"name":name})
        except Exception as e: 
            messages.info(request,e)
            ret = redirect('/user/')
        return ret
    else:
        return redirect('/login/')

def DelWishlist(request):
    if validationusr(request):
        if request.method == "POST":
            wlistid = request.POST.get('delid')
            try:
                wishlist.objects.get(id = wlistid).delete()
                messages.success(request,"Product deleted from Wishlist")
            except:
                messages.info(request,"Sorry")
            return redirect('/user/wishlist/')
    else:
        return redirect('/login/')

#End - Wishlist Views


#Cart Views

def AddToCart(request,productid):
    if validationusr(request):
        userid = request.session['id']
        try:
            cart.objects.get(uid = userid,pid = productid)
            messages.warning(request,"Product Already Exist in Cart")
        except: 
            if products.objects.get(id = productid).stock < 1 :
                qty = 0
            else:
                qty = 1
            cart(uid = neonlogin(userid), pid = products(productid),quantity = qty).save()
            messages.success(request,"Product added to Cart")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/login/')

@never_cache
def Cart(request):
    if validationusr(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        try:
            c = cart.objects.filter(uid = userid)
            cartcount = cart.objects.filter(uid = userid).count()
            price = 0
            for i in c:
                stock = i.pid.stock
                if i.quantity > stock:
                    cart.objects.filter(id = i.id).update(quantity = stock)
                # print(i.pid.calcofferprice())
                try:
                    price += round((i.pid.calcofferprice() * i.quantity),2)
                except:
                    price += (i.pid.price * i.quantity)
            if cartcount == 0:
                raise Exception("Cart is Empty")
            else:
                if price > 500:
                    s = 0
                else:
                    s = 40
                availablecoupens = coupens.objects.all()
                usercart = cart.objects.filter(uid = userid)
                ret = render(request,"user/cart.html",{"w":usercart,"cartcount":cartcount,"name":name,"price":price,"total":price+s,"s":s,'coupens':availablecoupens})
        except Exception as e: 
            messages.info(request,e)
            ret = redirect('/user/')
        return ret
    else:
        return redirect('/login/')

def DelCart(request):
    if validationusr(request):
        if request.method == "POST":
            cartid = request.POST.get('delid')
            try:
                cart.objects.get(id = cartid).delete()
                messages.success(request,"Product deleted from Cart")
            except:
                messages.info(request,"Sorry")
            return redirect('/user/cart/')
    else:
        return redirect('/login/')

def updateqty(request):
    if validationusr(request):
        userid = request.session['id']
        o = int(request.POST.get('o'))
        q = request.POST.get('pdtid')
        pid = cart.objects.get(id = q).pid
        stok = pid.stock
        if stok < 1:
            qty = 0
        else:
            if o == 0:
                qty = cart.objects.get(id = q).quantity
                if qty > 1:
                    c = cart.objects.filter(uid = userid)
                    try:
                        for i in c:
                            i.discounts = None
                            i.less = 0
                            i.save()      
                            i.setfimalamt()
                    finally:
                        qty -=1
            elif o == 1:
                qty = cart.objects.get(id = q).quantity
                if stok > qty:
                    c = cart.objects.filter(uid = userid)
                    try:
                        for i in c:
                            i.discounts = None
                            i.less = 0
                            i.save()      
                            i.setfimalamt()
                    finally:
                        qty +=1
            cart.objects.filter(id = q).update(quantity = qty)
            c = cart.objects.filter(uid = userid)
            price = 0
            for i in c:
                if i.pid.calcofferprice():
                    price += round((i.pid.calcofferprice() * i.quantity),2)
                else:
                    price += round((i.pid.price * i.quantity),2)
            if price > 500:
                s = 0
            else:
                s = 40
        return JsonResponse({'qty':qty,'price':price,'s':s})


def cei(request):
    if validationusr(request):
        if request.method == 'POST':
            userid = request.session['id']
            c = cart.objects.filter(uid = userid)
            for i in c:
                if i.quantity == 0:
                    raise Exception("Out of Stock")
                else:
                    return JsonResponse({'response':'success'})
    else:
        return redirect('/login/')

@never_cache
def checkout(request):
    if validationusr(request):
        try:
            cartss = cart.objects.filter(uid = request.session['id'])
            if cartss:
                pass
            else:
                raise Exception('')
        except:
            return redirect('/user/myorders/')
        userid = request.session['id']
        c = cart.objects.filter(uid = userid)
        for i in c:
            if i.quantity == 0:
                qty = 0
                break
            else:
                qty = 1
        if qty == 0:
            return redirect('/user/cart/')
        elif qty == 1:
            name = neonlogin.objects.get(id = userid).name
            try:
                a = address.objects.filter(uid = userid)
                cartcount = cart.objects.filter(uid = userid).count()
                price = 0
                less = 0
                coupencode = False
                for i in c:
                    try:
                        price += (i.pid.calcofferprice() * i.quantity)
                    except:
                        price += (i.pid.price * i.quantity)
                    try:
                        less += i.less
                        coupencode = i.discounts.code
                    except:
                        pass
                if cartcount == 0:
                    raise Exception("Cart is Empty")
                else:
                    if price > 500:
                        s = 0
                    else:
                        s = 40
                    ret = render(request,"user/checkout.html",{"a":a,"cartcount":cartcount,"name":name,"price":price,"total":round((price+s-less),2),"s":s,'less':less,'coupen':coupencode})
            except Exception as e: 
                messages.info(request,e)
                ret = redirect('/user/')
            return ret
    else:
        return redirect('/login/')

    
#Applying coupen code
def applycoupen(request):
    if validationusr(request):
        if request.method == 'GET':
            userid = request.session['id']
            coupen = request.GET.get('code')
            coupen = coupen.upper()
            try:
                coupencode = coupens.objects.get(code = coupen)
                c = cart.objects.filter(uid = userid)
                price = 0
                for i in c:
                    try:
                        price += (i.pid.calcofferprice() * i.quantity)
                    except:
                        price += (i.pid.price * i.quantity)
                    # product_price = (i.pid.price) * (i.quantity)
                    # price += product_price
                discount = price * (coupencode.discount/100)
                if (discount <= coupencode.discount_limit) and price > coupencode.min_purchase_amt:
                    for i in c:
                        p_price = 0
                        try:
                            p_price += (i.pid.calcofferprice() * i.quantity)
                        except:
                            p_price += (i.pid.price * i.quantity)
                        # p_price = (i.pid.price) * (i.quantity) 
                        dis = round(p_price * (coupencode.discount/100),2) 
                        i.less = dis
                        i.discounts = coupencode                  
                        i.save()
                        i.setfimalamt()
                    return JsonResponse({"status":"success","message": "Coupen Code applied Successfully"})
                elif price >= coupencode.min_purchase_amt:
                    return JsonResponse({'less':coupencode.discount_limit,'finalamt':(price - coupencode.discount_limit)})
                elif price < coupencode.min_purchase_amt:
                    mesage = ("Requirement Not met:Minimum purchase of ₹{} Required").format(coupencode.min_purchase_amt)
                    return JsonResponse({"status":"error","message": mesage})
            except:
                pass
    else:
        return redirect('/login/')


def removecoupen(request):
    if validationusr(request):
        userid = request.session['id']
        c = cart.objects.filter(uid = userid)
        try:
            for i in c:
                i.discounts = None
                i.less = 0
                i.save()      
                i.setfimalamt()

            return redirect('/user/checkout/') 
        except:
            messages.info('No coupen code Exist')
            return redirect('/login/')

    else:
        return redirect('/login/')   


def userordercreation(request):
    if validationusr(request):
        if request.method == "POST":
            userid = request.session['id']
            pmethod = request.POST.get('paymentmethod')
            paymentid = request.POST.get('paymentid')
            crt = cart.objects.filter(uid = userid)
            adid = request.POST.get('address')
            ad = address.objects.get(id = adid).id
            for items in crt:
                pdtid = items.pid
                price = pdtid.price
                qty = items.quantity
                try:
                    offerprice = pdtid.calcofferprice()
                    amt = offerprice * qty
                except:
                    amt = qty*price
                try:
                    coupenobj = items.discounts
                    discountamt = items.less
                except:
                    coupenobj = None
                    discountamt = 0
                orders(
                    uid = neonlogin(userid),
                    pid = products(pdtid.id),
                    quantity = qty,
                    paymentMethod = pmethod,
                    paymentId = paymentid,
                    ShippingAddress = address(ad),
                    orderStatus = "Order Placed",
                    amount = amt,
                    discounts = coupenobj,
                    less = discountamt
                    ).save()
                p = products.objects.filter(id = pdtid.id)
                for i in p:
                    stok = i.stock
                # print(stok,qty)
                p.update(stock = (stok - qty))
                cart.objects.get(id = items.id).delete()
            return JsonResponse({"response":"Success"})
    else:
        return redirect('/login/')   


def myorders(request):
    if validationusr(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        cartcount = cart.objects.filter(uid = userid).count()
        order = orders.objects.filter(uid = userid).order_by('-orderedtime')
        try:
            pgno = request.GET.get('pgno')
        except:
            pgno = 1
        p = Paginator(order,5)
        paginatedorder = p.get_page(pgno)
        count = []
        for i in range(1,(p.num_pages+1)):
            count.append(i)
        return render(request,'user/myorders.html',{'lastpage':count,'order': paginatedorder,"cartcount":cartcount,"name":name})         
    else:
        return redirect('/login/')

def returnpdt(request):
    if validationusr(request):
        if request.method == 'POST':
            order = orders.objects.get(id = request.POST.get('oid'))
            order.orderStatus = 'Returned'
            pdt = products.objects.get(id = order.pid.id)
            pdt.stock += order.quantity
            pdt.save()
            order.save()
            return JsonResponse({'response':'success'})    
    else:
        return redirect('/login/')

#Download Invoice

def downloadinvoice(request):
    if validationusr(request):
        oid = request.GET.get('orderid')
        orderobj = orders.objects.filter(id = oid)
        invoice = render_to_pdf('downloads/invoice.html',{'orderobj':orderobj})
        if invoice:
            if request.GET.get('option') == 'view':
                return invoice   
            elif request.GET.get('option') == 'download':
                filename = "attachment; filename=Invoice{}.pdf".format(oid)
                invoice['Content-Disposition'] = filename
                return invoice
        else:
            return HttpResponse("Invoice Not Found")
    else:
        return redirect('/login/')

def cancelorder(request):
    if validationusr(request):
        if request.method == 'POST':
            oid = request.POST.get('oid')
            orders.objects.filter(id = oid).update(orderStatus = 'Cancelled')
            return JsonResponse({'response':'working'})

        # userid = request.session['id']
        # name = neonlogin.objects.get(id = userid).name
        # cartcount = cart.objects.filter(uid = userid).count()
        # order = orders.objects.filter(uid = userid).order_by('-orderedtime')
        # return render(request,'user/myorders.html',{'order': order,"cartcount":cartcount,"name":name})         
    else:
        return redirect('/login/')

def SinglePageProduct(request,pid):
    try:
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        cartcount = cart.objects.filter(uid = userid).count()
    except:
        cartcount = False
        name = False
    try:
        pdt = products.objects.get(id = pid)
        return render(request,"user/Single-Product-Page.html",{"product":pdt,"cartcount":cartcount,"name":name})
    except:
        return redirect('/')
    # if request.method == "POST":
    #     cartid = request.POST.get('delid')
    #     try:
    #         cart.objects.get(id = cartid).delete()
    #         messages.success(request,"Product deleted from Cart")
    #     except:
    #         messages.info(request,"Sorry")
    #     return redirect('/user/cart/')



#Address views

def myaddress(request):
    if validationusr(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        cartcount = cart.objects.filter(uid = userid).count()
        ad = address.objects.filter(uid = userid)
        return render(request,"user/myaddress.html",{"cartcount":cartcount,"name":name,"ad":ad})
    else:
        return redirect('/login/')
    
def addAddress(request):
    if validationusr(request):
        if request.method == "POST":
            userid = request.session['id']
            name = request.POST.get('name')
            phone =request.POST.get('mobno')
            pincode = request.POST.get('pincode')
            locality = request.POST.get('locality')
            addres = request.POST.get('address')
            state = request.POST.get('state')
            city = request.POST.get('city')
            landmark = request.POST.get('landmark')
            alternatephone = request.POST.get('amobno')
            if alternatephone == '':
                alternatephone = 0
            try:
                address(
                        uid = neonlogin(userid),
                        name = name,
                        phone = phone,
                        pincode = pincode,
                        locality = locality,
                        addres = addres,
                        state = state,
                        city = city,
                        landmark = landmark,
                        alternatephone = alternatephone,
                ).save()
                messages.success(request,"Address saved Successfully")
            except:
                messages.warning(request,"Something Went Wrong")
            return redirect('/user/myaddress/')
    else:
        return redirect('/login/')

@never_cache
def myprofile(request):
    if validationusr(request):
        userid = request.session['id']
        user = neonlogin.objects.get(id = userid)
        cartcount = cart.objects.filter(uid = userid).count()
        return render(request,"user/userprofile.html",{"cartcount":cartcount,"user":user})
    else:
        return redirect('/login/')

def changepassword(request):
    if validationusr(request):
        if request.method == "POST":
            userid = request.session['id']
            oldpass = request.POST.get('oldpass')
            newpass = request.POST.get('newpass')
            user = neonlogin.objects.get(id = userid)
            if decrypt(user.password) == oldpass:
                user.password = encrypt(newpass)
                user.save()
                res = {"response":"Password Changed Successfully"}
            else:
                res = {"response":"Your Old Password is not matching"}
            return JsonResponse(res)
    else:
        return redirect('/login/')


def updateprofile(request):
    if validationusr(request):
        if request.method == 'POST':    
            userid = request.session['id']
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            user = neonlogin.objects.get(id = userid)
            user.name = name
            user.email = email
            user.phone = phone
            user.save()
            return JsonResponse({'response':'Successfully Updated'})
    else:
        return redirect('/login/')



def search(request):
    try:
        pgno = request.GET.get('pgno')
    except:
        pgno = 1
    try:
        userid = request.session['id']
        user = neonlogin.objects.get(id = userid).name
        cartcount = cart.objects.filter(uid = userid).count()
    except:
        cartcount = False
        user = False
    q = request.GET.get('query')
    cc = categories.objects.filter(Q(category__icontains = q))
    lis = [x for x in cc]
    # print(q)
    #searching quries
    try:
        sort = request.GET.get('sort')
        min = request.GET.get('min')
        max = request.GET.get('max')
        if sort == 'htl':
            s = '-price'
        elif sort == 'lth':
            s = 'price'
        else:
            raise Exception('')

        searchresult =[i for i in products.objects.filter(Q(name__icontains = q) | Q(brand__icontains = q) | Q(description__icontains = q) | Q(category_id__in = lis)).order_by(s)]
        torem =[]
        # print(max,min)
        try:
            # print('MIN')
            if min is not None:
                for s in searchresult:
                    if s.price < int(min):
                        torem.append(s)
        except:
            pass

        try:
            # print('MAX')
            if max is not None:
                for s in searchresult:
                    if s.price > int(max):
                        torem.append(s)
        except:
            pass


        for item in torem:
            for se in searchresult:
                if item == se:
                    searchresult.remove(se)

                    
        # c = categories.objects.filter(category__icontains = q)
        # searchincategory = []
        # for cat in c:
        #     p = products.objects.filter(category_id = cat).order_by(s)
        #     for x in p:
        #         searchincategory.append(x)
        # finaldata = []
        # finaldata.extend(searchresult)
        # for fd in finaldata:
        #     for d in searchincategory:
        #         if fd == d :
        #             searchincategory.remove(d)
        # # finaldata.append(searchincategory)
        # for dis in finaldata:
        #     print(dis.price)
    except:
        searchresult =[i for i in products.objects.filter(Q(name__icontains = q) | Q(brand__icontains = q) | Q(description__icontains = q) | Q(category_id__in = lis))]
        

        #----- Method First Tried ------#
        # searchresult =[i for i in products.objects.filter(Q(name__icontains = q) | Q(brand__icontains = q) | Q(description__icontains = q))]
        # c = categories.objects.filter(category__icontains = q)
        # searchincategory = []
        # for cat in c:
        #     p = products.objects.filter(category_id = cat)
        #     for x in p:
        #         searchincategory.append(x)
        # finaldata = []
        # finaldata = list(set(searchincategory + searchresult))
    #searching quries ends
    maxprice = 0
    for m in products.objects.all():
        if m.price > maxprice:
            maxprice = m.price
    # for x in finaldata:
    #     print(x.price)
    r1 = Paginator(searchresult,4)
    r = r1.get_page(pgno)
    count = []
    for i in range(1,(r1.num_pages+1)):
        count.append(i)
    return render(request,'user/searchresult.html',{"cartcount":cartcount,"name":user,'result':r,'lastpage':count,'query':q,'maxprice':maxprice})
    # except:
    #     r1 = Paginator(searchresult,4)
    #     r = r1.get_page(pgno)
    #     count = []
    #     for i in range(1,(r1.num_pages+1)):
    #         count.append(i)
    #     print("inside except")
    #     return render(request,'user/searchresult.html',{"cartcount":cartcount,"name":user,'result':r,'lastpage':count,'query':q})

    
#2FA
import pyotp
from django.conf import settings
from qrcode import *

def enable2fa(request):
    if validationusr(request):
        if request.method == "POST":
            u = neonlogin.objects.get(id = request.session['id'])
            userkey = pyotp.random_base32()
            qr = pyotp.totp.TOTP(userkey).provisioning_uri(name=u.name, issuer_name='Neon')
            qrimg = make(qr)
            img_name = str(u.id) + '.png'
            qrimg.save(str(settings.MEDIA_ROOT) + '/auth/' + img_name)
            u.twofakey = userkey
            u.twofa = 'T'
            u.save()
            return render(request,'user/showqr.html',{'qrimg':img_name})
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
