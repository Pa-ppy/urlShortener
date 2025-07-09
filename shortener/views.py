from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from .models import URL
from .serializers import URLSerializer
from .renderers import PrettyJSONRenderer
import random
import string

class URLShortenerView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    renderer_classes = [PrettyJSONRenderer]

    def generate_short_code(self):
        length = 6
        while True:
            short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not URL.objects.filter(short_code=short_code).exists():
                return short_code

    def create(self, request, *args, **kwargs):
        original_url = request.data.get('original_url')
        try:
            url_instance = URL.objects.get(original_url=original_url)
            serializer = self.get_serializer(url_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except URL.DoesNotExist:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
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
