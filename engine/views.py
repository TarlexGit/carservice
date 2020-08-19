from django.shortcuts import render 
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group 
from rest_framework import permissions
from .serializers import SignUpSerializer, MasterSerializer
from .models import FixDate, Master
from . import services
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.all()#.filter(work_status=True)
    serializer_class = MasterSerializer
    permission_classes = [permissions.IsAuthenticated]

import datetime
class RecordList(APIView):  
    def get(self, request, format=None): 
        records = FixDate.objects.all().filter(date_pub__gte=datetime.date.today())
        start_times = [str(records.start_time) for records in FixDate.objects.all()]
        end_times = [str(records.end_time)for records in FixDate.objects.all()]
        di = dict(zip(start_times, end_times))

        return Response(di)


class SignUpView(generics.CreateAPIView):
    queryset = FixDate.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser,)

    def post(self, request):
        req = self.request 
          
        if services.chek_and_return(req)  == False:
            return Response({'message':'Время занято.'}, status = status.HTTP_400_BAD_REQUEST)
        else: profile = services.chek_and_return(req)

        chek = services.chek_work_time(date = profile['start_date'], time = profile['start_time'])
        serializer_class = SignUpSerializer(data=profile) 
        mes = chek['message'] 

        if serializer_class.is_valid() and chek['correct'] == True:
            serializer_class.save()
            return Response({'message':mes}, status = status.HTTP_201_CREATED)
        else:
            return Response({'message':mes}, status = status.HTTP_400_BAD_REQUEST) 
 
