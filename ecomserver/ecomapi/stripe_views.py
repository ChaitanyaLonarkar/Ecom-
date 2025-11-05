from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from ecomserver.settings import STRIPE_API_KEY, STRIPE_SECRET_KEY
from django.conf import settings

from .serializers import CartSerializer
from .stripe_serializer import CardInformationSerializer
import stripe
from .models import CartItem, PaymentDetails, Product, Cart


class PaymentAPI(APIView):

   
    # stripe.api_key = settings.STRIPE_API_KEY

    domain_url = 'http://localhost:8000/'

    def post(self, request):
        try:
            # get product details here
            user= request.user
            print(settings.STRIPE_API_KEY,"dfasdfsdfsadfasdfasdfasdfasdfasdf")
            carts= Cart.objects.get(user=user)

            # print(user,"dfasdf")
            # print("cartid", carts.id)
            cart = CartItem.objects.all().filter(cart=carts.id)
            
            serializer=CartSerializer(carts)

            print(serializer.data,"dfasdf")

            total=0
            for item in cart:
                total += item.subtotal

            convert_total= total * 100  # converting to cents
            total= int(convert_total)
            # create checkout session 
            checkout_session= stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': 'E-commerce Purchase',
                            },
                            
                            'unit_amount': total ,  # Amount in cents
                        },
                        'quantity': cart.count(),
                        
                    },
                ],

                # line_items=[
                #     {
                #         'price': 12 ,
                #         'quantity': 1,
                #     },
                # ],
                mode='payment',
                success_url=self.domain_url + 'success/',
                cancel_url=self.domain_url + 'cancel/',
            )
            return Response({'url': checkout_session['url']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.error, 'status': status.HTTP_400_BAD_REQUEST})
        
     
class StripeWebhookAPIView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        # endpoint_secret = STRIPE_SECRET_KEY
       
        
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return Response(status=400)
        
        except stripe.error.SignatureVerificationError :
            return Response(status=400)

    
        if event['type'] == 'checkout.session.completed' :
            print(event)
            print('Payment was successful.')
            print(event['data']['object']['customer'])
            amount_total = event['data']['object']['amount_total']
            customer_email = event['data']['object']['customer_details']['email']
            customer_name = event['data']['object']['customer_details']['name']
            payment_id = event['id']
            payment_status = event['data']['object']['payment_status']
            status= event['data']['object']['status']

            payment_details = PaymentDetails(
                payment_id=payment_id,
                customer_email=customer_email,
                customer_name=customer_name,
                amount_total=amount_total,
                payment_status=payment_status,
                status=status
            )
            payment_details.save()

            print(payment_details)


        elif event['type'] == 'checkout.session.async_payment_failed':
            print('Payment failed.')
        
      
        return Response(status=200)



    # serializer_class = CardInformationSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     response = {}
    #     if serializer.is_valid():
    #         data_dict = serializer.data
          
    #         stripe.api_key = 'your-key-goes-here'
    #         response = self.stripe_card_payment(data_dict=data_dict)

    #     else:
    #         response = {'errors': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST
    #             }
                
    #     return Response(response)

    # def stripe_card_payment(self, data_dict):
    #     try:
    #         # card_details = (
    #         #     type="card",
    #         #     card={
    #         #         "number": data_dict['card_number'],
    #         #         "exp_month": data_dict['expiry_month'],
    #         #         "exp_year": data_dict['expiry_year'],
    #         #         "cvc": data_dict['cvc'],
    #         #     },
    #         # )
    #         #  you can also get the amount from databse by creating a model
    #         payment_intent = stripe.PaymentIntent.create(
    #             amount=10000, 
    #             currency='inr',
    #         )
    #         payment_intent_modified = stripe.PaymentIntent.modify(
    #             payment_intent['id'],
    #             payment_method=card_details['id'],
    #         )
    #         try:
    #             payment_confirm = stripe.PaymentIntent.confirm(
    #                 payment_intent['id']
    #             )
    #             payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
    #         except:
    #             payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
    #             payment_confirm = {
    #                 "stripe_payment_error": "Failed",
    #                 "code": payment_intent_modified['last_payment_error']['code'],
    #                 "message": payment_intent_modified['last_payment_error']['message'],
    #                 'status': "Failed"
    #             }
    #         if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
    #             response = {
    #                 'message': "Card Payment Success",
    #                 'status': status.HTTP_200_OK,
    #                 "card_details": card_details,
    #                 "payment_intent": payment_intent_modified,
    #                 "payment_confirm": payment_confirm
    #             }
    #         else:
    #             response = {
    #                 'message': "Card Payment Failed",
    #                 'status': status.HTTP_400_BAD_REQUEST,
    #                 "card_details": card_details,
    #                 "payment_intent": payment_intent_modified,
    #                 "payment_confirm": payment_confirm
    #             }
    #     except:
    #         response = {
    #             'error': "Your card number is incorrect",
    #             'status': status.HTTP_400_BAD_REQUEST,
    #             "payment_intent": {"id": "Null"},
    #             "payment_confirm": {'status': "Failed"}
    #         }
    #     return response