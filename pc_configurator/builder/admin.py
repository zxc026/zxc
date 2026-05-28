from django.contrib import admin
from .models import CPU, Motherboard, GPU

admin.site.register(CPU)
admin.site.register(Motherboard)
admin.site.register(GPU)