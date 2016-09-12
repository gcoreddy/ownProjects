from django.contrib import admin
from myproject.tims.models import Stream
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('StreamName', 'StreamType','Source','EncodedStreamType','RawStreamType','Resolution','Frames','ScanType','Complexity','FrameCount','Conformance','ContainerFormat')
    search_fields = ('StreamName', 'StreamType','Source','EncodedStreamType','RawStreamType','Resolution','Frames','ScanType','Complexity','FrameCount','Conformance','ContainerFormat')
admin.site.register(Stream,AuthorAdmin)
admin.site.site_title = 'Stream Management'
admin.site.site_header = 'TIMS(TEST INPUT MANAGEMENT SYSTEM)'
admin.site.index_title = "Welcome to Stream Management and Storage System"
#admin.site.register(AuthorAdmin)
# Register your models here.
