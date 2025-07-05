from django.urls import path
from .views import URLShortenerView, URLRedirectView

urlpatterns = [
    path('api/shorten/', URLShortenerView.as_view(), name='url-shorten'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url-redirect'),
]
