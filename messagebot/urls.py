from django.urls import path
from messagebot import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('help', views.help, name='help'),
    path('display',views.display,name="display"),
    path('schedule',views.schedule_event,name="schedule_event"),
    path('message',views.get_message,name="get_message"),
    path('sendmessage',views.send_message,name="send_message"),
]