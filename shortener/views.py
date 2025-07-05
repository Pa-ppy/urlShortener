from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from .models import URL
from .serializers import URLSerializer
import random
import string

class URLShortenerView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def generate_short_code(self):
        length = 6
        while True:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not URL.objects.filter(short_code=short_code).exists():
                return short_code

    def perform_create(self, serializer):
        original_url = serializer.validated_data['original_url']
        # Check if the URL already exists
        try:
            url_instance = URL.objects.get(original_url=original_url)
            # If it exists, return the existing short URL
            serializer.instance = url_instance
        except URL.DoesNotExist:
            # If it doesn't exist, create a new one
            short_code = self.generate_short_code()
            serializer.save(short_code=short_code)

class URLRedirectView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    lookup_field = 'short_code'

    def get(self, request, *args, **kwargs):
        short_code = self.kwargs['short_code']
        url_instance = get_object_or_404(URL, short_code=short_code)
        url_instance.clicks += 1
        url_instance.save()
        return redirect(url_instance.original_url)