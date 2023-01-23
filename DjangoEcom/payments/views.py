import stripe
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.conf import settings
from account.models import Order,Order_Item


from account.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        prod_id=self.kwargs["pk"]
        try:
            cart=Cart_products.objects.get(cart_id=prod_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'inr',
                            
                             'unit_amount':int(cart.product_id.price) * 100,
                             'product_data':{
                                 'name':cart.product_id.name,
                             }
                        },
                        'quantity': 1, 
                    },
                ],
                metadata={
                    "cart_id":cart.cart_id,
                    "cart_product":cart.product_id.pk
                    
                },
                mode='payment',
                success_url=settings.SITE_URL + '?success=true',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'Message':'Something went wrong while creating stripe session','error':str(e)}, status=500)




@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)
        customer_email=session['customer_details']['email']
        prod_id=session['metadata']['product_id']
        amount = session['amount_total']
        product=Product.objects.get(id=prod_id)
        #sending confimation mail
        

        # #creating payment history
        user=User.objects.get(email=customer_email)
        print(user)
        cart_id = Cart.objects.get(user=user.pk,is_active=True)
        print(cart_id)
        product=Cart_products.objects.get(product_id=product)
        print(product)
        product = Product.objects.get(id=product)
        order= Order.objects.create(cart_id=user, is_paid=True)
        Order_Item.objects.create(order_id=order,user_detail_id=user,
            product=product,total_amount=(amount/100))
        # product.stock_quantity -= products.quantity
        # product.save()
        # cart_products = Cart_products.objects.filter(cart_id=cart_id)
        # for cart_product in cart_products:
        #     cart_product.is_paid = True
        #     cart_product.save()
        # # user.cart.is_active = False
        # # user.cart.save()
        # cart_id.is_active=False
        # cart_id.save()
        # Cart.objects.create(user_id=user, is_active=True)


    return HttpResponse(status=200)