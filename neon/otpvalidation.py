from django.shortcuts import *
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import random
from neonuser.models import neonlogin
from django.contrib import messages
from .guestcart_to_cart import guestcart_to_cart
import os
import dotenv

dotenv.read_dotenv()

def sendotp(request):
    if request.method == "POST":
        try:
            ph = int(request.POST.get('phone'))
            neonlogin.objects.get(phone = ph)
            account_sid = os.environ.get('account_sid')
            auth_token = os.environ.get('auth_token')
            client = Client(account_sid, auth_token)
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            request.session['ph'] = ph
            request.session.set_expiry(300)
            client.messages.create(body="Your OTP to Login to Your Account is {0}. The OTP is valid only for 5mins ".format(otp),from_='+19705008034',to='+918590203684')
            return render(request,"enterotp.html",{'phno':ph})
        except:
            messages.warning(request,"User does not exist with the Phone Number")
            return redirect('/lotp/')
    else:
        return redirect('/login/')


def valadatingotp(request):
    if request.method == "POST":
        try:
            otp1 = request.POST.get('otp1')        
            otp2 = request.POST.get('otp2')
            otp3 = request.POST.get('otp3')
            otp4 = request.POST.get('otp4')       
            otp = int(otp1+otp2+otp3+otp4) 
        except:
            messages.warning(request,"Enter valid OTP")
            return redirect('/')
        try:
            if otp == request.session['otp']:
                phone = request.session['ph']
                request.session.flush()
                d = neonlogin.objects.get(phone = phone)
                request.session['email'] = d.email
                request.session['epass'] = d.password
                request.session['id'] = d.id
                if d.id == 1:
                    ret = redirect('/admin/')
                    ret.set_cookie('email',d.email)
                    ret.set_cookie('epass',d.password)
                elif d.blocked == "F":
                    guestcart_to_cart(request)
                    ret = redirect('/user/')
                    ret.set_cookie('email',d.email)
                    ret.set_cookie('epass',d.password)
                else:
                    messages.info(request,"Admin Has Blocked!Contact Admin")
                    ret = redirect('/login/')
                return ret
            else:
                return redirect('/lotp/')
        except:
            messages.info(request,"OTP Expired. Try Again")
            return redirect('/lotp/')