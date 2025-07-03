
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('twilio/webhook/', views.twilio_webhook),
    path('api/feedback-data/',views.feedback_data_api, name='feedback-data-api'),
    path('', views.dashboard_view, name='dashboard'),
    path('send-test/', views.send_test_message),
]
