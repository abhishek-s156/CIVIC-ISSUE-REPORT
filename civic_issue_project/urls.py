"""
urls.py (main project file)
------------------------------;;;;
This is the starting point for all web addresses (URLs) in our
project. It sends most requests to our issue_app, and also turns
on the Django admin panel.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('issue_app.urls')),
]

# this line lets us see uploaded photos while developing (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
