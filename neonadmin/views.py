from django.http import JsonResponse
from django.shortcuts import *
from neon.decorators import *
from neon.pdfgenerator import render_to_pdf
from neonuser.models import *
from .models import *
from django.contrib import messages
from django.db.models import Count,Sum
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date



def adminhome(request):
    if validationadmin(request):
        dat = neonlogin.objects.get(id=1)
        cat = categories.objects.all()
        totalsale = orders.objects.filter(orderStatus = "Delivered").count()
        order = orders.objects.filter(orderStatus = "Delivered")
        dailyrevenue = orders.objects.values('orderedtime__date').annotate(amount = Sum('amount'))
        totalrevenue = 0
        for o in order:
            totalrevenue += (o.amount - o.less)
        datewiseorders = orders.objects.values('orderedtime__date').annotate(sales=Count('id')).order_by('-orderedtime__date')[:30]
        datewiseCancelledOrders = orders.objects.values('orderedtime__date').annotate(status=Count('id',filter = Q(orderStatus = 'Cancelled'))).order_by('-orderedtime__date') [:30]
        datewiseDeliveredOrders = orders.objects.values('orderedtime__date').annotate(status=Count('id',filter = Q(orderStatus = 'Delivered'))).order_by('-orderedtime__date') [:30]
        count = 0
        catrevenue = 0
        categorysales = []
        categoryrevenue = []
        for c in cat:
            count = 0
            catrevenue = 0
            for o in order:
                if c.category == o.pid.category_id.category:
                    count += 1
                    catrevenue += (o.amount - o.less)
            categorysales.append(count)
            categoryrevenue.append(catrevenue)
        # print(categorysales)
        # categorysales = orders.objects.values('pid','category_id','category',filter = Q(orderStatus = 'Delivered')).annotate(catsales = Count('id')).order_by('-orderedtime__date') [:30]
        # print(datewiserevenue)

        return render(request, 'admin/index.html', {'name': dat.name,'categories':cat,'orders':datewiseorders,'corders':datewiseCancelledOrders,'dorders':datewiseDeliveredOrders,'dailyrevenue':dailyrevenue,'totalsale':totalsale,'totalrevenue':totalrevenue,'categories':cat,'categorysales':categorysales,'catrevenue':categoryrevenue})
    else:
        return redirect('/login/')


def viewusers(request):
    if validationadmin(request):
        if request.method == "POST":        
            usort = request.POST.get('usort')
            dat = neonlogin.objects.all().order_by(usort).exclude(id=1)
        else:
            adminname = neonlogin.objects.get(id=1).name
            dat = neonlogin.objects.all().order_by('name').exclude(id=1)
        return render(request, 'admin/viewusers.html', {'name': adminname,'data': dat})
    else:
        return redirect('/login/')


def blockuser(request):
    if request.method == "POST":
        userid = request.POST.get('uid')
        neonlogin.objects.filter(id=userid).update(blocked='T')
        messages.success(request, "User Blocked")
        return redirect('/admin/viewusers/')


def unblockuser(request):
    if request.method == "POST":
        userid = request.POST.get('uid')
        neonlogin.objects.filter(id=userid).update(blocked='F')
        messages.success(request, "User Unblocked")
        return redirect('/admin/viewusers/')

# Category Management Views


def category(request):
    if validationadmin(request):
        adminname = neonlogin.objects.get(id=1).name
        data = categories.objects.all().order_by('category')
        return render(request, 'admin/category.html', {'name': adminname,"data": data})
    else:
        return redirect('/login/')


def addcategory(request):
    if validationadmin(request):
        if request.method == "POST":
            cat = request.POST.get('category')
            try:
                categories(category=cat).save()
                messages.success(request, "Category added Successfully")
            except:
                messages.warning(request, "Category Already Exist")
            return redirect('/admin/addcategory/')
        else:
            adminname = neonlogin.objects.get(id=1).name
            return render(request, 'admin/addcategory.html',{'name': adminname})
    else:
        return redirect('/login/')


