from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stripe_serializer import CardInformationSerializer
import stripe
from .models import Product, Cart


class PaymentAPI(APIView):

    stripe.api_key = 'your-key-goes-here'
    domain_url = 'http://localhost:8000/'

    def post(self, request):
        try:
            # get product details here
            cart_id = request.data.get('cart_id')
            cart_items=Cart.objects.get(id=cart_id)
            print('cart_items',cart_items)


            # create checkout session 
            checkout_session= stripe.checkout.Session.create(
                payment_method_types=['card'],
                # line_items=[
                #     {
                #         # 'price_data': {
                #         #     'currency': 'inr',
                #         #     'product_data': {
                #         #         'name': cart_items.product,
                #         #     },
                #         #     'unit_amount': cart_items.subtotal,  # Amount in cents
                #         # },
                #         # 'quantity': cart_items.quantity,
                        
                #     },
                # ],

                line_items=[
                    {
                        'price': 12 ,
                        'quantity': 1,
                    },
                ],


                mode='payment',
                success_url=self.domain_url + 'success/',
                cancel_url=self.domain_url + 'cancel/',
            )
            return Response({'url': checkout_session['url']}, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({'error': e.error['message'], 'status': status.HTTP_400_BAD_REQUEST})
        
     

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