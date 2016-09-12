from __future__ import unicode_literals

from django.db import models
from django.db import models as m
from django.utils import timezone

# Create your models here.

class Search(m.Model):
	projectName = m.CharField(max_length=10)
	scope = m.CharField(max_length=20)
	startDate = m.DateField('Date time created')
	endDate = m.DateField()
	csvFile = m.CharField(max_length=20)
	genericString = m.CharField(default="END TO END TESTING",max_length=50)


class Query(m.Model):
	search = m.ForeignKey(Search)
	projectName = m.CharField(default="VDK",max_length=10)
	scope = m.CharField(default="SANITY",max_length=20)
	startDate = m.DateField('Date time created')
	endDate = m.DateField()
	csvFile = m.CharField(max_length=20)
	genericString = m.CharField(default="END TO END TESTING",max_length=50)