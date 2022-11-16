from django.http import JsonResponse
from django.shortcuts import *
import razorpay
from neon.decorators import validationusr
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def PaymentGateway(request):
    if validationusr(request):
        if request.method == 'POST':
            p = request.POST.get('price')
            client = razorpay.Client(auth=("rzp_test_ZTRd7diWGDPbuQ", "MCIN87roPOXPSfJLtylJqqs7"))
            DATA = {
            "amount": p,
            "currency": "INR",
            # "receipt": "receipt#1",
            # "notes": {
            #     "key1": "value3",
            #     "key2": "value2"
            #     }
            }   
            Razorpay_order = client.order.create(data=DATA)
            Razorpay_order_id = Razorpay_order['id']            

            return JsonResponse({"order_id":Razorpay_order_id})
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')
