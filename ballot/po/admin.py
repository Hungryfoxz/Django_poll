from unicodedata import name
from django.contrib import admin
from po.models import Positions, Candidate, extra_field, Mock,Mock_Positions,Voted
#from django.contrib.auth.models import Group

# Unregister Group Here
#admin.site.unregister(Group)
# Change admin site name Here..
admin.site.site_header = "JIST Admin"
admin.site.index_title = "Welcome to JIST Admin Panel"
admin.site.site_title = "Jorhat Institute Of Science and Technology"


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'votes')


# Register your models here.
admin.site.register(Positions)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(extra_field)
admin.site.register(Voted)
admin.site.register(Mock)
admin.site.register(Mock_Positions)