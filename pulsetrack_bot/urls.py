
from django.contrib import admin
from django.urls import path,include
from myapp.views import twilio_webhook, feedback_data_api, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]