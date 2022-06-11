from unicodedata import name
from django.contrib import admin
from po.models import Positions, Candidate, extra_field


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'votes')
    
# Register your models here.
admin.site.register(Positions)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(extra_field)