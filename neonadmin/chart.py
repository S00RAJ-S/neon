from django.http import JsonResponse
from django.shortcuts import *
from neon.decorators import validationadmin
from .models import *
from neonuser.models import *

def catorderqty(request,catid):
    if validationadmin(request):
        # dat = neonlogin.objects.get(id=1)
        cat = categories.objects.get(id = catid)
        order = orders.objects.all()
        count = 0
        for o in order:
            if o.pid.category_id.category == cat.category:
                count += 1

        return JsonResponse({'count':count})
    else:
        return redirect('/login/')