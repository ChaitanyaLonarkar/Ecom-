from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
def cron_job(): 

    send_mail(
            'Daily Update',
            'This is your daily update email.',
            'from@example.com',
            ['chaitanyalonarkar@gmail.com'],
            fail_silently=False,
        )
    # try:
        # send_mail(
        #         'This is cronm Job mail',
        #         # email_html_message,  # Use html_message for HTML content
        #         f"This is cronm Job mail, please check it",
        #         'django@gmail.com',
        #         ['chaitanyalonarkar@gmail.com'],
        #         fail_silently=False,
        #         # html_message=email_html_message,
        #     )
    #     return("Mail sent successfully")
    # except :
    #     return("Error in sending mail")


class CronJobDemo(APIView):
    def get(self, request):
        cron_job()
        return Response({'message': 'Cron job executed successfully'}, status=status.HTTP_200_OK)
