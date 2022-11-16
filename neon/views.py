from django.http import JsonResponse
from django.shortcuts import *
from neonuser.models import neonlogin
from django.contrib import messages
from django.views.decorators.cache import never_cache
from neon.encryption import decrypt
from neon.decorators import *
from neonadmin.models import products,categories,banner


def landingpage(request):
    if validationadmin(request):
        return redirect('/admin/')
    elif validationusr(request):
        return redirect('/user/')
    else:
        cat = categories.objects.all()
        pdt = products.objects.all()
        b = banner.objects.all()
        return render(request,'landingpage.html',{"categories":cat,"products":pdt,"banner":b})

@never_cache
def myloginfn(request):
    if validationadmin(request):
        return redirect('/admin/')
    elif validationusr(request):
        return redirect('/user/')
    else:
        return render(request,'login.html')
    
    
def loginv(request):
    if request.method == 'POST':
            email = request.POST.get('email')
            enteredpassword = request.POST.get('pass')
            try:
                d = neonlogin.objects.get(email=email)
                # print(d.blocked)
                encryptedpassword = d.password
                password = decrypt(encryptedpassword)
                if enteredpassword == password:
                    request.session['email'] = email
                    request.session['epass'] = encryptedpassword
                    request.session['id'] = d.id
                    if d.id == 1:
                        ret = redirect('/admin/')
                        ret.set_cookie('email',email)
                        ret.set_cookie('epass',encryptedpassword)
                    elif d.blocked == "F":
                        if d.twofa == "T":
                            return render(request,'user/entertotp.html')
                        else:
                            ret = redirect('/user/')
                            ret.set_cookie('email',email)
                            ret.set_cookie('epass',encryptedpassword)
                    else:
                        messages.info(request,"Admin Has Blocked!Contact Admin")
                        ret = redirect('/login/')
                    return ret
                else:
                    messages.warning(request,'Credentials are Not matched')
                    return redirect('/login/')
            except:
                messages.warning(request,'User is Not registered')
                return redirect('/login/')

import pyotp
def validatetotp(request):
    if request.method == "POST":
        enteredTOTP = request.POST.get('totp')
        e = request.session['email']
        p = request.session['epass']
        u = neonlogin.objects.get(email = e)
        totp = pyotp.TOTP(u.twofakey)
        if totp.verify(enteredTOTP):
            ret = redirect('/user/')
            ret.set_cookie('email',e)
            ret.set_cookie('epass',p)
            return ret
    else:
        return('/')

@never_cache
def lotp(request):
    if validationadmin(request):
        return redirect('/admin/')
    elif validationusr(request):
        return redirect('/user/')
    else:
        return render(request,'lotp.html')

def logoutusr(request):
    return logoutuser(request)
