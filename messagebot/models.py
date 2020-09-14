from django.db import models
from django.utils.timezone import localtime
# Create your models here.
class Messages(models.Model):
	message_id = models.AutoField(primary_key=True)
	name=models.CharField(max_length=1000,default="Message1",unique=True)
	message = models.TextField( blank=True, default='')
	image = models.CharField(max_length=1000, blank=True, default='')
	link=models.CharField(max_length=1000, blank=True, default='')
	link_text=models.CharField(max_length=1000, blank=True, default='')
	order=models.CharField(max_length=3)

	class Meta:
		db_table=u'Messages'
	def __str__(self):  
		return u'%s' % (self.name)


class AfterRegistration(models.Model):
	event_id = models.AutoField(primary_key=True)
	days = models.IntegerField()
	hours = models.IntegerField()
	minutes = models.IntegerField()
	name=models.ForeignKey(Messages,to_field='name',on_delete=models.CASCADE)




	class Meta:
		verbose_name = (u"After Registration")
		db_table=u'AfterRegistration'
	def __str__(self):
		return u'After %s days -----  at %s:%s  ----- send %s' % (self.days,self.hours,self.minutes, self.name )
	

class EveryDay(models.Model):
	event_id=models.AutoField(primary_key=True)
	hours=models.IntegerField()
	minutes=models.IntegerField()
	name= models.ForeignKey(Messages,to_field='name',on_delete=models.CASCADE)

	class Meta:
		verbose_name = (u"EveryDay")
		db_table=u'EveryDay'
	def __str__(self):
		return u'At  %s hours -----  %s  minutes ----- send %s' % (self.hours,self.minutes, self.name )


class SpecificDay(models.Model):
	event_id=models.AutoField(primary_key=True)
	date = models.DateTimeField()
	name=models.ForeignKey(Messages,to_field='name',on_delete=models.CASCADE)

	class Meta:
		verbose_name = (u"SpecificDay")
		db_table=u'SpecificDay'
	def __str__(self):
		return u'At  %s  ----- send %s' % (localtime(self.date), self.name )


class Events(models.Model):
	event_id=models.CharField(primary_key=True,max_length=16)
	display_date=models.DateTimeField()
	time=models.IntegerField()
	name=models.ForeignKey(Messages,to_field='name',on_delete=models.CASCADE)
	user=models.CharField(max_length=100,default="ALL")

	class Meta:
		verbose_name= (u'Event')
		db_table=u'Events'
	def __str__(self):
		return u'At %s ------- send %s ------- to %s  %s' % (localtime(self.display_date),self.name,self.user,self.event_id)