def delcategory(request):
    if validationadmin(request):
        if request.method == "POST":
            cid = request.POST.get('cid')
            categories.objects.get(id=cid).delete()
            messages.success(request, "Category deleted Successfully")
            return redirect('/admin/category/')
    else:
        return redirect('/login/')

# End - Category Management Views

# SubCategory Management Views


def subcategory(request):
    if validationadmin(request):
        adminname = neonlogin.objects.get(id=1).name
        data = subcategories.objects.all().order_by('category_id')
        return render(request, 'admin/subcategory.html', {'name': adminname,"data": data})
    else:
        return redirect('/login/')


def addsubcategory(request):
    if validationadmin(request):
        if request.method == "POST":
            subcat = request.POST.get('subcategory')
            cat = request.POST.get('category')
            try:
                s = subcategories.objects.filter(category_id = cat)
                for i in s:
                    if i.subcategory == subcat:
                        raise Exception("Subcategory already Exist for the given Category")
                subcategories(category_id=categories(cat), subcategory=subcat).save()
                messages.success(request, "SubCategory added Successfully")
            except Exception as e:
                messages.warning(request, e)
            return redirect('/admin/addsubcategory/')
        else:
            adminname = neonlogin.objects.get(id=1).name
            cat = categories.objects.all()
            return render(request, 'admin/addsubcategory.html', {'name': adminname,"categories": cat})
    else:
        return redirect('/login/')


def delsubcategory(request):
    if validationadmin(request):
        if request.method == "POST":
            cid = request.POST.get('cid')
            subcategories.objects.get(id=cid).delete()
            messages.success(request, "Category deleted Successfully")
            return redirect('/admin/subcategory/')
    else:
        return redirect('/login/')

# End - SubCategory Management Views


# Product Management Views

def viewproducts(request):
    if validationadmin(request):
        if request.method == "POST":
            pid = request.POST.get('pid')
            products.objects.get(id = pid).delete()
            messages.success(request,'Product deleted Successfully')
            return redirect('/admin/products/')
        else:
            uid = request.session['id']
            name = neonlogin.objects.get(id = uid).name
            data = products.objects.all().order_by('name')
            return render(request,'admin/viewproducts.html',{"data":data,"name":name})
    else:
        return redirect('/login/')

def editproduct(request):
    if validationadmin(request):
        if request.method == "POST":
            pid = request.POST.get('pid')
            uid = request.session['id']
            name = neonlogin.objects.get(id = uid).name
            data = products.objects.get(id = pid)
            cat = categories.objects.all()
            return render(request,'admin/editproduct.html',{"data":data,"pid":pid,"categories":cat,"name":name})
    else:
        return redirect('/login/')

def editpdt(request):
    if validationadmin(request):
        if request.method == "POST":
            pid = request.POST.get('pid')
            name = request.POST.get('name')
            brand = request.POST.get('brand')
            model = request.POST.get('model')
            p = request.POST.get('price')
            category = request.POST.get('category')
            subcatid = request.POST.get('subcategory')
            if subcatid == None :
                subcatid = products.objects.get(id = pid).subcategory_id.id
            ram = request.POST.get('ram')
            rom = request.POST.get('rom')
            processor = request.POST.get('processor')
            display = request.POST.get('display')
            spec = request.POST.get('spec')

            pobj = products.objects.get(id = pid)
            img1 = request.FILES.get('img1')
            if img1 != None:
                pobj.img1 = img1
                pobj.save()
            img2 = request.FILES.get('img2')
            if img2 != None:
                pobj.img2 = img2
                pobj.save()

            img3 = request.FILES.get('img3')
            if img3 != None:
                pobj.img3 =  img3
                pobj.save()

            img4 = request.FILES.get('img4')
            if img4 != None:
                pobj.img4 = img4
                pobj.save()
                
            stock = request.POST.get('stock')
            products.objects.filter(id = pid).update(
                name = name,
                brand = brand,
                model_number = model, 
                price = p, 
                category_id = categories(category), subcategory_id = subcategories(subcatid),
                ram = ram, rom = rom, processor = processor, display = display, description = spec,stock = stock
                )
            messages.success(request,"Product Updated")
            return redirect('/admin/addproducts/')
        else:
            uid = request.session['id']
            name = neonlogin.objects.get(id = uid).name
            categ = categories.objects.all()
            return render(request,'admin/addproducts.html',{"categories":categ,"name":name})
    else:
        return redirect('/login/')

