from django.shortcuts import *
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import random
from neonuser.models import neonlogin
from django.contrib import messages

# Find your Account SID and Auth Token in Account Info
# and set the environment variables. See http://twil.io/secure
# account_sid = 'AC3fbf6eb6e3e9f5ccacfc98f8bab1c5ce'
# auth_token = '97b33b574d5c95b22b5bac3bb1971c05'
# client = Client(account_sid, auth_token)

# message = client.messages.create(body='Hi there',from_='+19705008034',to='+918547455343')
# print(message.sid)
                    


def sendotp(request):
    if request.method == "POST":
        try:
            ph = int(request.POST.get('phone'))
            neonlogin.objects.get(phone = ph)
            account_sid = 'AC3fbf6eb6e3e9f5ccacfc98f8bab1c5ce'
            auth_token = '97b33b574d5c95b22b5bac3bb1971c05'
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