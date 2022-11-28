from django.shortcuts import *
from django.http import JsonResponse
import braintree
from django.contrib import messages


def paypalorderidgen(request):
    if request.method == 'POST':
        gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id="gqxpzs6zydhzgrqf",
            public_key="3m8jxf6sfg6hhdd7",
            private_key="0f6f0bdeced9eda6330992486b18bdb7"
        )
        )
        # pass client_token to your front-end
        #Including a customer_id when generating the client token lets returning customers select
        #from previously used payment method options, improving user experience over multiple checkouts
        # client_token = gateway.client_token.generate({
        #     "customer_id": a_customer_id
        # })
        client_token = gateway.client_token.generate({
            "customer_id": 472188472
        })
        # print("hello")
        # print(type(client_token))
        return JsonResponse({'client_token':client_token})
    else:
        return redirect('/')


def create_purchase(request):
    if request.method == "POST":
        amt = round(float(request.POST.get('price')),2)
        # Use payment method nonce here...
        gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    braintree.Environment.Sandbox,
                    merchant_id="gqxpzs6zydhzgrqf",
                    public_key="3m8jxf6sfg6hhdd7",
                    private_key="0f6f0bdeced9eda6330992486b18bdb7"
                )
                )
        result = gateway.transaction.sale({
            "amount": str(amt),
            "payment_method_nonce": request.POST.get('nonce'),
            # "device_data": device_data_from_the_client,
            "options": {
            "submit_for_settlement": True
            }
            })
        # print(result)
        # if result.is_success:
        #     # True

        #     transaction = result.transaction
        #     print(transaction)
        #     print(transaction.status)
        #     # "authorized"
        if result.is_success:
        # See result.transaction for details
            # print(result.transaction) 
            # print(result.transaction.id)  
            return JsonResponse({'status':'success','paypal_payment_id':result.transaction.id})
        else:
        # Handle errors
            print("error occured result")
            messages.warning(request,"Payment Not completed")
    else:
        return redirect('/')