def addproducts(request):
    if validationadmin(request):
        if request.method == "POST":
            name = request.POST.get('name')
            brand = request.POST.get('brand')
            model = request.POST.get('model')
            p = request.POST.get('price')
            category = request.POST.get('category')
            subcatid = request.POST.get('subcategory')
            ram = request.POST.get('ram')
            rom = request.POST.get('rom')
            processor = request.POST.get('processor')
            display = request.POST.get('display')
            spec = request.POST.get('spec')
            img1 = request.FILES.get('img1')
            img2 = request.FILES.get('img2')
            img3 = request.FILES.get('img3')
            img4 = request.FILES.get('img4')
            stock = request.POST.get('stock')
            products(
                name = name,
                brand = brand,
                model_number = model, 
                price = p, 
                category_id = categories(category), subcategory_id = subcategories(subcatid),
                ram = ram, rom = rom, processor = processor, display = display, description = spec,
                img1 = img1,img2 = img2,img3 = img3,img4 = img4,
                stock = stock
                ).save()
            messages.success(request,"Product Added")
            return redirect('/admin/addproducts/')
        else:
            uid = request.session['id']
            name = neonlogin.objects.get(id = uid).name
            categ = categories.objects.all()
            return render(request,'admin/addproducts.html',{"categories":categ,"name":name})
    else:
        return redirect('/login/')

# End - Product Management Views

# Banner Management 

def banners(request):
    if validationadmin(request):
        adminname = neonlogin.objects.get(id=1).name
        images = banner.objects.all()
        return render(request,'admin/banner.html',{'name': adminname,"images":images})
    else:
        return redirect('/login/')


def uploadbanners(request):
    if validationadmin(request):
        if request.method == "POST":
            bannerimage = request.FILES.get('bannerimg')
            banner(img = bannerimage).save()
            return redirect('/admin/banner/')
    else:
        return redirect('/login/')
    

def deletebanners(request):
    if validationadmin(request):
        if request.method == "POST":
            bannerid = request.POST.get('bannerid')
            banner.objects.get(id = bannerid).delete()
            messages.success(request,"Banner Image Deleted Successfully")
            return redirect('/admin/banner/')
    else:
        return redirect('/login/')



#End Banner Management

