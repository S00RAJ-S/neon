from .models import *
from neon.decorators import *
from django.shortcuts import *


def subcat(request,subcategoryid):
    subcateg = subcategories.objects.filter(category_id = subcategoryid)
    return render(request,'admin/showsubcat.html',{"subcategories":subcateg})

