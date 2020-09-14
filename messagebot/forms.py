from django import forms
from django.forms import ModelForm
from messagebot.models import Messages,AfterRegistration

class MessageForm(ModelForm):
	class Meta:
		model = Messages
		fields=['message_id','name','message','image','link','link_text','order']

class AfterRegistration(ModelForm):
	class Meta:
		model = AfterRegistration
		fields=['event_id','days','hours','minutes','name']