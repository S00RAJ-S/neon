from django.shortcuts import redirect
from neon.encryption import decrypt
from neonuser.models import neonlogin

def validationadmin(request):
    try:
        if request.session['email'] == request.COOKIES['email']:
            if decrypt(request.session['epass']) == decrypt(request.COOKIES['epass']) == decrypt(neonlogin.objects.get(email = request.session['email']).password):
                if request.session['id'] == 1:
                    return True
            else:
                return False
    except:
        return False
def validationusr(request):
    try:
        if request.session['email'] == request.COOKIES['email']:
            if decrypt(request.session['epass']) == decrypt(request.COOKIES['epass']) == decrypt(neonlogin.objects.get(email = request.session['email']).password):
                if request.session['id'] != 1 :
                    return True
            else:
                return False
    except:
        return False
def logoutuser(request):
    request.session.flush()
    ret = redirect('/login/')
    ret.delete_cookie('email')
    ret.delete_cookie('epass')
    return ret