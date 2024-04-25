from django.contrib import admin
from .models import Profile,File,DataUpload

class FileAdmin(admin.ModelAdmin):
    list_display=('file','profile')




admin.site.register(File,FileAdmin)
admin.site.register(Profile)
admin.site.register(DataUpload)


