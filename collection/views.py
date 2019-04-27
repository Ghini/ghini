from django.shortcuts import render
from rest_framework import generics, viewsets, views
from rest_framework import status
from rest_framework.response import Response

from .models import Accession, Contact, Verification
from .serializers import AccessionSerializer, ContactSerializer, VerificationSerializer

# Create your views here.

class AccessionList(generics.ListCreateAPIView):
    lookup_field = 'code'
    queryset = Accession.objects.all()
    serializer_class = AccessionSerializer

class AccessionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    serializer_class = AccessionSerializer

    def get_queryset(self):
        queryset = Accession.objects.filter(code=self.kwargs['code'])
        return queryset


class AccessionInfobox(AccessionDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        obj = qs.first()
        if obj:
            serializer = AccessionSerializer(instance=obj)
            result = serializer.data
            del result['id']
            result['taxa'] = ", ".join(["%s" % i for i in obj.taxa.all()])
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)

class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
        
class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
        
class ContactInfobox(ContactDetail):
    pass

class VerificationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'

    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Verification.objects.filter(accession=accession)
        return queryset

    serializer_class = VerificationSerializer

class VerificationList(generics.ListCreateAPIView):
    def post(self, request, accession_code):
        from collection.models import Accession
        accession = Accession.objects.filter(code=accession_code).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['accession'] = accession.pk
        if 'code' not in data:
            from django.db import models
            max_code = (Verification.objects
                        .filter(accession=accession)
                        .aggregate(max_code=models.Max('code')))['max_code']
            data['code'] = (max_code or 0) + 1
        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            verification = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'ser': serializer.errors, 'dat': data}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Verification.objects.filter(accession=accession)
        return queryset

    serializer_class = VerificationSerializer
