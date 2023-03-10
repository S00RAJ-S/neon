from django.shortcuts import *
from django.http import JsonResponse
import braintree,os,dotenv
from django.contrib import messages

dotenv.read_dotenv()

def paypalorderidgen(request):
    if request.method == 'POST':
        gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=os.environ.get('merchant_id'),
            public_key=os.environ.get('public_key'),
            private_key=os.environ.get('private_key')
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
                    merchant_id=os.environ.get('merchant_id'),
                    public_key=os.environ.get('public_key'),
                    private_key=os.environ.get('private_key')
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