from django.contrib import admin
from po.models import Positions, Candidate, extra_field

# Register your models here.
admin.site.register(Positions)
admin.site.register(Candidate)
admin.site.register(extra_field)