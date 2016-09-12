from django.contrib import admin

# Register your models here.
from django.contrib import admin
from sqadashboard import models as m

admin.site.register(m.Search)
admin.site.register(m.Query)