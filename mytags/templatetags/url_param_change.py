import json
from django import template

register = template.Library()

# @register.simple_tag(name='urlparam')
# def test(a,b):
#     # print(context)
#     # print('asdf')
#     # return products.objects.count()
#     return a+b

@register.simple_tag(name='urlparam')
def test(request,key,value):
    d = request.GET.copy()

    # for k,val in d.items():
    #     if k != key and val != value:
    #         d[key] = value
    d[key]=str(value)
    # print(d)
    url = request.path
    genurl = url
    c = 0
    for k,val in d.items():
        if c<1:
            genurl += '?'+k+'='+val   
            c = 1     
        else:
            genurl += '&'+k+'='+val        

    # print(genurl)
    return genurl

@register.filter(is_safe=True)
def js(obj):
    return json.dumps(obj)