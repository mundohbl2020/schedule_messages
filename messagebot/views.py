from django.shortcuts import render
from django.http import HttpResponse
from messagebot.forms import MessageForm,AfterRegistration
from messagebot.models import AfterRegistration,EveryDay,SpecificDay,Events,Messages
from datetime import datetime 
import pytz
from messaging import settings
from django.utils.timezone import localtime
import  json
import logging
from time import sleep
import requests
import time
import gspread
from django.conf import settings
import os
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(settings.BASE_DIR,"credentials.json"), scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=0").sheet1
user_sheet=client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=1831337301").get_worksheet(1)
TOKEN="1295514171:AAGGiqZHneD8REKvHVAg_k_XDBm2ti3t1dI"
# Create your views here.
WET=pytz.timezone('Portugal')
def hello_world(request):
	return render(request, 'index.html', {})
def help(request):
	return render(request, 'help.html',{})

def display(request):
	params={"error":"hi"}
	if request.method == "POST":
		MyMessage = MessageForm(request.POST)
		if MyMessage.is_valid():
			params={
			"name":MyMessage.cleaned_data['name'],
			"message":MyMessage.cleaned_data['message'],
			"link":MyMessage.cleaned_data['link'],
			"image":MyMessage.cleaned_data['image'],
			"link_text":MyMessage.cleaned_data['link_text'],
			"order":MyMessage.cleaned_data['order']}
			MyMessage.save()
		else:
			params={"error":"Please enter correct details"}
			return render(request,"index.html",params)
	return render(request,'display.html',{"params":params})


def schedule_daily_events():
	daily_events=EveryDay.objects.all()
	for event in daily_events:
		date_obj=datetime.now(WET)
		req_time= datetime(date_obj.year,date_obj.month,date_obj.day,event.hours,event.minutes).timestamp()
		display_time1=datetime.fromtimestamp(req_time).strftime("%Y-%m-%d %H:%M")
		event_id=str(date_obj.year)+str(date_obj.month)+str(date_obj.day)+str(event.hours)+str(event.minutes)
		if len(event_id) <14:
			for i in range(0,14-len(event_id)):
				event_id=str(0)+event_id
		event_id='D'+event_id
		new_event_obj=Events(display_date=display_time1,time=req_time,name=Messages.objects.get(name=event.name),event_id=event_id)
		record=Events.objects.filter(event_id=event_id).count()
		if record>0:
			continue
		print(record)
		new_event_obj.save()
	return None

def schedule_after_reg_events(user='500145420'):
	after_reg_events = AfterRegistration.objects.all()
	for event in after_reg_events:
		total_sec= event.days*24*60*60 + event.hours*60*60 +event.minutes*60
		if user == "ALL":
			user="500"
		event_id=str(user)+str(event.days)+str(event.hours)+str(event.minutes)
		if len(event_id) <14:
			for i in range(0,14-len(event_id)):
				event_id=str(0)+event_id
		event_id='R'+event_id
		date_obj=datetime.now(WET)
		req_time= datetime(date_obj.year,date_obj.month,date_obj.day+event.days,event.hours,event.minutes).timestamp()
		if req_time-date_obj.timestamp() <0 and event.days == 0:
			req_time= datetime(date_obj.year,date_obj.month,date_obj.day+1,event.hours,event.minutes).timestamp()
		display_time1=datetime.fromtimestamp(req_time).strftime("%Y-%m-%d %H:%M")
		new_event_obj=Events(display_date=display_time1,time=req_time,name=Messages.objects.get(name=event.name),event_id=event_id,user=user)
		record=Events.objects.filter(event_id=event_id).count()
		if record>0:
			continue
		new_event_obj.save()
	return None

def schedule_specific_events(user='ALL'):
	specific_day_events = SpecificDay.objects.all()
	for event in specific_day_events:
		date_obj=localtime(event.date)
		date=datetime(date_obj.year,date_obj.month,date_obj.day,date_obj.hour,date_obj.minute).timestamp()
		display_time1=datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M")
		event_id=str(date_obj.year)+str(date_obj.month)+str(date_obj.day)+str(date_obj.hour)+str(date_obj.minute)
		if len(event_id) <14:
			for i in range(0,14-len(event_id)):
				event_id=str(0)+event_id
		event_id='S'+event_id
		new_event_obj=Events(display_date=display_time1,time=date,name=Messages.objects.get(name=event.name),event_id=event_id)
		record=Events.objects.filter(event_id=event_id).count()
		if record>0:
			continue
		new_event_obj.save()
	return None