def myorders(request):
    if validationadmin(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        if request.GET.get('filter'):
            orderobj = orders.objects.filter(orderStatus = request.GET.get('filter'))
            f = request.GET.get('filter')
        else:
            orderobj = orders.objects.all().order_by('-orderedtime')
            f = False
        orderpage = Paginator(orderobj,10   )
        try:
            pgno = request.GET.get('pgno')
        except:
            pgno = 1
        order = orderpage.get_page(pgno)
        count = []
        for i in range(1,(orderpage.num_pages+1)):
            count.append(i)
        return render(request,'admin/myorders.html',{'lastpage':count,'order': order,'name':name,'filter':f})         
    else:
        return redirect('/login/')

def changeorderstatus(request):
    if validationadmin(request):
        if request.method == 'POST':
            orders.objects.filter(id = request.POST.get('oid')).update(orderStatus = request.POST.get('ostatus'))
            return JsonResponse({'response':'success'})         
    else:
        return redirect('/login/')


#coupens

def viewcoupens(request):
    if validationadmin(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        c = coupens.objects.all()
        return render(request,'admin/viewcoupens.html',{'coupen':c,'name':name})         
    else:
        return redirect('/login/')


def addcoupens(request):
    if validationadmin(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        if request.method == 'POST':
            coupen = request.POST.get('coupencode')
            coupen = coupen.upper()
            discountp = request.POST.get('discount')
            discountl = request.POST.get('discountlimit')
            minamt = request.POST.get('minpurchase')
            coupens(
                code = coupen,
                discount = discountp,
                discount_limit = discountl,
                min_purchase_amt = minamt
            ).save()
            messages.success(request,'Coupen added successfully')
        return render(request,'admin/addcoupens.html',{'name':name})         
         
    else:
        return redirect('/login/')


def delcoupen(request):
    if validationadmin(request):
        if request.method == 'POST':
            cid = request.POST.get('cid')
            try:
                cartobj = cart.objects.filter(discounts = coupens.objects.get(id = cid).id)
                for c in cartobj:
                    c.discounts_id = None
                    c.save()
                    print(c.discounts)
                coupens.objects.get(id = cid).delete()
            except:
                coupens.objects.get(id = cid).delete()

            messages.success(request,'Coupen Successfully Deleted')
            return redirect('/admin/coupens/')
    else:
        return redirect('/login/')


#Offers

def addoffers(request):
    if validationadmin(request):
        if request.method == 'POST':
            offerfor = request.POST.get('offerfor')
            discount = request.POST.get('discount')
            dislimit = request.POST.get('discountlimit')
            if offerfor == 'category':
                offerforcat = request.POST.get('cat')
                try:
                    offers(
                        catid = categories( categories.objects.get(category = offerforcat).id ),
                        pid = None,
                        offer = discount,
                        max_limit = dislimit
                    ).save()
                    messages.success(request,"Added Successfully")
                except:
                    messages.warning(request,'Offer Already Exist')
            elif offerfor == 'product':
                offerforpdt = request.POST.get('pdt')
                offerforcat = None
                try:
                    offers(
                        catid = None,
                        pid = products( products.objects.get(name =  offerforpdt).id ),
                        offer = discount,
                        max_limit = dislimit
                    ).save()
                    messages.success(request,"Added Successfully")
                except:
                    messages.warning(request,'Offer Already Exitst')
            return redirect('/admin/addoffers/')
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        return render(request,'admin/addoffers.html',{'name':name})
    else:
        return redirect('/login/')


def catorpdt(request):
    if validationadmin(request):
        s = request.GET.get('sel')
        if s == 'category':
            cat = categories.objects.all()
            return render(request,'admin/categoryorpdt.html',{'cat':cat})
        elif s == 'product':
            p = products.objects.all()
            return render(request,'admin/categoryorpdt.html',{'p':p})
    else:
        return redirect('/login/')

def viewoffers(request):
    if validationadmin(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        offerz = offers.objects.all()
        return render(request,'admin/viewoffers.html',{'name':name,'offers':offerz})
    else:
        return redirect('/login/')

def deloffers(request):
    if validationadmin(request):
        if request.method == 'POST':
            oid = request.POST.get('oid')
            offers.objects.get(id = oid).delete()
            messages.success(request,'Offer Successfully Deleted')
            return redirect('/admin/offers/')
    else:
        return redirect('/login/')


#Download Sales Report

def downloadsalesreport(request):
    if validationadmin(request):
        search = request.GET.get('search')
        orderobj = orders.objects.filter(orderStatus = search).order_by('-orderedtime')[:100]
        t = request.GET.get('type')
        salesreport = render_to_pdf('downloads/reports.html',{'orderobj':orderobj})
        if salesreport:
            if t == 'view':
                return salesreport
            elif t == 'download':
                filename = "attachment; filename=Invoice{}.pdf".format(0)
                salesreport['Content-Disposition'] = filename
                return salesreport
    else:
        return redirect('/login/')


def salesreport(request):
    if validationadmin(request):
        userid = request.session['id']
        name = neonlogin.objects.get(id = userid).name
        return render(request,'admin/salesreport.html',{'name':name})        
    else:
        return redirect('/login/')

def genreport(request):
    if validationadmin(request):
        fromdate = parse_date(request.GET.get('from'))
        todate = parse_date(request.GET.get('to'))
        if fromdate > todate:
            return HttpResponse("Select a Valid Date Range")
        else:
            print((todate-fromdate).days)            
            o = orders.objects.filter(orderedtime__lte = todate).filter(orderedtime__gte = fromdate).filter(orderStatus = "Delivered").order_by('orderedtime')
            if o == None:
                o = None
            return render(request,'admin/genreport.html',{'orders':o})
    else:
        return redirect('/login/')