def schedule_event(request):	
	user='ALL'
	if request.GET.get('user') != None:
		user=request.GET['user']

	schedule_after_reg_events(user)
	schedule_daily_events()
	schedule_specific_events()
	date_obj=datetime.now(WET)
	start_of_the_today= int(datetime(date_obj.year,date_obj.month,date_obj.day,0,0).timestamp())
	end_of_the_day=int(datetime(date_obj.year,date_obj.month,date_obj.day,23,55).timestamp())
	today_events=Events.objects.filter(time__gte=start_of_the_today,time__lte=end_of_the_day)
	Events.objects.filter(time__lte=start_of_the_today).delete()
	events_obj={"events":[]}
	for event in today_events:
		events_obj['events'].append({'user_id':event.user,'time':event.time,'message_name':event.name.name})
	return HttpResponse(json.dumps(events_obj), content_type="application/json")
	



def get_message(request):
	message='Message1'
	if request.GET.get('name') != None:
		message=request.GET['name']

	message=Messages.objects.filter(name__iexact=message)
	if message.count() == 0:
		return HttpResponse(json.dumps({"status":"message not found"}), content_type="application/json")
	message=message[0]
	message_obj={'text':message.message,'image':message.image,'link':message.link,'link_text':message.link_text,'order':message.order}
	return HttpResponse(json.dumps(message_obj), content_type="application/json")

	
	
def send_message(request):
	message='Message1'
	bot_url='https://api.telegram.org/bot' + TOKEN 
	if request.GET.get('name') != None:
		message=request.GET['name']
	uid= str(371051489)
	if request.GET.get('userid') != None:
		uid=request.GET['userid']
	try:
		message=Messages.objects.filter(name__iexact=message)
		if message.count() == 0:
			return HttpResponse(json.dumps({"status":"message not found"}), content_type="application/json")
		message_obj=message[0]
		print(message_obj)
		user_row = user_sheet.find(uid).row
		coachId = user_sheet.acell('B{}'.format(str(user_row))).value
		coach_row = sheet.find(coachId).row
		coach_data=sheet.row_values(coach_row)
		print(coach_data)
		text = message_obj.message
		link = message_obj.link
		image= message_obj.image
		link_text =message_obj.link_text
		order = message_obj.order
		if 'COACH_MOBILE' in text:
			text = text.replace('COACH_MOBILE',"%2B"+coach_data[4])
		if 'COACH_NAME' in text:
			text = text.replace('COACH_NAME',coach_data[2])
		if 'PRODUCT_LINK' in text:
			text =  text.replace('PRODUCT_LINK',coach_data[6])
		if 'COACH_EMAIL' in text:
			text =  text.replace('COACH_EMAIL',coach_data[3])
		if 'BUSiNESS_LINK' in text:
			text =  text.replace('BUSiNESS_LINK',coach_data[5])
		if 'FACEBOOK_LINK' in text:
			text = text.replace('FACEBOOK_LINK',coach_data[7])
		if 'INSTAGRAM_LINK' in text:
			text = text.replace('INSTAGRAM_LINK',coach_data[8])
		if 'LEAD_NAME' in text:
			text=text.replace('LEAD_NAME',user_sheet.acell('Q{}'.format(str(user_row))).value)
		for i in order:
			sleep(3)
			print(i)
			if i == 'M':
				text = text.replace('&', '%26')
				res=requests.get(bot_url+'/sendMessage?chat_id='+ uid + '&parse_mode=HTML&text=' + text)
				print(res.json())
			elif i == 'P':
				res=requests.get(bot_url+'/sendPhoto?chat_id='+uid+'&photo='+image)
			elif i== 'L':
				link=link.replace('&','%26')
				link_text= link_text.replace('&','%26')
				msg= '<a href="'+link+'">'+link_text+'</a>'
				res=requests.get(bot_url+'/sendMessage?chat_id='+ uid + '&parse_mode=HTML&text=' + msg)
				print(res.json())
		return HttpResponse(json.dumps({"status":"message_sent"}), content_type="application/json")	
	except Exception as e:
		print(e)
		return e





